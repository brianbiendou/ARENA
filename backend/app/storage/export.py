"""Export utilities — JSON, CSV, Markdown."""

from __future__ import annotations

import csv
import io
import json

from ..models.run import RunResult


def to_json(result: RunResult) -> str:
    """Full JSON export."""
    return json.dumps(result.model_dump(mode="json"), ensure_ascii=False, indent=2)


def to_csv(result: RunResult) -> str:
    """Flat CSV of all messages across rounds."""
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["round", "phase", "agent", "content", "timestamp"])
    for rd in result.rounds:
        for msg in rd.messages:
            writer.writerow([rd.round_number, msg.phase.value, msg.agent_name, msg.content, msg.timestamp])
    return buf.getvalue()


def to_markdown(result: RunResult) -> str:
    """Human-readable Markdown transcript."""
    lines: list[str] = []
    cfg = result.config
    lines.append(f"# ARENA — {cfg.experiment_id.value}")
    lines.append(f"**Run:** {result.run_id}  ")
    lines.append(f"**Status:** {result.status.value}  ")
    lines.append(f"**Seed:** {cfg.seed}  ")
    if result.started_at:
        lines.append(f"**Début:** {result.started_at}  ")
    if result.finished_at:
        lines.append(f"**Fin:** {result.finished_at}  ")
    lines.append("")

    lines.append("## Agents")
    for a in cfg.agents:
        lines.append(f"- **{a.name}** ({a.model} via {a.provider.value})")
    lines.append("")

    for rd in result.rounds:
        lines.append(f"## Tour {rd.round_number}")
        if rd.instruction:
            lines.append(f"> {rd.instruction}")
            lines.append("")
        for msg in rd.messages:
            lines.append(f"### [{msg.phase.value}] {msg.agent_name}")
            lines.append(msg.content)
            lines.append("")
        if rd.votes:
            lines.append("### Votes")
            for v in rd.votes:
                lines.append(f"- **{v.agent_name}**: {v.choice} — _{v.reasoning}_")
            lines.append("")

    if result.metrics:
        lines.append("## Métriques")
        m = result.metrics
        lines.append(f"- Tokens totaux: {m.total_tokens}")
        lines.append(f"- Messages totaux: {m.total_messages}")
        lines.append(f"- Temps de réponse moyen: {m.average_response_time:.2f}s")
        lines.append(f"- Durée: {m.total_duration:.1f}s")
        lines.append("")

    return "\n".join(lines)
