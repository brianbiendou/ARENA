import { useEffect, useState, useMemo } from "react";
import { useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { runs as runsApi } from "../services/api.ts";
import Card from "../components/ui/Card.tsx";
import Button from "../components/ui/Button.tsx";
import Badge from "../components/ui/Badge.tsx";
import type { RunSummary, RunStatus } from "../types";

const STATUS_CONFIG: Record<RunStatus, { label: string; color: string }> = {
  pending: { label: "En attente", color: "#f59e0b" },
  running: { label: "En cours", color: "#06b6d4" },
  completed: { label: "Terminé", color: "#22c55e" },
  failed: { label: "Erreur", color: "#ef4444" },
  cancelled: { label: "Annulé", color: "#888" },
};

const EXPERIMENT_ICONS: Record<string, string> = {
  budget_groupe: "💰",
  conseil_crise: "🏛️",
  traitre_invisible: "🎭",
  enquete_collective: "🔍",
  negociation_ressources: "⚖️",
  pouvoir_tourne: "👑",
  information_fragmentee: "🧩",
  repartition_priorites: "📊",
  construction_regle: "📜",
  loi_du_groupe: "⚖️",
};

type SortKey = "date" | "experiment" | "status";

export default function History() {
  const navigate = useNavigate();
  const [runsList, setRunsList] = useState<RunSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [sortBy, setSortBy] = useState<SortKey>("date");
  const [filterExp, setFilterExp] = useState<string>("all");
  const [filterStatus, setFilterStatus] = useState<string>("all");
  const [confirmDelete, setConfirmDelete] = useState<string | null>(null);

  const fetchRuns = () => {
    setLoading(true);
    runsApi
      .list()
      .then(setRunsList)
      .catch((e) => setError((e as Error).message))
      .finally(() => setLoading(false));
  };

  useEffect(() => { fetchRuns(); }, []);

  const handleDelete = async (runId: string) => {
    try {
      await runsApi.delete(runId);
      setRunsList((prev) => prev.filter((r) => r.run_id !== runId));
      setConfirmDelete(null);
    } catch (e) {
      console.error("Delete failed:", e);
    }
  };

  // Unique experiments for filter
  const experimentOptions = useMemo(() => {
    const set = new Set(runsList.map((r) => r.experiment_id));
    return Array.from(set).sort();
  }, [runsList]);

  // Filtered & sorted
  const sortedRuns = useMemo(() => {
    let filtered = [...runsList];
    if (filterExp !== "all") filtered = filtered.filter((r) => r.experiment_id === filterExp);
    if (filterStatus !== "all") filtered = filtered.filter((r) => r.status === filterStatus);

    filtered.sort((a, b) => {
      if (sortBy === "date") return new Date(b.created_at).getTime() - new Date(a.created_at).getTime();
      if (sortBy === "experiment") return a.experiment_id.localeCompare(b.experiment_id);
      return a.status.localeCompare(b.status);
    });
    return filtered;
  }, [runsList, sortBy, filterExp, filterStatus]);

  // Group by experiment
  const grouped = useMemo(() => {
    const map = new Map<string, RunSummary[]>();
    for (const run of sortedRuns) {
      const key = run.experiment_id;
      if (!map.has(key)) map.set(key, []);
      map.get(key)!.push(run);
    }
    return map;
  }, [sortedRuns]);

  const formatDate = (iso: string) => {
    const d = new Date(iso);
    return d.toLocaleDateString("fr-FR", { day: "2-digit", month: "short", year: "numeric" })
      + " " + d.toLocaleTimeString("fr-FR", { hour: "2-digit", minute: "2-digit" });
  };

  const formatDuration = (s?: number) => {
    if (!s) return "—";
    if (s < 60) return `${Math.round(s)}s`;
    return `${Math.floor(s / 60)}m ${Math.round(s % 60)}s`;
  };

  if (loading) {
    return (
      <div className="text-center py-20">
        <div className="animate-spin inline-block w-8 h-8 border-2 border-arena-accent border-t-transparent rounded-full" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-20 text-arena-danger">
        <p className="text-lg mb-2">Erreur de chargement</p>
        <p className="text-sm text-arena-muted">{error}</p>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-white">📜 Historique des parties</h1>
          <p className="text-sm text-arena-muted mt-1">
            {runsList.length} partie{runsList.length !== 1 ? "s" : ""} enregistrée{runsList.length !== 1 ? "s" : ""}
          </p>
        </div>
        <Button variant="secondary" size="sm" onClick={fetchRuns}>
          🔄 Rafraîchir
        </Button>
      </div>

      {/* Filters */}
      {runsList.length > 0 && (
        <div className="flex flex-wrap items-center gap-3 mb-6">
          {/* Sort */}
          <div className="flex items-center gap-2">
            <span className="text-xs text-arena-muted">Trier :</span>
            <div className="flex rounded-lg bg-arena-bg/80 p-0.5">
              {([["date", "📅 Date"], ["experiment", "🧪 Jeu"], ["status", "📊 Status"]] as [SortKey, string][]).map(([key, label]) => (
                <button
                  key={key}
                  onClick={() => setSortBy(key)}
                  className={`text-xs px-2.5 py-1.5 rounded-md transition-all ${
                    sortBy === key ? "bg-arena-accent text-white" : "text-arena-muted hover:text-white"
                  }`}
                >
                  {label}
                </button>
              ))}
            </div>
          </div>

          {/* Filter experiment */}
          <select
            title="Filtrer par expérience"
            value={filterExp}
            onChange={(e) => setFilterExp(e.target.value)}
            className="text-xs px-3 py-1.5 rounded-lg bg-arena-bg border border-arena-border text-arena-text focus:border-arena-accent focus:outline-none"
          >
            <option value="all">Toutes les expériences</option>
            {experimentOptions.map((id) => (
              <option key={id} value={id}>{EXPERIMENT_ICONS[id] || "🧪"} {id.replace(/_/g, " ")}</option>
            ))}
          </select>

          {/* Filter status */}
          <select
            title="Filtrer par statut"
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value)}
            className="text-xs px-3 py-1.5 rounded-lg bg-arena-bg border border-arena-border text-arena-text focus:border-arena-accent focus:outline-none"
          >
            <option value="all">Tous les statuts</option>
            {Object.entries(STATUS_CONFIG).map(([key, cfg]) => (
              <option key={key} value={key}>{cfg.label}</option>
            ))}
          </select>

          {(filterExp !== "all" || filterStatus !== "all") && (
            <button
              onClick={() => { setFilterExp("all"); setFilterStatus("all"); }}
              className="text-xs text-arena-accent hover:text-arena-accent-light transition-colors"
            >
              ✕ Réinitialiser
            </button>
          )}
        </div>
      )}

      {/* Empty state */}
      {runsList.length === 0 && (
        <div className="text-center py-20 text-arena-muted">
          <p className="text-4xl mb-4">🏟️</p>
          <p className="text-lg mb-2">Aucune partie jouée</p>
          <p className="text-sm mb-6">Lancez votre première expérience depuis le Hub !</p>
          <Button onClick={() => navigate("/")}>🏠 Aller au Hub</Button>
        </div>
      )}

      {/* No results after filter */}
      {runsList.length > 0 && sortedRuns.length === 0 && (
        <div className="text-center py-16 text-arena-muted">
          <p className="text-lg">Aucune partie ne correspond aux filtres.</p>
        </div>
      )}

      {/* Grouped view (when sorted by experiment) or flat list */}
      {sortBy === "experiment" ? (
        <div className="space-y-8">
          {Array.from(grouped.entries()).map(([expId, expRuns]) => (
            <div key={expId}>
              <div className="flex items-center gap-2 mb-3">
                <span className="text-xl">{EXPERIMENT_ICONS[expId] || "🧪"}</span>
                <h2 className="text-lg font-semibold text-white capitalize">{expId.replace(/_/g, " ")}</h2>
                <span className="text-xs text-arena-muted bg-arena-bg/60 px-2 py-0.5 rounded-full">
                  {expRuns.length}
                </span>
              </div>
              <div className="space-y-2">
                {expRuns.map((run) => (
                  <RunRow
                    key={run.run_id}
                    run={run}
                    onNavigate={() => navigate(`/analysis/${run.run_id}`)}
                    onDelete={() => confirmDelete === run.run_id ? handleDelete(run.run_id) : setConfirmDelete(run.run_id)}
                    isConfirmingDelete={confirmDelete === run.run_id}
                    onCancelDelete={() => setConfirmDelete(null)}
                    formatDate={formatDate}
                    formatDuration={formatDuration}
                    showExperiment={false}
                  />
                ))}
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="space-y-2">
          <AnimatePresence>
            {sortedRuns.map((run) => (
              <RunRow
                key={run.run_id}
                run={run}
                onNavigate={() => navigate(`/analysis/${run.run_id}`)}
                onDelete={() => confirmDelete === run.run_id ? handleDelete(run.run_id) : setConfirmDelete(run.run_id)}
                isConfirmingDelete={confirmDelete === run.run_id}
                onCancelDelete={() => setConfirmDelete(null)}
                formatDate={formatDate}
                formatDuration={formatDuration}
                showExperiment={true}
              />
            ))}
          </AnimatePresence>
        </div>
      )}
    </div>
  );
}

/* ─── Run Row Component ─── */
function RunRow({ run, onNavigate, onDelete, isConfirmingDelete, onCancelDelete, formatDate, formatDuration, showExperiment }: {
  run: RunSummary;
  onNavigate: () => void;
  onDelete: () => void;
  isConfirmingDelete: boolean;
  onCancelDelete: () => void;
  formatDate: (iso: string) => string;
  formatDuration: (s?: number) => string;
  showExperiment: boolean;
}) {
  const status = STATUS_CONFIG[run.status] || STATUS_CONFIG.pending;

  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, x: -20 }}
      layout
    >
      <Card hover onClick={onNavigate} className="!p-4">
        <div className="flex items-center gap-4">
          {/* Experiment icon */}
          {showExperiment && (
            <span className="text-2xl shrink-0">{EXPERIMENT_ICONS[run.experiment_id] || "🧪"}</span>
          )}

          {/* Info */}
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2 mb-1">
              {showExperiment && (
                <span className="text-sm font-semibold text-white capitalize truncate">
                  {run.experiment_name || run.experiment_id.replace(/_/g, " ")}
                </span>
              )}
              <Badge label={status.label} color={status.color} />
              {run.consensus_reached !== undefined && run.consensus_reached !== null && (
                <span className={`text-xs ${run.consensus_reached ? "text-arena-success" : "text-arena-warning"}`}>
                  {run.consensus_reached ? "✓ Consensus" : "✗ Pas de consensus"}
                </span>
              )}
            </div>

            <div className="flex items-center gap-4 text-xs text-arena-muted">
              <span>📅 {formatDate(run.created_at)}</span>
              <span>👥 {run.agent_count} agents</span>
              <span>🔄 {run.rounds_completed}/{run.total_rounds} tours</span>
              <span>⏱️ {formatDuration(run.duration_s)}</span>
            </div>

            <p className="text-xs text-arena-muted/60 font-mono mt-1 truncate">
              {run.run_id}
            </p>
          </div>

          {/* Actions */}
          <div className="flex items-center gap-2 shrink-0" onClick={(e) => e.stopPropagation()}>
            <Button variant="secondary" size="sm" onClick={onNavigate}>
              📊 Analyse
            </Button>

            {isConfirmingDelete ? (
              <div className="flex items-center gap-1">
                <Button variant="danger" size="sm" onClick={onDelete}>
                  Confirmer
                </Button>
                <Button variant="ghost" size="sm" onClick={onCancelDelete}>
                  ✕
                </Button>
              </div>
            ) : (
              <Button variant="ghost" size="sm" onClick={onDelete}>
                🗑️
              </Button>
            )}
          </div>
        </div>
      </Card>
    </motion.div>
  );
}
