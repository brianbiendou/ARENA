"""Engine — main orchestrator that runs a complete experiment."""

from __future__ import annotations

import logging
import uuid
from datetime import datetime
from typing import Any, Callable, Coroutine

from ..models.agent import AgentConfig
from ..models.experiment import ExperimentSetup
from ..models.run import RunConfig, RunMetrics, RunResult, RunStatus
from ..providers.registry import ProviderRegistry
from .agent import Agent
from .round_manager import RoundManager
from .seed import SeedManager

logger = logging.getLogger("arena.engine")

BroadcastFn = Callable[[dict[str, Any]], Coroutine[Any, Any, None]]


class ArenaEngine:
    """Orchestrates a complete experiment run."""

    def __init__(self, registry: ProviderRegistry, broadcast: BroadcastFn | None = None):
        self.registry = registry
        self._broadcast = broadcast
        self._current_run: RunResult | None = None

    async def _emit(self, event: dict[str, Any]) -> None:
        if self._broadcast:
            await self._broadcast(event)

    def _create_agents(self, agent_configs: list[AgentConfig]) -> list[Agent]:
        """Instantiate Agent wrappers with their providers."""
        agents = []
        for cfg in agent_configs:
            provider = self.registry.get_for_model(cfg.model, cfg.provider)
            agents.append(Agent(config=cfg, provider=provider))
        return agents

    async def run(self, config: RunConfig) -> RunResult:
        """Execute a complete experiment run."""
        run_id = f"{config.experiment.experiment_id.value}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"

        result = RunResult(
            run_id=run_id,
            status=RunStatus.RUNNING,
            experiment_id=config.experiment.experiment_id,
            config=config,
            agents=config.agents,
            created_at=datetime.now(),
        )
        self._current_run = result

        await self._emit({
            "type": "run_start",
            "run_id": run_id,
            "experiment": config.experiment.experiment_id.value,
            "agents": [a.name for a in config.agents],
        })

        try:
            # Import experiment handler
            from ..experiments import get_experiment_handler
            experiment = get_experiment_handler(config.experiment.experiment_id)

            # Setup seed
            seed_mgr = SeedManager(config.seed)

            # Create agent instances
            agents = self._create_agents(config.agents)

            # Get experiment-specific setup
            setup_data = experiment.setup(config.experiment, seed_mgr)

            # Set system prompts for each agent
            system_prompt = setup_data["system_prompt"]
            for agent in agents:
                agent.set_system_prompt(system_prompt)
                # Apply private data if the experiment provides it
                private = setup_data.get("agent_private_data", {}).get(agent.id)
                if private:
                    agent.state.private_data = private
                    from .prompt_builder import build_agent_prompt
                    agent_prompt = build_agent_prompt(
                        template=setup_data.get("agent_prompt_template", ""),
                        agent_name=agent.name,
                        private_data=private,
                    )
                    if agent_prompt.strip():
                        agent.add_context(agent_prompt)

            # Run rounds
            round_mgr = RoundManager(
                agents=agents,
                seed_manager=seed_mgr,
                temperature=config.temperature,
                top_p=config.top_p,
                max_tokens=config.max_tokens,
                timeout_s=config.response_timeout_s,
                broadcast=self._broadcast,
            )

            all_messages: list[dict[str, str]] = []
            num_rounds = config.experiment.num_rounds

            for rnd in range(1, num_rounds + 1):
                # Check for events / plot twists
                phase_instruction = experiment.get_round_instruction(rnd, num_rounds, seed_mgr)
                events = experiment.get_events(rnd, num_rounds, seed_mgr)

                for ev in events:
                    await self._emit({"type": "event", "round": rnd, **ev})

                # Build vote options for last round
                vote_options = experiment.get_vote_options(config.experiment) if rnd == num_rounds else None

                round_data = await round_mgr.run_round(
                    round_number=rnd,
                    total_rounds=num_rounds,
                    previous_messages=all_messages if all_messages else None,
                    phase_instruction=phase_instruction,
                    vote_options=vote_options,
                    vote_context=experiment.get_vote_context(config.experiment),
                )
                round_data.events = events
                result.rounds.append(round_data)

                # Accumulate messages for context
                for msg in round_data.messages:
                    agent_name = next(
                        (a.name for a in agents if a.id == msg.agent_id), msg.agent_id
                    )
                    all_messages.append({"name": agent_name, "content": msg.content})

            # Compute metrics
            result.metrics = self._compute_metrics(result, agents)
            result.status = RunStatus.COMPLETED
            result.completed_at = datetime.now()

            await self._emit({
                "type": "run_end",
                "run_id": run_id,
                "status": "completed",
            })

        except Exception as e:
            logger.exception("Run failed: %s", e)
            result.status = RunStatus.FAILED
            result.error = str(e)
            result.completed_at = datetime.now()

            await self._emit({
                "type": "run_end",
                "run_id": run_id,
                "status": "failed",
                "error": str(e),
            })

        self._current_run = None
        return result

    def _compute_metrics(self, result: RunResult, agents: list[Agent]) -> RunMetrics:
        """Compute aggregate metrics from a completed run."""
        total_tokens = 0
        total_messages = 0
        total_response_time = 0

        agent_metrics: dict[str, dict[str, Any]] = {}

        for agent in agents:
            st = agent.state
            agent_metrics[agent.id] = {
                "name": agent.name,
                "tokens_used": st.tokens_used,
                "messages_sent": st.messages_sent,
                "avg_response_ms": (
                    st.tokens_used // max(st.messages_sent, 1)
                    if st.messages_sent else 0
                ),
            }
            total_tokens += st.tokens_used
            total_messages += st.messages_sent

        for rnd in result.rounds:
            for msg in rnd.messages:
                total_response_time += msg.response_time_ms

        duration = 0.0
        if result.completed_at and result.created_at:
            duration = (result.completed_at - result.created_at).total_seconds()

        return RunMetrics(
            total_tokens=total_tokens,
            total_messages=total_messages,
            avg_response_time_ms=(
                total_response_time / max(total_messages, 1)
            ),
            duration_s=duration,
            rounds_completed=len(result.rounds),
            agent_metrics=agent_metrics,
        )
