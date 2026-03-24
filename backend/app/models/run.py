"""Pydantic models for runs, rounds, and results."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field

from .agent import AgentConfig, AgentState
from .experiment import ExperimentId, ExperimentSetup


class RunStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class PhaseType(str, Enum):
    INTRODUCTION = "introduction"
    DISCUSSION = "discussion"
    REACTION = "reaction"
    VOTE = "vote"
    RESOLUTION = "resolution"
    EVENT = "event"
    PLOT_TWIST = "plot_twist"


class Message(BaseModel):
    """A single message from an agent during a round."""
    agent_id: str
    phase: PhaseType
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)
    tokens_used: int = 0
    response_time_ms: int = 0
    metadata: dict[str, Any] = Field(default_factory=dict)


class Vote(BaseModel):
    agent_id: str
    target: str = Field(..., description="What/who does this vote target")
    round_number: int
    reasoning: Optional[str] = None


class RoundData(BaseModel):
    """Data for a single round within a run."""
    round_number: int
    messages: list[Message] = Field(default_factory=list)
    votes: list[Vote] = Field(default_factory=list)
    agent_states: dict[str, AgentState] = Field(default_factory=dict)
    events: list[dict[str, Any]] = Field(default_factory=list)
    summary: Optional[str] = None


class RunConfig(BaseModel):
    """Full configuration to launch a run."""
    experiment: ExperimentSetup
    agents: list[AgentConfig]
    seed: Optional[int] = None
    temperature: float = 0.7
    top_p: float = 0.9
    max_tokens: int = 800
    response_timeout_s: int = 60


class RunMetrics(BaseModel):
    """Computed metrics for a completed run."""
    total_tokens: int = 0
    total_messages: int = 0
    avg_response_time_ms: float = 0.0
    duration_s: float = 0.0
    rounds_completed: int = 0
    consensus_reached: Optional[bool] = None
    winner: Optional[str] = None
    agent_metrics: dict[str, dict[str, Any]] = Field(default_factory=dict)
    custom_metrics: dict[str, Any] = Field(default_factory=dict)


class RunResult(BaseModel):
    """Complete result of a run."""
    run_id: str
    status: RunStatus = RunStatus.PENDING
    experiment_id: ExperimentId
    config: RunConfig
    agents: list[AgentConfig] = Field(default_factory=list)
    rounds: list[RoundData] = Field(default_factory=list)
    metrics: Optional[RunMetrics] = None
    created_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    error: Optional[str] = None


class RunSummary(BaseModel):
    """Lightweight summary for listing runs."""
    run_id: str
    experiment_id: ExperimentId
    experiment_name: str
    status: RunStatus
    agent_count: int
    rounds_completed: int
    total_rounds: int
    created_at: datetime
    duration_s: Optional[float] = None
    consensus_reached: Optional[bool] = None
