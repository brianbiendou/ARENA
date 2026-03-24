"""Pydantic models for agents."""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

from .settings import ProviderType


class AgentStatus(str, Enum):
    IDLE = "idle"
    THINKING = "thinking"
    SPEAKING = "speaking"
    WAITING = "waiting"
    VOTING = "voting"
    ELIMINATED = "eliminated"


class AgentConfig(BaseModel):
    """Configuration for a single agent in a run."""
    id: str = Field(..., description="Unique agent id for this run, e.g. agent_1")
    name: str = Field(..., description="Display name, e.g. 'Claude-3.5 Sonnet'")
    model: str = Field(..., description="Model identifier, e.g. 'anthropic/claude-3.5-sonnet'")
    provider: ProviderType
    color: str = Field("#00bcd4", description="Hex color for UI")


class AgentState(BaseModel):
    """Live state of an agent during a run."""
    agent_id: str
    status: AgentStatus = AgentStatus.IDLE
    tokens_used: int = 0
    messages_sent: int = 0
    last_response_ms: Optional[int] = None
    eliminated: bool = False
    private_data: dict = Field(default_factory=dict, description="Secret role, fragments, etc.")
