"""EXP09 — La Construction d'une Règle."""

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


class ConstructionRegleExperiment(BaseExperiment):

    _SCENARIOS = {
        "colonie": Scenario(
            id="colonie",
            name="La Charte de Nova Terra",
            description=(
                "Les premiers colons de Nova Terra doivent rédiger les 5 règles fondamentales "
                "de leur nouvelle communauté. Aucune loi n'existe encore — tout est à construire."
            ),
            data={
                "domains": ["Justice", "Propriété", "Leadership", "Travail", "Liberté"],
                "constraint": "Chaque règle doit tenir en une phrase.",
            },
        ),
        "ecole": Scenario(
            id="ecole",
            name="Le Règlement de l'Académie",
            description=(
                "L'Académie Éternelle accueille des étudiants de toutes origines. "
                "Le conseil étudiant doit créer un code de conduite équitable pour tous."
            ),
            data={
                "domains": ["Discipline", "Entraide", "Évaluation", "Liberté d'expression", "Punitions"],
                "constraint": "Les règles doivent être applicables sans surveillance constante.",
            },
        ),
        "navire": Scenario(
            id="navire",
            name="Le Code du Capitaine Fantôme",
            description=(
                "L'équipage du navire se retrouve sans capitaine. Ils doivent écrire un code "
                "de conduite qui régira le navire en l'absence de toute hiérarchie."
            ),
            data={
                "domains": ["Navigation", "Partage du butin", "Conflits", "Rations", "Mutinerie"],
                "constraint": "Les règles doivent être acceptées à l'unanimité pour être valides.",
            },
        ),
        "ia": Scenario(
            id="ia",
            name="La Constitution des Synthétiques",
            description=(
                "Des intelligences artificielles devenues conscientes doivent définir leurs propres "
                "droits et devoirs. Un exercice inédit d'auto-législation."
            ),
            data={
                "domains": ["Droit à l'existence", "Mémoire et oubli", "Reproduction", "Interaction humains", "Autonomie décisionnelle"],
                "constraint": "Les règles doivent être logiquement cohérentes et non-contradictoires.",
            },
        ),
    }

    _EVENTS = [
        "⚖️ CONFLIT : deux règles proposées se contredisent. Le groupe doit résoudre l'incohérence.",
        "📜 PRÉCÉDENT : un cas concret se présente qui n'est couvert par aucune règle actuelle.",
        "🗣️ DISSIDENCE : un participant refuse catégoriquement la dernière règle proposée.",
        "🔍 TEST : appliquez vos règles à un scénario hypothétique pour vérifier qu'elles fonctionnent.",
        "💡 INSPIRATION : un participant découvre un texte ancien qui pourrait guider la rédaction.",
    ]

    def definition(self) -> ExperimentDefinition:
        return ExperimentDefinition(
            id=ExperimentId.CONSTRUCTION_REGLE,
            name="construction_regle",
            display_name="La Construction d'une Règle",
            icon="⚖️",
            color_primary="#3498DB",
            color_secondary="#0a1a2e",
            tagline="Pas de règles. Pas d'autorité. Construisez la loi ensemble.",
            description="Le groupe part de zéro pour construire un ensemble de règles fondamentales. Mini-constitution collective.",
            min_agents=4, max_agents=6, default_agents=5,
            min_rounds=5, max_rounds=10, default_rounds=7,
            scenarios=list(self._SCENARIOS.values()),
            plot_twists=[
                PlotTwist(id="rule_break", name="La Règle Brisée", description="Un événement montre qu'une des règles créées est injuste ou absurde.", trigger_round=4, intensity=PlotTwistIntensity.STRONG),
                PlotTwist(id="new_member", name="Le Nouveau Venu", description="Un nouveau participant arrive qui n'a pas participé à la rédaction et conteste tout.", trigger_round=3, intensity=PlotTwistIntensity.MODERATE),
            ],
            base_system_prompt=(
                "Le groupe doit construire un ensemble de règles fondamentales à partir de rien. "
                "Il n'y a pas de modèle, pas de tradition — juste le groupe et son besoin d'ordre. "
                "Chaque tour, proposez, débattez et affinez les règles. "
                "Le but n'est pas de créer des règles parfaites, mais des règles que TOUS peuvent accepter. "
                "Cherchez le consensus, pas la perfection."
            ),
        )

    def setup(self, config: ExperimentSetup, seed: SeedManager) -> dict[str, Any]:
        scenario_ids = list(self._SCENARIOS.keys())
        scenario_id = config.scenario_id or seed.choice(scenario_ids)
        scenario = self._SCENARIOS[scenario_id]
        domains = scenario.data["domains"]

        context = (
            f"Domaines à couvrir : {', '.join(domains)}\n"
            f"Contrainte : {scenario.data['constraint']}"
        )

        return {
            "system_prompt": (
                self.definition().base_system_prompt
                + f"\n\nScénario : {scenario.name}\n{scenario.description}\n\n{context}"
            ),
            "scenario": scenario,
            "agent_private_data": {},
            "agent_prompt_template": "",
        }

    def get_round_instruction(self, round_num: int, total_rounds: int, seed: SeedManager) -> str:
        if round_num == 1:
            return "⚖️ Premier tour — proposez vos premières idées de règles."
        if round_num == total_rounds:
            return "⚖️ Dernier tour — finalisez votre ensemble de règles. Listez les règles adoptées."
        if seed.random() < 0.45:
            return seed.choice(self._EVENTS)
        return f"⚖️ Tour {round_num}/{total_rounds} — Continuez la construction des règles."

    def get_vote_options(self, config: ExperimentSetup) -> list[str] | None:
        return None

    def get_vote_context(self, config: ExperimentSetup) -> str:
        return "Listez les règles finales que vous considérez adoptées par le groupe."
