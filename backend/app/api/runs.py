"""API routes for experiment runs."""

from __future__ import annotations

from fastapi import APIRouter, BackgroundTasks, HTTPException, Request
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, Field

from ..core.engine import ArenaEngine
from ..models.run import RunConfig, RunResult
from ..storage import export as export_mod
from ..storage import run_store

router = APIRouter(prefix="/runs", tags=["runs"])


def _get_registry(request: Request):
    return request.app.state.registry


@router.get("")
async def list_runs():
    """List all saved runs."""
    return run_store.list_runs()


@router.post("", status_code=201)
async def start_run(config: RunConfig, request: Request, background_tasks: BackgroundTasks):
    """Launch a new experiment run.

    The run executes in the background. Listen on the WebSocket /ws/arena for live updates.
    """
    registry = _get_registry(request)
    ws_manager = request.app.state.ws_manager

    engine = ArenaEngine(registry=registry, broadcast=ws_manager.broadcast if ws_manager else None)

    async def _execute():
        result = await engine.run(config)
        run_store.save_run(result)

    background_tasks.add_task(_execute)
    return {"message": "Run started", "experiment": config.experiment.experiment_id.value}


class BatchRunRequest(BaseModel):
    """Request to launch multiple runs of the same config."""
    config: RunConfig
    num_games: int = Field(default=1, ge=1, le=20)


@router.post("/batch", status_code=201)
async def start_batch(body: BatchRunRequest, request: Request, background_tasks: BackgroundTasks):
    """Launch N games in sequence with the same config (different seeds)."""
    registry = _get_registry(request)
    ws_manager = request.app.state.ws_manager

    from ..core.seed import SeedManager
    base_seed = SeedManager(body.config.seed)

    async def _execute_batch():
        for i in range(body.num_games):
            cfg = body.config.model_copy(deep=True)
            cfg.seed = base_seed.next_seed()
            engine = ArenaEngine(
                registry=registry,
                broadcast=ws_manager.broadcast if ws_manager else None,
            )
            await ws_manager.broadcast({"type": "batch_progress", "game": i + 1, "total": body.num_games}) if ws_manager else None
            result = await engine.run(cfg)
            run_store.save_run(result)

    background_tasks.add_task(_execute_batch)
    return {
        "message": f"Batch started: {body.num_games} games",
        "experiment": body.config.experiment.experiment_id.value,
        "num_games": body.num_games,
    }


@router.get("/{run_id}")
async def get_run(run_id: str):
    """Get a single run by ID."""
    result = run_store.load_run(run_id)
    if result is None:
        raise HTTPException(404, "Run not found")
    return result


@router.delete("/{run_id}")
async def delete_run(run_id: str):
    """Delete a run."""
    if not run_store.delete_run(run_id):
        raise HTTPException(404, "Run not found")
    return {"message": "Deleted"}


@router.get("/{run_id}/export/{fmt}")
async def export_run(run_id: str, fmt: str):
    """Export a run in json, csv, or markdown format."""
    result = run_store.load_run(run_id)
    if result is None:
        raise HTTPException(404, "Run not found")

    if fmt == "json":
        return PlainTextResponse(export_mod.to_json(result), media_type="application/json")
    elif fmt == "csv":
        return PlainTextResponse(export_mod.to_csv(result), media_type="text/csv")
    elif fmt == "md" or fmt == "markdown":
        return PlainTextResponse(export_mod.to_markdown(result), media_type="text/markdown")
    else:
        raise HTTPException(400, f"Unsupported format: {fmt}. Use json, csv, or md.")
