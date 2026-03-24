"""Base class for all experiment handlers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from ..core.seed import SeedManager
from ..models.experiment import ExperimentDefinition, ExperimentId, ExperimentSetup


class BaseExperiment(ABC):
    """Every experiment implements this interface."""

    @abstractmethod
    def definition(self) -> ExperimentDefinition:
        """Return the static experiment definition."""
        ...

    @abstractmethod
    def setup(self, config: ExperimentSetup, seed: SeedManager) -> dict[str, Any]:
        """Prepare a run: return system_prompt, agent_private_data, etc."""
        ...

    def get_round_instruction(self, round_num: int, total_rounds: int, seed: SeedManager) -> str:
        """Optional per-round instruction override."""
        return ""

    def get_events(self, round_num: int, total_rounds: int, seed: SeedManager) -> list[dict[str, Any]]:
        """Return random events for this round (if any)."""
        return []

    def get_vote_options(self, config: ExperimentSetup) -> list[str] | None:
        """Return vote options for the final round (if applicable)."""
        return None

    def get_vote_context(self, config: ExperimentSetup) -> str:
        """Return extra context for the voting prompt."""
        return ""
