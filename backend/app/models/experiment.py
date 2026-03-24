"""Pydantic models for experiments."""

from __future__ import annotations

from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class ExperimentId(str, Enum):
    BUDGET_GROUPE = "budget_groupe"
    CONSEIL_CRISE = "conseil_crise"
    TRAITRE_INVISIBLE = "traitre_invisible"
    ENQUETE_COLLECTIVE = "enquete_collective"
    NEGOCIATION_RESSOURCES = "negociation_ressources"
    POUVOIR_TOURNE = "pouvoir_tourne"
    INFORMATION_FRAGMENTEE = "information_fragmentee"
    REPARTITION_PRIORITES = "repartition_priorites"
    CONSTRUCTION_REGLE = "construction_regle"
    LOI_DU_GROUPE = "loi_du_groupe"


class PlotTwistIntensity(str, Enum):
    SUBTLE = "subtle"
    MODERATE = "moderate"
    STRONG = "strong"


class Scenario(BaseModel):
    id: str
    name: str
    description: str
    data: dict[str, Any] = Field(default_factory=dict)


class PlotTwist(BaseModel):
    id: str
    name: str
    description: str
    trigger_round: Optional[int] = None
    intensity: PlotTwistIntensity = PlotTwistIntensity.MODERATE


class ExperimentDefinition(BaseModel):
    """Static definition of an experiment (from Blueprint)."""
    id: ExperimentId
    name: str
    display_name: str
    icon: str
    color_primary: str
    color_secondary: str
    tagline: str
    description: str

    min_agents: int = 4
    max_agents: int = 7
    default_agents: int = 5
    min_rounds: int = 3
    max_rounds: int = 10
    default_rounds: int = 5

    scenarios: list[Scenario] = Field(default_factory=list)
    plot_twists: list[PlotTwist] = Field(default_factory=list)
    parameters: dict[str, Any] = Field(default_factory=dict, description="Experiment-specific params")

    base_system_prompt: str = ""
    agent_prompt_template: str = ""


class ExperimentSetup(BaseModel):
    """User-configured experiment for a run."""
    experiment_id: ExperimentId
    scenario_id: Optional[str] = None
    num_rounds: int = 5
    enable_plot_twists: bool = False
    plot_twist_intensity: PlotTwistIntensity = PlotTwistIntensity.MODERATE
    enable_random_events: bool = True
    custom_parameters: dict[str, Any] = Field(default_factory=dict)
