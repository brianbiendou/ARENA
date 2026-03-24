import { useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { useArenaStore } from "../stores/arenaStore.ts";
import Card from "../components/ui/Card.tsx";
import Button from "../components/ui/Button.tsx";
import Badge from "../components/ui/Badge.tsx";

const AGENT_COLORS: Record<string, string> = {
  Atlas: "#6366f1",
  Lyra: "#22c55e",
  Orion: "#ef4444",
  Nova: "#f59e0b",
  Vega: "#06b6d4",
  Clio: "#ec4899",
  Théo: "#8b5cf6",
};

function getAgentColor(name: string): string {
  return AGENT_COLORS[name] || "#888";
}

export default function Arena() {
  const navigate = useNavigate();
  const { runId, status, currentRound, messages, votes, agents, init, reset } = useArenaStore();
  const transcriptRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const unsub = init();
    return () => {
      unsub();
    };
  }, [init]);

  // Auto-scroll transcript
  useEffect(() => {
    if (transcriptRef.current) {
      transcriptRef.current.scrollTop = transcriptRef.current.scrollHeight;
    }
  }, [messages]);

  const isRunning = status === "running";
  const isComplete = status === "completed" || status === "failed";

  return (
    <div className="max-w-6xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-2">
            ⚔️ Arena
            {isRunning && (
              <span className="inline-flex items-center gap-1 text-sm font-normal text-arena-success">
                <span className="w-2 h-2 bg-arena-success rounded-full animate-pulse" />
                En cours
              </span>
            )}
            {isComplete && (
              <Badge
                label={status === "completed" ? "Terminé" : "Erreur"}
                color={status === "completed" ? "#22c55e" : "#ef4444"}
              />
            )}
          </h1>
          {runId && <p className="text-xs text-arena-muted mt-1 font-mono">{runId}</p>}
        </div>

        <div className="flex gap-2">
          {isComplete && runId && (
            <Button variant="secondary" size="sm" onClick={() => navigate(`/analysis/${runId}`)}>
              📊 Analyse
            </Button>
          )}
          <Button variant="ghost" size="sm" onClick={() => { reset(); navigate("/"); }}>
            ← Hub
          </Button>
        </div>
      </div>

      {/* No run */}
      {!runId && !isRunning && (
        <div className="text-center py-20 text-arena-muted">
          <p className="text-lg mb-2">Aucune expérience en cours</p>
          <p className="text-sm">Lancez une expérience depuis le Hub.</p>
          <Button variant="secondary" className="mt-4" onClick={() => navigate("/")}>
            Aller au Hub
          </Button>
        </div>
      )}

      {/* Active run layout */}
      {(runId || isRunning) && (
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-5">
          {/* ─── Agent Circle (sidebar) ─── */}
          <Card className="lg:col-span-1">
            <h2 className="text-sm font-semibold text-arena-muted mb-3">Agents</h2>
            <div className="space-y-2">
              {agents.map((name) => (
                <div
                  key={name}
                  className="flex items-center gap-2 px-3 py-2 rounded-lg bg-arena-bg border border-arena-border"
                >
                  <div
                    className="w-3 h-3 rounded-full"
                    style={{ backgroundColor: getAgentColor(name) }}
                  />
                  <span className="text-sm text-white">{name}</span>
                </div>
              ))}
            </div>

            {currentRound > 0 && (
              <div className="mt-4 text-center">
                <span className="text-xs text-arena-muted">Tour</span>
                <p className="text-2xl font-bold text-arena-accent-light">{currentRound}</p>
              </div>
            )}
          </Card>

          {/* ─── Transcript ─── */}
          <Card className="lg:col-span-3">
            <h2 className="text-sm font-semibold text-arena-muted mb-3">Transcript</h2>

            <div
              ref={transcriptRef}
              className="space-y-3 max-h-[60vh] overflow-y-auto pr-2"
            >
              <AnimatePresence initial={false}>
                {messages.map((msg, i) => (
                  <motion.div
                    key={i}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.2 }}
                    className="flex gap-3 items-start"
                  >
                    <div
                      className="w-2 h-2 mt-2 rounded-full shrink-0"
                      style={{ backgroundColor: getAgentColor(msg.agent_name || msg.agent_id) }}
                    />
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-0.5">
                        <span
                          className="text-sm font-medium"
                          style={{ color: getAgentColor(msg.agent_name || msg.agent_id) }}
                        >
                          {msg.agent_name || msg.agent_id}
                        </span>
                        <Badge label={msg.phase} variant="outline" />
                      </div>
                      <p className="text-sm text-arena-text leading-relaxed whitespace-pre-wrap">
                        {msg.content}
                      </p>
                    </div>
                  </motion.div>
                ))}
              </AnimatePresence>

              {isRunning && messages.length > 0 && (
                <div className="flex items-center gap-2 text-arena-muted text-xs py-2">
                  <div className="animate-spin w-3 h-3 border border-arena-accent border-t-transparent rounded-full" />
                  Un agent réfléchit…
                </div>
              )}

              {messages.length === 0 && isRunning && (
                <div className="text-center py-10 text-arena-muted">
                  <div className="animate-spin inline-block w-6 h-6 border-2 border-arena-accent border-t-transparent rounded-full mb-2" />
                  <p className="text-sm">Initialisation de l'expérience…</p>
                </div>
              )}
            </div>

            {/* Votes section */}
            {votes.length > 0 && (
              <div className="mt-4 pt-4 border-t border-arena-border">
                <h3 className="text-sm font-semibold text-arena-muted mb-2">🗳️ Votes</h3>
                <div className="space-y-1">
                  {votes.map((v, i) => (
                    <div key={i} className="flex items-center gap-2 text-sm">
                      <span style={{ color: getAgentColor(v.agent_name || v.agent_id) }}>
                        {v.agent_name || v.agent_id}
                      </span>
                      <span className="text-arena-muted">→</span>
                      <span className="text-white">{v.target}</span>
                      {v.reasoning && (
                        <span className="text-arena-muted text-xs">({v.reasoning})</span>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </Card>
        </div>
      )}
    </div>
  );
}
