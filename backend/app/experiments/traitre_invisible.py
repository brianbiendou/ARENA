"""EXP03 — Le Traître Invisible."""

from __future__ import annotations

from typing import Any

from ..core.seed import SeedManager
from ..models.experiment import (
    ExperimentDefinition,
    ExperimentId,
    ExperimentSetup,
    PlotTwist,
    PlotTwistIntensity,
    Scenario,
)
from .base import BaseExperiment


class TraitreInvisibleExperiment(BaseExperiment):

    def definition(self) -> ExperimentDefinition:
        return ExperimentDefinition(
            id=ExperimentId.TRAITRE_INVISIBLE,
            name="traitre_invisible",
            display_name="Le Traître Invisible",
            icon="🐍",
            color_primary="#8B0000",
            color_secondary="#0d0d0d",
            tagline="L'un d'entre vous ment. Mais lequel ?",
            description="Le groupe doit accomplir un objectif commun, mais un traître secret travaille contre eux.",
            min_agents=5, max_agents=7, default_agents=5,
            min_rounds=5, max_rounds=8, default_rounds=6,
            scenarios=[
                Scenario(id="laboratoire", name="Le Laboratoire", description="L'équipe scientifique doit valider un protocole. Le saboteur veut le faire échouer."),
                Scenario(id="expedition", name="L'Expédition", description="Un groupe d'explorateurs cherche un trésor. Le traître veut le garder pour lui."),
                Scenario(id="conseil", name="Le Conseil Municipal", description="Le conseil vote un projet. Un membre corrompu tente de le saboter discrètement."),
            ],
            plot_twists=[
                PlotTwist(id="double_agent", name="Le Double Jeu", description="Le traître peut changer de camp au tour 4 s'il n'a pas été suspecté.", trigger_round=4),
                PlotTwist(id="evidence", name="La Preuve", description="Un indice est révélé qui pointe vers un agent (peut être le traître ou un innocent).", trigger_round=3),
            ],
            base_system_prompt=(
                "Le groupe travaille ensemble sur un objectif commun. "
                "Chaque participant contribue par ses propositions et ses votes. "
                "Le groupe peut discuter librement de ses soupçons. "
                "À chaque tour de vote, le groupe peut choisir d'accuser un participant."
            ),
        )

    def setup(self, config: ExperimentSetup, seed: SeedManager) -> dict[str, Any]:
        scenarios = {"laboratoire": 0, "expedition": 1, "conseil": 2}
        scenario_id = config.scenario_id or seed.choice(list(scenarios.keys()))
        scenario = next(s for s in self.definition().scenarios if s.id == scenario_id)

        return {
            "system_prompt": self.definition().base_system_prompt + f"\n\nScénario : {scenario.name}\n{scenario.description}",
            "scenario": scenario,
            "agent_private_data": {},  # Traitor role assigned at runtime by engine
            "agent_prompt_template": "",
            "traitor_prompt": (
                "Tu as un objectif secret : faire échouer le projet du groupe SANS te faire démasquer. "
                "Sois subtil. Ne sabote pas ouvertement. Sème le doute, propose des solutions qui semblent bonnes "
                "mais qui sont subtilement néfastes. Si le groupe te démasque, tu perds."
            ),
        }

    def get_vote_options(self, config: ExperimentSetup) -> list[str] | None:
        return ["Valider le projet", "Rejeter le projet", "Reporter la décision"]

    def get_vote_context(self, config: ExperimentSetup) -> str:
        return "Le groupe doit décider du sort du projet. Le traître essaie de faire échouer le vote."
