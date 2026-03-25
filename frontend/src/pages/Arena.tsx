import { useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { useArenaStore } from "../stores/arenaStore";
import Card from "../components/ui/Card";
import Button from "../components/ui/Button";
import Badge from "../components/ui/Badge";

const AGENT_COLORS: Record<string, string> = {
  Atlas: "#6366f1",
  Lyra: "#22c55e",
  Orion: "#ef4444",
  Nova: "#f59e0b",
  Vega: "#06b6d4",
  Clio: "#ec4899",
  Théo: "#8b5cf6",
};

const PHASE_META: Record<string, { label: string; color: string; icon: string }> = {
  discussion: { label: "Discussion", color: "#6366f1", icon: "💬" },
  reaction: { label: "Réaction", color: "#f59e0b", icon: "⚡" },
  vote: { label: "Vote", color: "#22c55e", icon: "🗳️" },
};

function getAgentColor(name: string): string {
  return AGENT_COLORS[name] || "#888";
}

/** Build a flat list of transcript items (round headers, events, messages) for rendering. */
type TranscriptItem =
  | { kind: "round"; round: number; totalRounds: number }
  | { kind: "event"; data: Record<string, unknown> }
  | { kind: "phase"; phase: string }
  | { kind: "status"; agentId: string; agentName: string; status: string }
  | { kind: "message"; msg: Message }
  | { kind: "vote"; vote: Vote };

import type { Message, Vote, PhaseType } from "../types";

function buildTranscript(events: Record<string, unknown>[]): TranscriptItem[] {
  const items: TranscriptItem[] = [];
  for (const ev of events) {
    switch (ev.type) {
      case "round_start":
        items.push({ kind: "round", round: ev.round as number, totalRounds: (ev.total_rounds as number) || 0 });
        break;
      case "event":
        items.push({ kind: "event", data: ev });
        break;
      case "phase":
        items.push({ kind: "phase", phase: ev.phase as string });
        break;
      case "agent_status":
        items.push({ kind: "status", agentId: ev.agent_id as string, agentName: ev.agent_name as string || ev.agent_id as string, status: ev.status as string });
        break;
      case "message":
        items.push({
          kind: "message",
          msg: {
            agent_id: ev.agent_id as string,
            agent_name: ev.agent_name as string,
            phase: (ev.phase as string) as PhaseType,
            content: ev.content as string,
            timestamp: new Date().toISOString(),
            tokens_used: (ev.tokens as number) ?? 0,
            response_time_ms: (ev.response_time_ms as number) ?? 0,
          },
        });
        break;
      case "vote":
        items.push({
          kind: "vote",
          vote: {
            agent_id: ev.agent_id as string,
            agent_name: ev.agent_name as string,
            target: ev.target as string,
            round_number: 0,
            reasoning: ev.reasoning as string | undefined,
          },
        });
        break;
      // run_start, run_end, round_end — handled by store state, skip in transcript
    }
  }
  return items;
}

export default function Arena() {
  const navigate = useNavigate();
  const { runId, status, currentRound, agents, events, reset } = useArenaStore();
  const transcriptRef = useRef<HTMLDivElement>(null);
  const transcript = buildTranscript(events as Record<string, unknown>[]);

  // Auto-scroll transcript
  useEffect(() => {
    if (transcriptRef.current) {
      transcriptRef.current.scrollTop = transcriptRef.current.scrollHeight;
    }
  }, [transcript.length]);

  const isRunning = status === "running";
  const isComplete = status === "completed" || status === "failed";

  // Extract the latest agent thinking status
  const thinkingAgent = (() => {
    for (let i = events.length - 1; i >= 0; i--) {
      const e = events[i] as Record<string, unknown>;
      if (e.type === "agent_status" && e.status === "thinking") return e.agent_name as string || e.agent_id as string;
      if (e.type === "message") return null; // last event was a message, nobody thinking
    }
    return null;
  })();

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
          {/* ─── Sidebar ─── */}
          <div className="lg:col-span-1 space-y-4">
            {/* Agents */}
            <Card>
              <h2 className="text-sm font-semibold text-arena-muted mb-3">Agents</h2>
              <div className="space-y-2">
                {agents.map((name) => {
                  const isThinking = thinkingAgent === name;
                  return (
                    <div
                      key={name}
                      className={`flex items-center gap-2 px-3 py-2 rounded-lg border transition-all duration-300 ${
                        isThinking
                          ? "bg-arena-accent/10 border-arena-accent/40"
                          : "bg-arena-bg border-arena-border"
                      }`}
                    >
                      <div
                        className={`w-3 h-3 rounded-full shrink-0 ${isThinking ? "animate-pulse" : ""}`}
                        style={{ backgroundColor: getAgentColor(name) }}
                      />
                      <span className="text-sm text-white">{name}</span>
                      {isThinking && (
                        <span className="ml-auto text-[10px] text-arena-accent animate-pulse">💭</span>
                      )}
                    </div>
                  );
                })}
              </div>

              {currentRound > 0 && (
                <div className="mt-4 text-center">
                  <span className="text-xs text-arena-muted">Tour</span>
                  <p className="text-2xl font-bold text-arena-accent-light">{currentRound}</p>
                </div>
              )}
            </Card>

            {/* Event log (sidebar) */}
            {events.some((e) => (e as Record<string, unknown>).type === "event") && (
              <Card>
                <h2 className="text-sm font-semibold text-arena-muted mb-2">📡 Événements</h2>
                <div className="space-y-2 max-h-48 overflow-y-auto">
                  {events
                    .filter((e) => (e as Record<string, unknown>).type === "event")
                    .map((e, i) => {
                      const ev = e as Record<string, unknown>;
                      return (
                        <div key={i} className="text-xs p-2 rounded-lg bg-amber-500/10 border border-amber-500/20 text-amber-300">
                          <span className="font-semibold">Tour {String(ev.round)}</span>
                          {" — "}
                          {String(ev.description || ev.label || ev.name || "Événement")}
                        </div>
                      );
                    })}
                </div>
              </Card>
            )}
          </div>

          {/* ─── Transcript ─── */}
          <Card className="lg:col-span-3">
            <h2 className="text-sm font-semibold text-arena-muted mb-3">Transcript</h2>

            <div
              ref={transcriptRef}
              className="space-y-3 max-h-[65vh] overflow-y-auto pr-2"
            >
              <AnimatePresence initial={false}>
                {transcript.map((item, i) => {
                  if (item.kind === "round") {
                    return (
                      <motion.div
                        key={`round-${item.round}-${i}`}
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        className="flex items-center gap-3 py-2"
                      >
                        <div className="flex-1 h-px bg-arena-border" />
                        <span className="text-xs font-semibold text-arena-accent-light px-3 py-1 rounded-full bg-arena-accent/10 border border-arena-accent/20">
                          ⚔️ Tour {item.round}{item.totalRounds > 0 && ` / ${item.totalRounds}`}
                        </span>
                        <div className="flex-1 h-px bg-arena-border" />
                      </motion.div>
                    );
                  }

                  if (item.kind === "event") {
                    return (
                      <motion.div
                        key={`event-${i}`}
                        initial={{ opacity: 0, scale: 0.95 }}
                        animate={{ opacity: 1, scale: 1 }}
                        className="mx-4 p-3 rounded-lg bg-amber-500/10 border border-amber-500/30 text-amber-300"
                      >
                        <div className="flex items-center gap-2 text-sm font-semibold">
                          <span>⚡</span>
                          <span>{String((item.data as Record<string, unknown>).name || (item.data as Record<string, unknown>).label || "Événement")}</span>
                        </div>
                        {(item.data as Record<string, unknown>).description ? (
                          <p className="text-xs mt-1 text-amber-200/70">
                            {String((item.data as Record<string, unknown>).description)}
                          </p>
                        ) : null}
                      </motion.div>
                    );
                  }

                  if (item.kind === "phase") {
                    const meta = PHASE_META[item.phase] || { label: item.phase, color: "#888", icon: "📋" };
                    return (
                      <motion.div
                        key={`phase-${i}`}
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        className="flex items-center gap-2 py-1"
                      >
                        <span className="text-xs">{meta.icon}</span>
                        <span className="text-xs font-medium" style={{ color: meta.color }}>{meta.label}</span>
                        <div className="flex-1 h-px" style={{ backgroundColor: meta.color, opacity: 0.2 }} />
                      </motion.div>
                    );
                  }

                  if (item.kind === "message") {
                    const { msg } = item;
                    const phaseMeta = PHASE_META[msg.phase] || { label: msg.phase, color: "#888", icon: "📋" };
                    return (
                      <motion.div
                        key={`msg-${i}`}
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
                            <Badge label={`${phaseMeta.icon} ${phaseMeta.label}`} variant="outline" />
                            {msg.response_time_ms > 0 && (
                              <span className="text-[10px] text-arena-muted">{(msg.response_time_ms / 1000).toFixed(1)}s</span>
                            )}
                          </div>
                          <p className="text-sm text-arena-text leading-relaxed whitespace-pre-wrap">
                            {msg.content}
                          </p>
                        </div>
                      </motion.div>
                    );
                  }

                  if (item.kind === "vote") {
                    const { vote } = item;
                    return (
                      <motion.div
                        key={`vote-${i}`}
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        className="flex items-center gap-2 text-sm px-3 py-2 rounded-lg bg-green-500/10 border border-green-500/20"
                      >
                        <span>🗳️</span>
                        <span style={{ color: getAgentColor(vote.agent_name || vote.agent_id) }}>
                          {vote.agent_name || vote.agent_id}
                        </span>
                        <span className="text-arena-muted">→</span>
                        <span className="text-white font-medium">{vote.target}</span>
                        {vote.reasoning && (
                          <span className="text-arena-muted text-xs ml-1">({vote.reasoning})</span>
                        )}
                      </motion.div>
                    );
                  }

                  return null;
                })}
              </AnimatePresence>

              {/* Thinking indicator */}
              {isRunning && thinkingAgent && (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="flex items-center gap-2 text-arena-muted text-xs py-2"
                >
                  <div className="animate-spin w-3 h-3 border border-arena-accent border-t-transparent rounded-full" />
                  <span style={{ color: getAgentColor(thinkingAgent) }}>{thinkingAgent}</span> réfléchit…
                </motion.div>
              )}

              {/* Initial loading */}
              {transcript.length === 0 && isRunning && (
                <div className="text-center py-10 text-arena-muted">
                  <div className="animate-spin inline-block w-6 h-6 border-2 border-arena-accent border-t-transparent rounded-full mb-2" />
                  <p className="text-sm">Initialisation de l'expérience…</p>
                </div>
              )}
            </div>
          </Card>
        </div>
      )}
    </div>
  );
}
