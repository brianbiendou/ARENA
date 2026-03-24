import { useEffect, useState, useMemo } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { useExperimentStore } from "../stores/experimentStore.ts";
import { useProviderStore } from "../stores/providerStore.ts";
import { runs } from "../services/api.ts";
import Card from "../components/ui/Card.tsx";
import Button from "../components/ui/Button.tsx";
import Slider from "../components/ui/Slider.tsx";
import Select from "../components/ui/Select.tsx";
import Toggle from "../components/ui/Toggle.tsx";
import Badge from "../components/ui/Badge.tsx";
import type { AgentConfig, ExperimentSetup, ModelInfo, ProviderType } from "../types";

const AGENT_COLORS = ["#6366f1", "#22c55e", "#ef4444", "#f59e0b", "#06b6d4", "#ec4899", "#8b5cf6", "#14b8a6", "#f97316", "#e11d48"];
const AGENT_NAMES = ["Atlas", "Lyra", "Orion", "Nova", "Vega", "Clio", "Théo", "Selene", "Kaï", "Iris"];

const PROVIDER_LABELS: Record<ProviderType, string> = {
  ollama: "Ollama",
  lm_studio: "LM Studio",
  openrouter: "OpenRouter",
};

const PROVIDER_ICONS: Record<ProviderType, string> = {
  ollama: "🦙",
  lm_studio: "🧪",
  openrouter: "🌐",
};

/** Per-agent model assignment */
interface AgentSlot {
  provider: ProviderType;
  model: string;
}

