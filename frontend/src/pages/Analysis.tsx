import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { runs as runsApi } from "../services/api.ts";
import Card from "../components/ui/Card.tsx";
import Button from "../components/ui/Button.tsx";
import Badge from "../components/ui/Badge.tsx";
import type { RunResult } from "../types";

export default function Analysis() {
  const { runId } = useParams<{ runId: string }>();
  const navigate = useNavigate();
  const [result, setResult] = useState<RunResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!runId) return;
    setLoading(true);
    runsApi
      .get(runId)
      .then(setResult)
      .catch((e) => setError((e as Error).message))
      .finally(() => setLoading(false));
  }, [runId]);

  if (loading) {
    return (
      <div className="text-center py-20">
        <div className="animate-spin inline-block w-8 h-8 border-2 border-arena-accent border-t-transparent rounded-full" />
      </div>
    );
  }

  if (error || !result) {
    return (
      <div className="text-center py-20 text-arena-danger">
        <p>Erreur : {error || "Run introuvable"}</p>
        <Button variant="ghost" className="mt-4" onClick={() => navigate("/")}>
          Retour au Hub
        </Button>
      </div>
    );
  }

  const { config, rounds, metrics, agents } = result;

  return (
    <div className="max-w-6xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <Button variant="ghost" size="sm" onClick={() => navigate("/")}>
            ← Hub
          </Button>
          <h1 className="text-2xl font-bold text-white mt-2">📊 Analyse</h1>
          <p className="text-xs text-arena-muted font-mono mt-1">{result.run_id}</p>
        </div>

        <div className="flex gap-2">
          <a
            href={runsApi.exportUrl(result.run_id, "json")}
            target="_blank"
            rel="noreferrer"
          >
            <Button variant="secondary" size="sm">JSON</Button>
          </a>
          <a
            href={runsApi.exportUrl(result.run_id, "csv")}
            target="_blank"
            rel="noreferrer"
          >
            <Button variant="secondary" size="sm">CSV</Button>
          </a>
          <a
            href={runsApi.exportUrl(result.run_id, "md")}
            target="_blank"
            rel="noreferrer"
          >
            <Button variant="secondary" size="sm">Markdown</Button>
          </a>
        </div>
      </div>

      {/* Metrics Overview */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        {[
          { label: "Status", value: result.status, color: result.status === "completed" ? "#22c55e" : "#ef4444" },
          { label: "Tours", value: `${metrics?.rounds_completed || rounds.length}` },
          { label: "Messages", value: `${metrics?.total_messages || 0}` },
          { label: "Tokens", value: `${metrics?.total_tokens || 0}` },
        ].map((m) => (
          <Card key={m.label}>
            <p className="text-xs text-arena-muted">{m.label}</p>
            <p className="text-xl font-bold text-white mt-1" style={m.color ? { color: m.color } : {}}>
              {m.value}
            </p>
          </Card>
        ))}
      </div>

      {metrics && (
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-8">
          <Card>
            <p className="text-xs text-arena-muted">Temps moyen de réponse</p>
            <p className="text-lg font-bold text-white">{(metrics.avg_response_time_ms / 1000).toFixed(1)}s</p>
          </Card>
          <Card>
            <p className="text-xs text-arena-muted">Durée totale</p>
            <p className="text-lg font-bold text-white">{metrics.duration_s.toFixed(0)}s</p>
          </Card>
          {metrics.consensus_reached !== null && metrics.consensus_reached !== undefined && (
            <Card>
              <p className="text-xs text-arena-muted">Consensus</p>
              <p className={`text-lg font-bold ${metrics.consensus_reached ? "text-arena-success" : "text-arena-warning"}`}>
                {metrics.consensus_reached ? "Oui ✓" : "Non ✗"}
              </p>
            </Card>
          )}
        </div>
      )}

      {/* Agent Metrics */}
      {metrics && Object.keys(metrics.agent_metrics).length > 0 && (
        <Card className="mb-8">
          <h2 className="text-lg font-semibold text-white mb-4">🤖 Performance par Agent</h2>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-arena-border text-arena-muted text-left">
                  <th className="pb-2 pr-4">Agent</th>
                  <th className="pb-2 pr-4">Tokens</th>
                  <th className="pb-2 pr-4">Messages</th>
                </tr>
              </thead>
              <tbody>
                {Object.entries(metrics.agent_metrics).map(([id, data]) => (
                  <tr key={id} className="border-b border-arena-border/50">
                    <td className="py-2 pr-4 text-white">{data.name || id}</td>
                    <td className="py-2 pr-4 font-mono">{data.tokens_used || 0}</td>
                    <td className="py-2 pr-4 font-mono">{data.messages_sent || 0}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Card>
      )}

      {/* Rounds Transcript */}
      <Card>
        <h2 className="text-lg font-semibold text-white mb-4">📜 Transcript complet</h2>
        <div className="space-y-6">
          {rounds.map((round) => (
            <div key={round.round_number}>
              <h3 className="text-sm font-semibold text-arena-accent-light mb-2">
                Tour {round.round_number}
                {round.instruction && (
                  <span className="text-xs text-arena-muted font-normal ml-2">— {round.instruction}</span>
                )}
              </h3>
              <div className="space-y-2 pl-4 border-l-2 border-arena-border">
                {round.messages.map((msg, i) => {
                  const agent = agents.find((a) => a.id === msg.agent_id);
                  return (
                    <div key={i} className="text-sm">
                      <span
                        className="font-medium"
                        style={{ color: agent?.color || "#888" }}
                      >
                        {agent?.name || msg.agent_id}
                      </span>
                      <Badge label={msg.phase} variant="outline" />
                      <p className="text-arena-text mt-0.5 whitespace-pre-wrap">{msg.content}</p>
                    </div>
                  );
                })}
                {round.votes.length > 0 && (
                  <div className="mt-2 pt-2 border-t border-arena-border/50">
                    <p className="text-xs text-arena-muted mb-1">Votes :</p>
                    {round.votes.map((v, i) => {
                      const agent = agents.find((a) => a.id === v.agent_id);
                      return (
                        <p key={i} className="text-xs">
                          <span style={{ color: agent?.color || "#888" }}>
                            {agent?.name || v.agent_id}
                          </span>
                          {" → "}
                          <span className="text-white">{v.target}</span>
                        </p>
                      );
                    })}
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}
