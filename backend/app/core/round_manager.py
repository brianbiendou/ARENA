"""Round manager — orchestrates the phases within a single round."""

from __future__ import annotations

import logging
from typing import Any, Callable, Coroutine

from ..models.agent import AgentState, AgentStatus
from ..models.run import Message, PhaseType, RoundData, Vote
from .agent import Agent
from .prompt_builder import (
    build_discussion_prompt,
    build_reaction_prompt,
    build_vote_prompt,
)
from .seed import SeedManager

logger = logging.getLogger("arena.round_manager")

# Type for the WebSocket broadcast callback
BroadcastFn = Callable[[dict[str, Any]], Coroutine[Any, Any, None]]


class RoundManager:
    """Manages the execution of a single round."""

    def __init__(
        self,
        agents: list[Agent],
        seed_manager: SeedManager,
        temperature: float = 0.7,
        top_p: float = 0.9,
        max_tokens: int = 800,
        timeout_s: int = 60,
        broadcast: BroadcastFn | None = None,
    ):
        self.agents = agents
        self.seed = seed_manager
        self.temperature = temperature
        self.top_p = top_p
        self.max_tokens = max_tokens
        self.timeout_s = timeout_s
        self._broadcast = broadcast

    async def _emit(self, event: dict[str, Any]) -> None:
        if self._broadcast:
            await self._broadcast(event)

    async def run_round(
        self,
        round_number: int,
        total_rounds: int,
        previous_messages: list[dict[str, str]] | None = None,
        phase_instruction: str = "",
        vote_options: list[str] | None = None,
        vote_context: str = "",
    ) -> RoundData:
        """Execute a full round: discussion → reaction → optional vote."""
        round_data = RoundData(round_number=round_number)
        is_last = round_number == total_rounds

        await self._emit({
            "type": "round_start",
            "round": round_number,
            "total_rounds": total_rounds,
        })

        # --- Phase 1: Discussion ---
        speaking_order = self.seed.shuffle(self.agents)
        discussion_prompt = build_discussion_prompt(
            round_number=round_number,
            total_rounds=total_rounds,
            previous_messages=previous_messages,
            phase_instruction=phase_instruction,
        )

        round_messages: list[dict[str, str]] = []

        for agent in speaking_order:
            await self._emit({
                "type": "agent_status",
                "agent_id": agent.id,
                "status": AgentStatus.THINKING.value,
            })

            msg = await agent.generate(
                user_prompt=discussion_prompt,
                phase=PhaseType.DISCUSSION,
                temperature=self.temperature,
                top_p=self.top_p,
                max_tokens=self.max_tokens,
                timeout_s=self.timeout_s,
            )
            round_data.messages.append(msg)
            round_messages.append({"name": agent.name, "content": msg.content})

            await self._emit({
                "type": "message",
                "agent_id": agent.id,
                "agent_name": agent.name,
                "phase": PhaseType.DISCUSSION.value,
                "content": msg.content,
                "tokens": msg.tokens_used,
                "response_time_ms": msg.response_time_ms,
            })

        # --- Phase 2: Reaction ---
        reaction_prompt = build_reaction_prompt(round_messages)
        reaction_order = self.seed.shuffle(self.agents)

        for agent in reaction_order:
            await self._emit({
                "type": "agent_status",
                "agent_id": agent.id,
                "status": AgentStatus.THINKING.value,
            })

            msg = await agent.generate(
                user_prompt=reaction_prompt,
                phase=PhaseType.REACTION,
                temperature=self.temperature,
                top_p=self.top_p,
                max_tokens=300,  # Reactions are shorter
                timeout_s=self.timeout_s,
            )
            round_data.messages.append(msg)

            await self._emit({
                "type": "message",
                "agent_id": agent.id,
                "agent_name": agent.name,
                "phase": PhaseType.REACTION.value,
                "content": msg.content,
                "tokens": msg.tokens_used,
                "response_time_ms": msg.response_time_ms,
            })

        # --- Phase 3: Vote (last round or if options provided) ---
        if is_last and vote_options:
            await self._emit({"type": "phase", "phase": "vote"})

            vote_prompt_text = build_vote_prompt(vote_options, context=vote_context)

            for agent in self.agents:
                await self._emit({
                    "type": "agent_status",
                    "agent_id": agent.id,
                    "status": AgentStatus.VOTING.value,
                })

                msg = await agent.generate(
                    user_prompt=vote_prompt_text,
                    phase=PhaseType.VOTE,
                    temperature=0.3,  # Lower temp for votes
                    max_tokens=200,
                )
                round_data.messages.append(msg)

                vote = agent.parse_vote(msg)
                if vote:
                    vote.round_number = round_number
                    round_data.votes.append(vote)

                await self._emit({
                    "type": "vote",
                    "agent_id": agent.id,
                    "agent_name": agent.name,
                    "target": vote.target if vote else "ABSTENTION",
                    "reasoning": vote.reasoning if vote else None,
                })

        # Collect agent states
        for agent in self.agents:
            agent.state.status = AgentStatus.IDLE
            round_data.agent_states[agent.id] = agent.state.model_copy()

        await self._emit({
            "type": "round_end",
            "round": round_number,
        })

        return round_data