export default function Lobby() {
  const { experimentId } = useParams<{ experimentId: string }>();
  const navigate = useNavigate();
  const { experiments, fetch: fetchExperiments, getById } = useExperimentStore();
  const { providers, models, fetchProviders, fetchModels } = useProviderStore();

  const [loading, setLoading] = useState(false);

  // Experiment setup
  const [scenarioId, setScenarioId] = useState<string>("");
  const [numRounds, setNumRounds] = useState(5);
  const [numAgents, setNumAgents] = useState(5);
  const [enablePlotTwists, setEnablePlotTwists] = useState(false);
  const [enableEvents, setEnableEvents] = useState(true);
  const [temperature, setTemperature] = useState(0.7);
  const [maxTokens, setMaxTokens] = useState(800);
  const [seed, setSeed] = useState<number | undefined>(undefined);

  // Multi-model: uniform vs individual
  const [uniformMode, setUniformMode] = useState(true);
  const [globalProvider, setGlobalProvider] = useState<ProviderType>("ollama");
  const [globalModel, setGlobalModel] = useState<string>("");
  const [agentSlots, setAgentSlots] = useState<AgentSlot[]>([]);

  const exp = getById(experimentId as ExperimentSetup["experiment_id"]);

  // Available providers list
  const availableProviders = useMemo(
    () => providers.filter((p) => p.available),
    [providers],
  );

  // All models flat list for quick lookup
  const allModels = useMemo(() => {
    const flat: (ModelInfo & { providerType: ProviderType })[] = [];
    for (const type of Object.keys(models) as ProviderType[]) {
      for (const m of models[type] || []) {
        flat.push({ ...m, providerType: type });
      }
    }
    return flat;
  }, [models]);

  // ─── Effects ────────────────────────────
  useEffect(() => {
    fetchExperiments();
    fetchProviders();
  }, [fetchExperiments, fetchProviders]);

  useEffect(() => {
    if (exp) {
      setNumRounds(exp.default_rounds);
      setNumAgents(exp.default_agents);
    }
  }, [exp]);

  // Auto-load models for all available providers
  useEffect(() => {
    for (const p of availableProviders) {
      if (!models[p.type]) fetchModels(p.type);
    }
  }, [availableProviders, fetchModels]); // eslint-disable-line react-hooks/exhaustive-deps

  // Set initial global provider + model
  useEffect(() => {
    if (availableProviders.length && globalProvider === "ollama" && !availableProviders.find((p) => p.type === "ollama")) {
      setGlobalProvider(availableProviders[0].type);
    }
  }, [availableProviders, globalProvider]);

  useEffect(() => {
    const providerModels = models[globalProvider] || [];
    if (providerModels.length && !globalModel) {
      setGlobalModel(providerModels[0].id);
    }
  }, [models, globalProvider, globalModel]);

  // Sync agentSlots with numAgents
  useEffect(() => {
    setAgentSlots((prev) => {
      const next = [...prev];
      while (next.length < numAgents) {
        next.push({ provider: globalProvider, model: globalModel });
      }
      return next.slice(0, numAgents);
    });
  }, [numAgents, globalProvider, globalModel]);

  // When global model changes in uniform mode, sync all slots
  useEffect(() => {
    if (uniformMode) {
      setAgentSlots((prev) =>
        prev.map(() => ({ provider: globalProvider, model: globalModel })),
      );
    }
  }, [uniformMode, globalProvider, globalModel]);

  // ─── Helper: update one slot ────────────
  const updateSlot = (index: number, patch: Partial<AgentSlot>) => {
    setAgentSlots((prev) => {
      const next = [...prev];
      next[index] = { ...next[index], ...patch };
      return next;
    });
  };

  // Assign random models across available models
  const randomizeModels = () => {
    if (allModels.length === 0) return;
    setAgentSlots((prev) =>
      prev.map(() => {
        const m = allModels[Math.floor(Math.random() * allModels.length)];
        return { provider: m.providerType, model: m.id };
      }),
    );
    setUniformMode(false);
  };

  // ─── Guard ──────────────────────────────
  if (!exp && experiments.length > 0) {
    return (
      <div className="text-center py-20 text-arena-muted">
        Expérience introuvable.
        <Button variant="ghost" className="ml-2" onClick={() => navigate("/")}>
          Retour au Hub
        </Button>
      </div>
    );
  }

  if (!exp) {
    return (
      <div className="text-center py-20">
        <div className="animate-spin inline-block w-8 h-8 border-2 border-arena-accent border-t-transparent rounded-full" />
      </div>
    );
  }

  // ─── Can launch? ────────────────────────
  const canLaunch = uniformMode
    ? !!globalModel
    : agentSlots.every((s) => !!s.model);

  // ─── Launch ─────────────────────────────
  const handleLaunch = async () => {
    if (!canLaunch) return;
    setLoading(true);

    const agents: AgentConfig[] = Array.from({ length: numAgents }, (_, i) => {
      const slot = uniformMode
        ? { provider: globalProvider, model: globalModel }
        : agentSlots[i];
      return {
        id: `agent_${i}`,
        name: AGENT_NAMES[i] || `Agent ${i + 1}`,
        model: slot.model,
        provider: slot.provider,
        color: AGENT_COLORS[i % AGENT_COLORS.length],
      };
    });

    const setup: ExperimentSetup = {
      experiment_id: exp.id,
      scenario_id: scenarioId || undefined,
      num_rounds: numRounds,
      enable_plot_twists: enablePlotTwists,
      plot_twist_intensity: "moderate",
      enable_random_events: enableEvents,
      custom_parameters: {},
    };

    try {
      await runs.start({
        experiment: setup,
        agents,
        seed,
        temperature,
        top_p: 0.9,
        max_tokens: maxTokens,
        response_timeout_s: 60,
      });
      navigate("/arena");
    } catch (e) {
      console.error("Failed to start run:", e);
    } finally {
      setLoading(false);
    }
  };

  // ─── Helpers for rendering ──────────────
  const globalProviderModels = models[globalProvider] || [];
  const distinctModels = uniformMode
    ? [globalModel]
    : [...new Set(agentSlots.map((s) => s.model))];

  return (
    <div className="max-w-6xl mx-auto pb-8">
      {/* Header */}
      <div className="flex items-center gap-4 mb-8">
        <Button variant="ghost" size="sm" onClick={() => navigate("/")}>
          ← Retour
        </Button>
        <div className="flex items-center gap-3">
          <span className="text-3xl">{exp.icon}</span>
          <div>
            <h1 className="text-2xl font-bold text-white">{exp.display_name}</h1>
            <p className="text-sm text-arena-muted">{exp.tagline}</p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">

        {/* ═══════════════════════════════════════
            Col 1: Configuration de l'expérience
           ═══════════════════════════════════════ */}
        <Card>
          <h2 className="text-lg font-semibold text-white mb-4">⚙️ Configuration</h2>

          <Select
            label="Scénario"
            value={scenarioId}
            options={[
              { value: "", label: "🎲 Aléatoire" },
              ...exp.scenarios.map((s) => ({ value: s.id, label: `${s.name}` })),
            ]}
            onChange={setScenarioId}
          />

          {/* Scenario description tooltip */}
          <AnimatePresence>
            {scenarioId && exp.scenarios.find((s) => s.id === scenarioId) && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: "auto" }}
                exit={{ opacity: 0, height: 0 }}
                className="mt-2 p-3 rounded-lg bg-arena-accent/5 border border-arena-accent/10 text-xs text-arena-muted leading-relaxed"
              >
                {exp.scenarios.find((s) => s.id === scenarioId)!.description}
              </motion.div>
            )}
          </AnimatePresence>

          <div className="mt-5 space-y-4">
            <Slider label="Agents" value={numAgents} min={exp.min_agents} max={exp.max_agents} onChange={(v) => setNumAgents(v)} />
            <Slider label="Tours" value={numRounds} min={exp.min_rounds} max={exp.max_rounds} onChange={setNumRounds} />
          </div>

          <div className="mt-6 space-y-3">
            <Toggle label="Événements aléatoires" checked={enableEvents} onChange={setEnableEvents} />
            <Toggle label="Plot twists" checked={enablePlotTwists} onChange={setEnablePlotTwists} />
          </div>

          <div className="mt-6 space-y-4">
            <Slider label="🌡️ Température" value={temperature} min={0} max={2} step={0.1} onChange={setTemperature} />
            <Slider label="📝 Max Tokens" value={maxTokens} min={200} max={4096} step={100} onChange={setMaxTokens} />
          </div>

          <div className="mt-5">
            <label className="text-sm text-arena-muted">Seed (optionnel)</label>
            <input
              type="number"
              placeholder="Aléatoire"
              value={seed ?? ""}
              onChange={(e) => setSeed(e.target.value ? Number(e.target.value) : undefined)}
              className="w-full mt-1 px-3 py-2 rounded-lg bg-arena-bg border border-arena-border text-arena-text text-sm focus:border-arena-accent focus:outline-none"
            />
          </div>
        </Card>

        {/* ═══════════════════════════════════════
            Col 2: Agents & Modèles
           ═══════════════════════════════════════ */}
        <Card>
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-white">🤖 Agents & Modèles</h2>
            {!uniformMode && allModels.length > 0 && (
              <button
                onClick={randomizeModels}
                className="text-xs text-arena-accent hover:text-arena-accent-light transition-colors px-2 py-1 rounded-lg hover:bg-arena-accent/5"
              >
                🎲 Aléatoire
              </button>
            )}
          </div>

          {/* Mode toggle */}
          <div className="flex rounded-xl bg-arena-bg/80 p-1 mb-5">
            <button
              className={`flex-1 text-sm py-2 rounded-lg font-medium transition-all ${
                uniformMode
                  ? "bg-arena-accent text-white shadow-lg shadow-arena-accent/20"
                  : "text-arena-muted hover:text-white"
              }`}
              onClick={() => setUniformMode(true)}
            >
              Même modèle
            </button>
            <button
              className={`flex-1 text-sm py-2 rounded-lg font-medium transition-all ${
                !uniformMode
                  ? "bg-arena-accent text-white shadow-lg shadow-arena-accent/20"
                  : "text-arena-muted hover:text-white"
              }`}
              onClick={() => setUniformMode(false)}
            >
              Modèles différents
            </button>
          </div>

          <AnimatePresence mode="wait">
            {uniformMode ? (
              /* ─── Uniform mode: single selector ─── */
              <motion.div key="uniform" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="space-y-4">
                <Select
                  label="Fournisseur"
                  value={globalProvider}
                  options={availableProviders.map((p) => ({
                    value: p.type,
                    label: `${PROVIDER_ICONS[p.type]} ${PROVIDER_LABELS[p.type]}`,
                  }))}
                  onChange={(v) => {
                    setGlobalProvider(v as ProviderType);
                    setGlobalModel("");
                  }}
                />
                <Select
                  label="Modèle"
                  value={globalModel}
                  options={globalProviderModels.map((m) => ({ value: m.id, label: m.name || m.id }))}
                  onChange={setGlobalModel}
                />

                {globalModel && (
                  <p className="text-xs text-arena-muted mt-1">
                    → Les {numAgents} agents utiliseront <span className="text-arena-accent font-medium">{globalModel}</span>
                  </p>
                )}
              </motion.div>
            ) : (
              /* ─── Individual mode: per-agent selectors ─── */
              <motion.div key="individual" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
                <div className="space-y-2 max-h-105 overflow-y-auto pr-1 custom-scrollbar">
                  {agentSlots.slice(0, numAgents).map((slot, i) => {
                    const slotModels = models[slot.provider] || [];
                    return (
                      <motion.div
                        key={i}
                        initial={{ opacity: 0, x: -10 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: i * 0.03 }}
                        className="rounded-xl border border-arena-border/50 bg-arena-bg/40 p-3"
                      >
                        {/* Agent header */}
                        <div className="flex items-center gap-2 mb-2">
                          <div
                            className="w-3 h-3 rounded-full shrink-0"
                            style={{ backgroundColor: AGENT_COLORS[i % AGENT_COLORS.length] }}
                          />
                          <span className="text-sm font-medium text-white">
                            {AGENT_NAMES[i] || `Agent ${i + 1}`}
                          </span>
                        </div>

                        {/* Provider + Model row */}
                        <div className="flex gap-2">
                          <select
                            title={`Fournisseur pour ${AGENT_NAMES[i] || `Agent ${i + 1}`}`}
                            value={slot.provider}
                            onChange={(e) => {
                              const prov = e.target.value as ProviderType;
                              const provModels = models[prov] || [];
                              updateSlot(i, {
                                provider: prov,
                                model: provModels.length ? provModels[0].id : "",
                              });
                            }}
                            className="w-28 shrink-0 px-2 py-1.5 rounded-lg bg-arena-bg border border-arena-border/60 text-arena-text text-xs focus:border-arena-accent focus:outline-none"
                          >
                            {availableProviders.map((p) => (
                              <option key={p.type} value={p.type}>
                                {PROVIDER_LABELS[p.type]}
                              </option>
                            ))}
                          </select>
                          <select
                            title={`Modèle pour ${AGENT_NAMES[i] || `Agent ${i + 1}`}`}
                            value={slot.model}
                            onChange={(e) => updateSlot(i, { model: e.target.value })}
                            className="flex-1 min-w-0 px-2 py-1.5 rounded-lg bg-arena-bg border border-arena-border/60 text-arena-text text-xs focus:border-arena-accent focus:outline-none truncate"
                          >
                            {slotModels.length === 0 && (
                              <option value="">Aucun modèle</option>
                            )}
                            {slotModels.map((m) => (
                              <option key={m.id} value={m.id}>
                                {m.name || m.id}
                              </option>
                            ))}
                          </select>
                        </div>
                      </motion.div>
                    );
                  })}
                </div>

                {/* Quick-apply: copy one agent's config to all */}
                {numAgents > 1 && (
                  <div className="mt-3 pt-3 border-t border-arena-border/30">
                    <p className="text-xs text-arena-muted mb-2">Appliquer à tous :</p>
                    <div className="flex flex-wrap gap-1">
                      {agentSlots.slice(0, numAgents).map((slot, i) => (
                        <button
                          key={i}
                          onClick={() => {
                            setAgentSlots((prev) =>
                              prev.map(() => ({ ...slot })),
                            );
                          }}
                          className="text-xs px-2 py-1 rounded-lg border border-arena-border/40 text-arena-muted hover:text-white hover:border-arena-accent/40 hover:bg-arena-accent/5 transition-all"
                          title={`Appliquer le modèle de ${AGENT_NAMES[i]} à tous`}
                        >
                          <span
                            className="inline-block w-2 h-2 rounded-full mr-1 align-middle"
                            style={{ backgroundColor: AGENT_COLORS[i % AGENT_COLORS.length] }}
                          />
                          {AGENT_NAMES[i]}
                        </button>
                      ))}
                    </div>
                  </div>
                )}
              </motion.div>
            )}
          </AnimatePresence>
        </Card>

        {/* ═══════════════════════════════════════
            Col 3: Aperçu & Lancer
           ═══════════════════════════════════════ */}
        <Card>
          <h2 className="text-lg font-semibold text-white mb-4">👁️ Aperçu</h2>

          {/* Scenario preview */}
          {scenarioId && exp.scenarios.find((s) => s.id === scenarioId) && (
            <div className="mb-4 p-3 rounded-lg bg-arena-bg border border-arena-border">
              <p className="text-sm font-medium text-white">
                {exp.scenarios.find((s) => s.id === scenarioId)!.name}
              </p>
              <p className="text-xs text-arena-muted mt-1 line-clamp-3">
                {exp.scenarios.find((s) => s.id === scenarioId)!.description}
              </p>
            </div>
          )}

          {/* Agent roster */}
          <div className="mb-5">
            <p className="text-sm text-arena-muted mb-2">Agents ({numAgents})</p>
            <div className="space-y-1.5">
              {Array.from({ length: numAgents }, (_, i) => {
                const slot = uniformMode
                  ? { provider: globalProvider, model: globalModel }
                  : agentSlots[i] || { provider: globalProvider, model: globalModel };
                return (
                  <motion.div
                    key={i}
                    initial={{ opacity: 0, scale: 0.95 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: i * 0.04 }}
                    className="flex items-center gap-2 text-xs"
                  >
                    <div
                      className="w-2.5 h-2.5 rounded-full shrink-0"
                      style={{ backgroundColor: AGENT_COLORS[i % AGENT_COLORS.length] }}
                    />
                    <span className="text-white font-medium w-14 shrink-0">{AGENT_NAMES[i] || `Agent ${i + 1}`}</span>
                    <span className="text-arena-muted truncate">
                      {PROVIDER_ICONS[slot.provider]} {slot.model || "—"}
                    </span>
                  </motion.div>
                );
              })}
            </div>
          </div>

          {/* Stats */}
          <div className="text-xs text-arena-muted space-y-1.5 mb-6 pt-3 border-t border-arena-border/40">
            <p>🔄 {numRounds} tours</p>
            <p>🤖 {distinctModels.length} modèle{distinctModels.length > 1 ? "s" : ""} distinct{distinctModels.length > 1 ? "s" : ""}</p>
            <p>🌡️ Température: {temperature}</p>
            <p>📝 Max tokens: {maxTokens}</p>
            {enablePlotTwists && <p>🎭 Plot twists activés</p>}
            {enableEvents && <p>⚡ Événements activés</p>}
          </div>

          {/* Launch */}
          <Button
            size="lg"
            className="w-full"
            disabled={!canLaunch || loading}
            onClick={handleLaunch}
          >
            {loading ? (
              <span className="flex items-center justify-center gap-2">
                <span className="animate-spin inline-block w-4 h-4 border-2 border-white border-t-transparent rounded-full" />
                Lancement…
              </span>
            ) : (
              <>⚔️ Lancer l'expérience</>
            )}
          </Button>

          {!canLaunch && !loading && (
            <p className="text-xs text-arena-warning text-center mt-2">
              Sélectionnez un modèle pour chaque agent
            </p>
          )}
        </Card>
      </div>
    </div>
  );
}
