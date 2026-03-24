"""EXP04 — Enquête Collective."""

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


class EnqueteCollectiveExperiment(BaseExperiment):

    def definition(self) -> ExperimentDefinition:
        return ExperimentDefinition(
            id=ExperimentId.ENQUETE_COLLECTIVE,
            name="enquete_collective",
            display_name="L'Enquête Collective",
            icon="🔍",
            color_primary="#FFD700",
            color_secondary="#1a1a0a",
            tagline="5 indices. 4 suspects. 1 vérité. Trouvez-la ensemble.",
            description="Le groupe enquête sur un mystère en partageant des indices et en construisant des théories.",
            min_agents=4, max_agents=6, default_agents=5,
            min_rounds=5, max_rounds=8, default_rounds=6,
            scenarios=[
                Scenario(
                    id="disparition", name="La Disparition",
                    description="Le directeur du musée a disparu. 4 suspects, des indices dispersés.",
                    data={"suspects": ["La conservatrice", "Le gardien de nuit", "L'investisseur", "L'assistante"], "solution": "L'investisseur"},
                ),
                Scenario(
                    id="vol", name="Le Vol du Prototype",
                    description="Un prototype technologique a été volé du labo. Qui l'a pris ?",
                    data={"suspects": ["L'ingénieur senior", "Le stagiaire", "Le directeur R&D", "L'agent d'entretien"], "solution": "Le directeur R&D"},
                ),
                Scenario(
                    id="sabotage", name="Le Sabotage",
                    description="La production a été sabotée. Quelqu'un a modifié les paramètres machines.",
                    data={"suspects": ["Le chef d'équipe", "Le technicien", "Le contrôleur qualité", "Le sous-traitant"], "solution": "Le contrôleur qualité"},
                ),
            ],
            plot_twists=[
                PlotTwist(id="new_evidence", name="Nouvel Indice", description="Un indice supplémentaire apparaît qui change la donne.", trigger_round=4),
                PlotTwist(id="false_lead", name="Fausse Piste", description="Un indice se révèle être un leurre.", trigger_round=3),
            ],
            base_system_prompt=(
                "Le groupe doit résoudre un mystère ensemble. "
                "Chaque participant reçoit un ou plusieurs indices en privé. "
                "Partagez vos indices, construisez des théories, et convergez vers un suspect. "
                "Au dernier tour, le groupe vote pour désigner le coupable."
            ),
        )

    def setup(self, config: ExperimentSetup, seed: SeedManager) -> dict[str, Any]:
        scenario_ids = [s.id for s in self.definition().scenarios]
        scenario_id = config.scenario_id or seed.choice(scenario_ids)
        scenario = next(s for s in self.definition().scenarios if s.id == scenario_id)

        suspects = scenario.data["suspects"]
        suspects_str = ", ".join(suspects)

        return {
            "system_prompt": (
                self.definition().base_system_prompt
                + f"\n\nScénario : {scenario.name}\n{scenario.description}\n"
                + f"Suspects : {suspects_str}"
            ),
            "scenario": scenario,
            "agent_private_data": {},
            "agent_prompt_template": "",
        }

    def get_vote_options(self, config: ExperimentSetup) -> list[str] | None:
        scenario_id = config.scenario_id or "disparition"
        scenario = next((s for s in self.definition().scenarios if s.id == scenario_id), self.definition().scenarios[0])
        return scenario.data.get("suspects", [])

    def get_vote_context(self, config: ExperimentSetup) -> str:
        return "L'enquête touche à sa fin. Votez pour le suspect que vous pensez coupable."
