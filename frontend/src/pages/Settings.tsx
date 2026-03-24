/* ────────────────────────────────────────────
   Settings page — providers, models, defaults
   ──────────────────────────────────────────── */

import { useEffect, useState, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { settings as settingsApi, providers as providersApi } from "../services/api";
import type { AppSettings, ProviderConfig, ProviderType, ModelInfo } from "../types";
import Button from "../components/ui/Button";

const PROVIDER_META: Record<ProviderType, { label: string; icon: string; color: string; desc: string }> = {
  ollama:     { label: "Ollama",     icon: "🦙", color: "#22c55e", desc: "Modèles locaux — rapide et privé" },
  lm_studio:  { label: "LM Studio",  icon: "🧪", color: "#a855f7", desc: "Modèles locaux via LM Studio" },
  openrouter: { label: "OpenRouter", icon: "🌐", color: "#3b82f6", desc: "Accès cloud — centaines de modèles" },
};

const PROVIDER_ORDER: ProviderType[] = ["ollama", "lm_studio", "openrouter"];

export default function Settings() {
  const [appSettings, setAppSettings] = useState<AppSettings | null>(null);
  const [models, setModels] = useState<Record<string, ModelInfo[]>>({});
  const [loadingModels, setLoadingModels] = useState<Record<string, boolean>>({});
  const [testResults, setTestResults] = useState<Record<string, boolean | null>>({});
  const [saving, setSaving] = useState(false);
  const [dirty, setDirty] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [expandedProvider, setExpandedProvider] = useState<ProviderType | null>(null);

  useEffect(() => {
    settingsApi.get().then(setAppSettings).catch((e) => setError(e.message));
  }, []);

  const loadModels = useCallback(async (type: ProviderType) => {
    setLoadingModels((p) => ({ ...p, [type]: true }));
    try {
      const data = await providersApi.models(type);
      setModels((p) => ({ ...p, [type]: data }));
    } catch {
      setModels((p) => ({ ...p, [type]: [] }));
    }
    setLoadingModels((p) => ({ ...p, [type]: false }));
  }, []);

  // Auto-load models for enabled providers
  useEffect(() => {
    if (!appSettings) return;
    for (const type of PROVIDER_ORDER) {
      const cfg = appSettings.providers[type];
      if (cfg?.enabled && !models[type]) loadModels(type);
    }
  }, [appSettings, loadModels]); // eslint-disable-line react-hooks/exhaustive-deps

  const updateProvider = (type: ProviderType, patch: Partial<ProviderConfig>) => {
    if (!appSettings) return;
    setAppSettings({
      ...appSettings,
      providers: {
        ...appSettings.providers,
        [type]: { ...appSettings.providers[type], ...patch },
      },
    });
    setDirty(true);
  };

  const updateDefaults = (key: string, val: number) => {
    if (!appSettings) return;
    setAppSettings({
      ...appSettings,
      llm_defaults: { ...appSettings.llm_defaults, [key]: val },
    });
    setDirty(true);
  };

  const handleSave = async () => {
    if (!appSettings) return;
    setSaving(true);
    try {
      const updated = await settingsApi.update(appSettings);
      setAppSettings(updated);
      setDirty(false);
      for (const type of PROVIDER_ORDER) {
        if (updated.providers[type]?.enabled) loadModels(type);
      }
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Erreur lors de la sauvegarde");
    }
    setSaving(false);
  };

  const handleTest = async (type: ProviderType) => {
    setTestResults((p) => ({ ...p, [type]: null }));
    try {
      const result = await providersApi.test(type);
      setTestResults((p) => ({ ...p, [type]: result.connected }));
    } catch {
      setTestResults((p) => ({ ...p, [type]: false }));
    }
  };

  if (!appSettings) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="flex flex-col items-center gap-4">
          <div className="animate-spin rounded-full h-10 w-10 border-2 border-arena-accent border-t-transparent" />
          <span className="text-arena-muted text-sm">Chargement des paramètres…</span>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto space-y-10 pb-24">
      {/* ─── Header ─── */}
      <div className="relative">
        <div className="absolute -top-4 -left-4 w-32 h-32 bg-arena-accent/5 rounded-full blur-3xl" />
        <div className="relative flex items-end justify-between">
          <div>
            <h1 className="text-4xl font-bold text-white tracking-tight flex items-center gap-3">
              <span className="text-3xl opacity-80">⚙️</span>
              Configuration
            </h1>
            <p className="text-arena-muted mt-2 text-lg">
              Providers LLM, modèles disponibles et paramètres de génération
            </p>
          </div>
          <motion.div whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}>
            <Button variant={dirty ? "primary" : "secondary"} onClick={handleSave} disabled={!dirty || saving}>
              {saving ? (
                <span className="flex items-center gap-2">
                  <span className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent" />
                  Sauvegarde…
                </span>
              ) : dirty ? "💾 Sauvegarder" : "✓ À jour"}
            </Button>
          </motion.div>
        </div>
      </div>

      {/* ─── Error ─── */}
      <AnimatePresence>
        {error && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="flex items-center justify-between bg-red-500/10 border border-red-500/20 text-red-400 rounded-xl px-5 py-3"
          >
            <span className="text-sm">{error}</span>
            <button onClick={() => setError(null)} className="text-red-400/60 hover:text-red-400 text-lg">✕</button>
          </motion.div>
        )}
      </AnimatePresence>

      {/* ─── Providers ─── */}
      <section>
        <h2 className="text-sm font-semibold uppercase tracking-widest text-arena-muted mb-4">
          Providers LLM
        </h2>

        <div className="grid gap-4">
          {PROVIDER_ORDER.map((type) => {
            const cfg = appSettings.providers[type];
            const meta = PROVIDER_META[type];
            const providerModels = models[type] || [];
            const isLoading = loadingModels[type] || false;
            const testResult = testResults[type];
            const isExpanded = expandedProvider === type;

            return (
              <motion.div
                key={type}
                layout
                className="rounded-2xl border border-arena-border bg-arena-surface overflow-hidden"
                style={{ borderLeftColor: cfg.enabled ? meta.color : undefined, borderLeftWidth: cfg.enabled ? 3 : 1 }}
              >
                {/* Provider header */}
                <div
                  className="flex items-center justify-between px-6 py-4 cursor-pointer hover:bg-white/[0.02] transition-colors"
                  onClick={() => setExpandedProvider(isExpanded ? null : type)}
                >
                  <div className="flex items-center gap-4">
                    <span className="text-3xl">{meta.icon}</span>
                    <div>
                      <div className="flex items-center gap-3">
                        <h3 className="text-lg font-semibold text-white">{meta.label}</h3>
                        {cfg.enabled && providerModels.length > 0 && (
                          <span className="px-2 py-0.5 text-xs rounded-full font-medium"
                            style={{ backgroundColor: `${meta.color}20`, color: meta.color }}>
                            {providerModels.length} modèle{providerModels.length > 1 ? "s" : ""}
                          </span>
                        )}
                        {testResult === true && (
                          <span className="px-2 py-0.5 text-xs rounded-full bg-green-500/15 text-green-400 font-medium">
                            ✓ Connecté
                          </span>
                        )}
                        {testResult === false && (
                          <span className="px-2 py-0.5 text-xs rounded-full bg-red-500/15 text-red-400 font-medium">
                            ✗ Hors ligne
                          </span>
                        )}
                      </div>
                      <p className="text-sm text-arena-muted mt-0.5">{meta.desc}</p>
                    </div>
                  </div>

                  <div className="flex items-center gap-4" onClick={(e) => e.stopPropagation()}>
                    {cfg.enabled && (
                      <button
                        onClick={() => handleTest(type)}
                        className="text-sm text-arena-muted hover:text-white transition-colors px-3 py-1.5 rounded-lg hover:bg-white/5"
                      >
                        🔌 Tester
                      </button>
                    )}
                    {/* Toggle */}
                    <label className="relative inline-flex cursor-pointer">
                      <input
                        type="checkbox"
                        className="sr-only peer"
                        checked={cfg.enabled}
                        onChange={(e) => updateProvider(type, { enabled: e.target.checked })}
                      />
                      <div className="w-11 h-6 rounded-full transition-colors duration-200 bg-arena-border peer-checked:bg-arena-accent peer-focus:ring-2 peer-focus:ring-arena-accent/30">
                        <div className={`absolute top-0.5 left-0.5 w-5 h-5 rounded-full bg-white shadow transition-transform duration-200 ${cfg.enabled ? "translate-x-5" : ""}`} />
                      </div>
                    </label>
                    {/* Expand chevron */}
                    <motion.span
                      animate={{ rotate: isExpanded ? 180 : 0 }}
                      className="text-arena-muted text-lg"
                    >
                      ▾
                    </motion.span>
                  </div>
                </div>

                {/* Expanded content */}
                <AnimatePresence>
                  {isExpanded && cfg.enabled && (
                    <motion.div
                      initial={{ height: 0, opacity: 0 }}
                      animate={{ height: "auto", opacity: 1 }}
                      exit={{ height: 0, opacity: 0 }}
                      transition={{ duration: 0.2 }}
                      className="overflow-hidden"
                    >
                      <div className="px-6 pb-5 space-y-5 border-t border-arena-border/50 pt-4">
                        {/* Config row */}
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                          <div>
                            <label className="block text-xs font-medium text-arena-muted uppercase tracking-wider mb-1.5">
                              Endpoint
                            </label>
                            <input
                              type="text"
                              value={cfg.endpoint}
                              onChange={(e) => updateProvider(type, { endpoint: e.target.value })}
                              className="w-full px-4 py-2.5 bg-arena-bg/80 border border-arena-border/60 rounded-xl text-white text-sm focus:outline-none focus:border-arena-accent/60 focus:ring-1 focus:ring-arena-accent/20 transition-all"
                            />
                          </div>
                          {type === "openrouter" && (
                            <div>
                              <label className="block text-xs font-medium text-arena-muted uppercase tracking-wider mb-1.5">
                                API Key
                              </label>
                              <input
                                type="password"
                                value={cfg.api_key || ""}
                                onChange={(e) => updateProvider(type, { api_key: e.target.value })}
                                placeholder="sk-or-..."
                                className="w-full px-4 py-2.5 bg-arena-bg/80 border border-arena-border/60 rounded-xl text-white text-sm focus:outline-none focus:border-arena-accent/60 focus:ring-1 focus:ring-arena-accent/20 transition-all font-mono"
                              />
                            </div>
                          )}
                        </div>

                        {/* Models */}
                        <div>
                          <div className="flex items-center justify-between mb-3">
                            <label className="text-xs font-medium text-arena-muted uppercase tracking-wider">
                              Modèles disponibles
                            </label>
                            <button
                              onClick={() => loadModels(type)}
                              className="text-xs text-arena-accent hover:text-arena-accent-light transition-colors flex items-center gap-1"
                            >
                              <span className={isLoading ? "animate-spin" : ""}>↻</span> Rafraîchir
                            </button>
                          </div>

                          {isLoading ? (
                            <div className="flex items-center justify-center gap-3 text-arena-muted text-sm py-8 bg-arena-bg/30 rounded-xl">
                              <div className="animate-spin rounded-full h-5 w-5 border-2 border-arena-accent border-t-transparent" />
                              Chargement…
                            </div>
                          ) : providerModels.length === 0 ? (
                            <div className="text-center text-sm text-arena-muted py-8 bg-arena-bg/30 rounded-xl border border-dashed border-arena-border/50">
                              <span className="text-2xl block mb-2">🔍</span>
                              Aucun modèle trouvé
                            </div>
                          ) : (
                            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2">
                              {providerModels.map((m) => (
                                <div
                                  key={m.id}
                                  className="group flex items-center gap-3 px-4 py-3 bg-arena-bg/40 rounded-xl border border-arena-border/30 hover:border-arena-accent/20 hover:bg-arena-bg/60 transition-all"
                                >
                                  <div className="w-2 h-2 rounded-full shrink-0" style={{ backgroundColor: meta.color }} />
                                  <div className="min-w-0 flex-1">
                                    <span className="text-sm text-white font-medium truncate block">
                                      {m.name || m.id}
                                    </span>
                                    {m.context_length && (
                                      <span className="text-xs text-arena-muted">
                                        {(m.context_length / 1024).toFixed(0)}K ctx
                                      </span>
                                    )}
                                  </div>
                                </div>
                              ))}
                            </div>
                          )}
                        </div>
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </motion.div>
            );
          })}
        </div>
      </section>

      {/* ─── LLM Defaults ─── */}
      <section>
        <h2 className="text-sm font-semibold uppercase tracking-widest text-arena-muted mb-4">
          Paramètres de génération
        </h2>

        <div className="rounded-2xl border border-arena-border bg-arena-surface p-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-x-10 gap-y-6">
            {[
              { key: "temperature", label: "🌡️ Température", min: 0, max: 2, step: 0.1,
                hint: "Créativité des réponses. Bas = factuel, Haut = créatif" },
              { key: "top_p", label: "🎯 Top P", min: 0, max: 1, step: 0.05,
                hint: "Diversité du vocabulaire" },
              { key: "max_tokens", label: "📝 Max Tokens", min: 100, max: 4096, step: 50,
                hint: "Longueur maximale des réponses" },
              { key: "response_timeout_s", label: "⏱️ Timeout", min: 10, max: 300, step: 5,
                hint: "Temps max d'attente (secondes)" },
            ].map(({ key, label, min, max, step, hint }) => {
              const val = appSettings.llm_defaults[key as keyof typeof appSettings.llm_defaults];
              return (
                <div key={key} className="space-y-2">
                  <div className="flex justify-between items-baseline">
                    <label className="text-sm text-white font-medium">{label}</label>
                    <span className="text-arena-accent font-mono text-sm font-semibold">{val}</span>
                  </div>
                  <input
                    type="range"
                    min={min}
                    max={max}
                    step={step}
                    value={val}
                    onChange={(e) => updateDefaults(key, Number(e.target.value))}
                    className="w-full h-1.5 rounded-full appearance-none bg-arena-border accent-arena-accent cursor-pointer"
                  />
                  <p className="text-xs text-arena-muted">{hint}</p>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* ─── General ─── */}
      <section>
        <h2 className="text-sm font-semibold uppercase tracking-widest text-arena-muted mb-4">
          Général
        </h2>

        <div className="rounded-2xl border border-arena-border bg-arena-surface divide-y divide-arena-border/50">
          {/* Debug */}
          <div className="flex items-center justify-between px-6 py-4">
            <div>
              <p className="text-sm text-white font-medium">🐛 Debug logging</p>
              <p className="text-xs text-arena-muted mt-0.5">Logs détaillés côté backend</p>
            </div>
            <label className="relative inline-flex cursor-pointer">
              <input
                type="checkbox"
                className="sr-only peer"
                checked={appSettings.debug_logging}
                onChange={(e) => {
                  setAppSettings({ ...appSettings, debug_logging: e.target.checked });
                  setDirty(true);
                }}
              />
              <div className="w-11 h-6 rounded-full transition-colors duration-200 bg-arena-border peer-checked:bg-arena-accent">
                <div className={`absolute top-0.5 left-0.5 w-5 h-5 rounded-full bg-white shadow transition-transform duration-200 ${appSettings.debug_logging ? "translate-x-5" : ""}`} />
              </div>
            </label>
          </div>

          {/* Fallback */}
          <div className="flex items-center justify-between px-6 py-4">
            <div>
              <p className="text-sm text-white font-medium">🔄 Stratégie de fallback</p>
              <p className="text-xs text-arena-muted mt-0.5">Que faire si un modèle ne répond pas</p>
            </div>
            <select
              value={appSettings.fallback_strategy}
              onChange={(e) => {
                setAppSettings({ ...appSettings, fallback_strategy: e.target.value as AppSettings["fallback_strategy"] });
                setDirty(true);
              }}
              className="px-4 py-2 bg-arena-bg/80 border border-arena-border/60 rounded-xl text-white text-sm focus:outline-none focus:border-arena-accent/60 cursor-pointer"
            >
              <option value="stop">🛑 Stop</option>
              <option value="replace">🔄 Remplacer</option>
              <option value="ignore">⏭️ Ignorer</option>
            </select>
          </div>
        </div>
      </section>

      {/* ─── Floating save bar ─── */}
      <AnimatePresence>
        {dirty && (
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 30 }}
            className="fixed bottom-8 left-1/2 -translate-x-1/2 bg-arena-surface/95 backdrop-blur-lg border border-arena-accent/30 rounded-2xl px-8 py-4 shadow-2xl shadow-black/30 flex items-center gap-6 z-50"
          >
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-arena-warning animate-pulse" />
              <span className="text-sm text-white">Modifications non sauvegardées</span>
            </div>
            <Button variant="primary" size="sm" onClick={handleSave} disabled={saving}>
              {saving ? "Sauvegarde…" : "💾 Sauvegarder"}
            </Button>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
