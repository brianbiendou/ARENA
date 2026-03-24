import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { motion } from "framer-motion";
import { useExperimentStore } from "../stores/experimentStore.ts";
import { useProviderStore } from "../stores/providerStore.ts";
import { runs } from "../services/api.ts";
import Card from "../components/ui/Card.tsx";
import Button from "../components/ui/Button.tsx";
import Slider from "../components/ui/Slider.tsx";
import Select from "../components/ui/Select.tsx";
import Toggle from "../components/ui/Toggle.tsx";
import Badge from "../components/ui/Badge.tsx";
import type { AgentConfig, ExperimentSetup, ProviderType } from "../types";

const AGENT_COLORS = ["#6366f1", "#22c55e", "#ef4444", "#f59e0b", "#06b6d4", "#ec4899", "#8b5cf6"];
const AGENT_NAMES = ["Atlas", "Lyra", "Orion", "Nova", "Vega", "Clio", "Théo"];

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

  // Agent model selection
  const [selectedProvider, setSelectedProvider] = useState<ProviderType>("ollama");
  const [selectedModel, setSelectedModel] = useState<string>("");

  const exp = getById(experimentId as ExperimentSetup["experiment_id"]);

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

  useEffect(() => {
    const available = providers.find((p) => p.available);
    if (available) {
      setSelectedProvider(available.type);
      fetchModels(available.type);
    }
  }, [providers, fetchModels]);

  useEffect(() => {
    if (selectedProvider) {
      fetchModels(selectedProvider);
    }
  }, [selectedProvider, fetchModels]);

  useEffect(() => {
    const providerModels = models[selectedProvider];
    if (providerModels?.length && !selectedModel) {
      setSelectedModel(providerModels[0].id);
    }
  }, [models, selectedProvider, selectedModel]);

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

  const handleLaunch = async () => {
    if (!selectedModel) return;
    setLoading(true);

    const agents: AgentConfig[] = Array.from({ length: numAgents }, (_, i) => ({
      id: `agent_${i}`,
      name: AGENT_NAMES[i] || `Agent ${i + 1}`,
      model: selectedModel,
      provider: selectedProvider,
      color: AGENT_COLORS[i] || "#888",
    }));

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

  const providerModels = models[selectedProvider] || [];

  return (
    <div className="max-w-5xl mx-auto">
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
        {/* ─── Col 1: Model Pool ─── */}
        <Card>
          <h2 className="text-lg font-semibold text-white mb-4">🤖 Modèle LLM</h2>

          <Select
            label="Fournisseur"
            value={selectedProvider}
            options={providers.filter((p) => p.available).map((p) => ({
              value: p.type,
              label: p.type === "ollama" ? "Ollama" : p.type === "lm_studio" ? "LM Studio" : "OpenRouter",
            }))}
            onChange={(v) => {
              setSelectedProvider(v as ProviderType);
              setSelectedModel("");
            }}
          />

          <div className="mt-4">
            <Select
              label="Modèle"
              value={selectedModel}
              options={providerModels.map((m) => ({ value: m.id, label: m.name || m.id }))}
              onChange={setSelectedModel}
            />
          </div>

          {selectedModel && (
            <div className="mt-3">
              <Badge label={selectedModel} color={exp.color_primary} />
            </div>
          )}

          <div className="mt-6 space-y-4">
            <Slider label="Température" value={temperature} min={0} max={2} step={0.1} onChange={setTemperature} />
            <Slider label="Max Tokens" value={maxTokens} min={200} max={2000} step={100} onChange={setMaxTokens} />
          </div>
        </Card>

        {/* ─── Col 2: Experiment Config ─── */}
        <Card>
          <h2 className="text-lg font-semibold text-white mb-4">⚙️ Configuration</h2>

          <Select
            label="Scénario"
            value={scenarioId}
            options={[
              { value: "", label: "🎲 Aléatoire" },
              ...exp.scenarios.map((s) => ({ value: s.id, label: s.name })),
            ]}
            onChange={setScenarioId}
          />

          <div className="mt-4 space-y-4">
            <Slider label="Agents" value={numAgents} min={exp.min_agents} max={exp.max_agents} onChange={setNumAgents} />
            <Slider label="Tours" value={numRounds} min={exp.min_rounds} max={exp.max_rounds} onChange={setNumRounds} />
          </div>

          <div className="mt-6 space-y-3">
            <Toggle label="Événements aléatoires" checked={enableEvents} onChange={setEnableEvents} />
            <Toggle label="Plot twists" checked={enablePlotTwists} onChange={setEnablePlotTwists} />
          </div>

          <div className="mt-6">
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

        {/* ─── Col 3: Preview & Launch ─── */}
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

          {/* Agent preview */}
          <div className="space-y-2 mb-6">
            <p className="text-sm text-arena-muted">Agents ({numAgents})</p>
            <div className="flex flex-wrap gap-2">
              {Array.from({ length: numAgents }, (_, i) => (
                <motion.div
                  key={i}
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ delay: i * 0.05 }}
                >
                  <Badge
                    label={AGENT_NAMES[i] || `Agent ${i + 1}`}
                    color={AGENT_COLORS[i]}
                  />
                </motion.div>
              ))}
            </div>
          </div>

          {/* Summary */}
          <div className="text-xs text-arena-muted space-y-1 mb-6">
            <p>🔄 {numRounds} tours</p>
            <p>🤖 {selectedModel || "Aucun modèle"}</p>
            <p>🌡️ Température: {temperature}</p>
            {enablePlotTwists && <p>🎭 Plot twists activés</p>}
            {enableEvents && <p>⚡ Événements activés</p>}
          </div>

          {/* Launch */}
          <Button
            size="lg"
            className="w-full"
            disabled={!selectedModel || loading}
            onClick={handleLaunch}
          >
            {loading ? (
              <span className="animate-spin inline-block w-4 h-4 border-2 border-white border-t-transparent rounded-full" />
            ) : (
              <>⚔️ Lancer l'expérience</>
            )}
          </Button>
        </Card>
      </div>
    </div>
  );
}
