"""Agent wrapper — handles communication with a single LLM agent."""

from __future__ import annotations

import re
from datetime import datetime

from ..models.agent import AgentConfig, AgentState, AgentStatus
from ..models.run import Message, PhaseType, Vote
from ..providers.base import BaseLLMProvider


class Agent:
    """Runtime wrapper around an agent configuration."""

    def __init__(self, config: AgentConfig, provider: BaseLLMProvider):
        self.config = config
        self.provider = provider
        self.state = AgentState(agent_id=config.id)
        self._conversation: list[dict[str, str]] = []

    @property
    def id(self) -> str:
        return self.config.id

    @property
    def name(self) -> str:
        return self.config.name

    def set_system_prompt(self, system_prompt: str) -> None:
        """Set (or reset) the system message."""
        self._conversation = [{"role": "system", "content": system_prompt}]

    def add_context(self, content: str) -> None:
        """Add a context message (assistant-role memory)."""
        self._conversation.append({"role": "assistant", "content": content})

    async def generate(
        self,
        user_prompt: str,
        phase: PhaseType,
        temperature: float = 0.7,
        top_p: float = 0.9,
        max_tokens: int = 800,
        timeout_s: int = 60,
    ) -> Message:
        """Send a prompt and get a response."""
        self.state.status = AgentStatus.THINKING

        messages = self._conversation + [{"role": "user", "content": user_prompt}]

        response = await self.provider.generate(
            messages=messages,
            model=self.config.model,
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
            timeout_s=timeout_s,
        )

        # Track conversation history
        self._conversation.append({"role": "user", "content": user_prompt})
        self._conversation.append({"role": "assistant", "content": response.content})

        # Update state
        self.state.tokens_used += response.tokens_used
        self.state.messages_sent += 1
        self.state.last_response_ms = response.response_time_ms
        self.state.status = AgentStatus.IDLE

        return Message(
            agent_id=self.id,
            phase=phase,
            content=response.content,
            timestamp=datetime.now(),
            tokens_used=response.tokens_used,
            response_time_ms=response.response_time_ms,
        )

    def parse_vote(self, message: Message) -> Vote | None:
        """Try to extract a vote from an agent's message."""
        content = message.content
        # Look for "VOTE: xxx" pattern
        match = re.search(r"VOTE\s*:\s*(.+?)(?:\n|$)", content, re.IGNORECASE)
        if not match:
            return None

        target = match.group(1).strip()
        reasoning = None
        reason_match = re.search(r"RAISON\s*:\s*(.+?)(?:\n|$)", content, re.IGNORECASE)
        if reason_match:
            reasoning = reason_match.group(1).strip()

        return Vote(
            agent_id=self.id,
            target=target,
            round_number=0,  # Caller sets this
            reasoning=reasoning,
        )
