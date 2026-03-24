"""API routes for experiments."""

from __future__ import annotations

from fastapi import APIRouter

from ..experiments import get_all_definitions, get_experiment_handler
from ..models.experiment import ExperimentId

router = APIRouter(prefix="/experiments", tags=["experiments"])


@router.get("")
async def list_experiments():
    """Return all experiment definitions."""
    return get_all_definitions()


@router.get("/{experiment_id}")
async def get_experiment(experiment_id: ExperimentId):
    """Return a single experiment definition."""
    handler = get_experiment_handler(experiment_id)
    return handler.definition()
