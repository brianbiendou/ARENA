"""Run storage — save / load / list experiment runs as JSON files."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from ..config import get_data_dir
from ..models.run import RunResult, RunSummary


def _runs_dir() -> Path:
    d = get_data_dir() / "runs"
    d.mkdir(parents=True, exist_ok=True)
    return d


def save_run(result: RunResult) -> Path:
    """Persist a RunResult to disk and return the file path."""
    path = _runs_dir() / f"{result.run_id}.json"
    path.write_text(json.dumps(result.model_dump(mode="json"), ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def load_run(run_id: str) -> RunResult | None:
    """Load a single run by ID. Returns None if not found."""
    path = _runs_dir() / f"{run_id}.json"
    if not path.exists():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    return RunResult.model_validate(data)


def list_runs() -> list[RunSummary]:
    """Return summaries of all saved runs, newest first."""
    summaries: list[RunSummary] = []
    for path in _runs_dir().glob("*.json"):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            config = data.get("config", {})
            experiment_setup = config.get("experiment", {})
            metrics = data.get("metrics") or {}
            summaries.append(
                RunSummary(
                    run_id=data["run_id"],
                    experiment_id=data["experiment_id"],
                    experiment_name=data["experiment_id"],
                    status=data["status"],
                    agent_count=len(config.get("agents", [])),
                    rounds_completed=len(data.get("rounds", [])),
                    total_rounds=experiment_setup.get("num_rounds", 0),
                    created_at=data.get("created_at", ""),
                    duration_s=metrics.get("duration_s"),
                    consensus_reached=metrics.get("consensus_reached"),
                )
            )
        except Exception:
            continue
    summaries.sort(key=lambda s: s.created_at.isoformat() if hasattr(s.created_at, 'isoformat') else str(s.created_at), reverse=True)
    return summaries


def delete_run(run_id: str) -> bool:
    """Delete a run file. Returns True if deleted."""
    path = _runs_dir() / f"{run_id}.json"
    if path.exists():
        path.unlink()
        return True
    return False
