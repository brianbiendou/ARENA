import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { useExperimentStore } from "../stores/experimentStore.ts";
import Card from "../components/ui/Card.tsx";
import type { ExperimentDefinition } from "../types";

function ExperimentCard({ exp }: { exp: ExperimentDefinition }) {
  const navigate = useNavigate();

  return (
    <motion.div
      whileHover={{ scale: 1.02, y: -4 }}
      transition={{ type: "spring", stiffness: 300, damping: 20 }}
    >
      <Card
        hover
        onClick={() => navigate(`/lobby/${exp.id}`)}
        className="h-full"
      >
        <div className="flex items-start gap-3 mb-3">
          <span className="text-3xl">{exp.icon}</span>
          <div className="flex-1 min-w-0">
            <h3 className="font-bold text-white truncate">{exp.display_name}</h3>
            <p className="text-xs text-arena-muted mt-0.5">{exp.tagline}</p>
          </div>
        </div>

        <p className="text-sm text-arena-muted leading-relaxed mb-4 line-clamp-3">
          {exp.description}
        </p>

        <div className="flex items-center gap-3 text-xs text-arena-muted">
          <span>👥 {exp.min_agents}-{exp.max_agents}</span>
          <span>🔄 {exp.min_rounds}-{exp.max_rounds} tours</span>
          <span>🎭 {exp.scenarios.length} scénarios</span>
        </div>

        {/* Color accent bar */}
        <div
          className="mt-4 h-1 rounded-full opacity-60"
          style={{ background: `linear-gradient(to right, ${exp.color_primary}, ${exp.color_secondary})` }}
        />
      </Card>
    </motion.div>
  );
}

export default function Hub() {
  const { experiments, loading, error, fetch } = useExperimentStore();

  useEffect(() => {
    fetch();
  }, [fetch]);

  return (
    <div className="max-w-6xl mx-auto">
      {/* Hero */}
      <div className="text-center mb-10">
        <h1 className="text-4xl font-bold tracking-tight">
          <span className="text-arena-accent-light">⚔️ ARENA</span>
        </h1>
        <p className="text-arena-muted mt-2 text-lg">
          Plateforme expérimentale multi-agents
        </p>
        <p className="text-arena-muted/60 mt-1 text-sm">
          Choisissez une expérience pour commencer
        </p>
      </div>

      {/* Loading / Error */}
      {loading && (
        <div className="text-center text-arena-muted py-20">
          <div className="animate-spin inline-block w-8 h-8 border-2 border-arena-accent border-t-transparent rounded-full mb-3" />
          <p>Chargement des expériences…</p>
        </div>
      )}

      {error && (
        <div className="text-center text-arena-danger py-20">
          <p className="text-lg mb-2">Erreur de connexion</p>
          <p className="text-sm text-arena-muted">{error}</p>
          <p className="text-xs text-arena-muted mt-4">
            Assurez-vous que le backend tourne sur <code>localhost:8000</code>
          </p>
        </div>
      )}

      {/* Experiment Grid */}
      {!loading && !error && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {experiments.map((exp, i) => (
            <motion.div
              key={exp.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.05 }}
            >
              <ExperimentCard exp={exp} />
            </motion.div>
          ))}
        </div>
      )}
    </div>
  );
}
