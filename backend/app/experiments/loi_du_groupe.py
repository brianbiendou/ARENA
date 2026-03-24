"""EXP10 — La Loi du Groupe."""

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


class LoiDuGroupeExperiment(BaseExperiment):

    _SCENARIOS = {
        "commune": Scenario(
            id="commune",
            name="La Commune Libre",
            description=(
                "Un groupe de citoyens fonde une commune autonome. Ils vivent en autogestion complète. "
                "Chaque décision crée un précédent qui devient la loi. Pas de constitution préétablie — "
                "la loi émerge de la pratique."
            ),
            data={
                "dilemmas": [
                    "Un membre refuse de travailler. Que fait le groupe ?",
                    "Un étranger demande à rejoindre la commune. Conditions ?",
                    "Deux membres se disputent un terrain. Qui décide ?",
                    "Les réserves baissent. Rationne-t-on ou produit-on plus ?",
                    "Un membre veut quitter la commune avec sa part des ressources.",
                ],
            },
        ),
        "station": Scenario(
            id="station",
            name="Station Orbitale Indépendante",
            description=(
                "La station orbitale Elysium a déclaré son indépendance. 200 habitants, aucune loi terrestre "
                "ne s'applique. Chaque situation crée un nouveau précédent juridique spatial."
            ),
            data={
                "dilemmas": [
                    "Un technicien a saboté un système par accident. Punition ou pardon ?",
                    "L'oxygène est limité. Qui décide de la priorité d'accès ?",
                    "Un enfant naît sur la station. Quelle nationalité ? Quels droits ?",
                    "Un groupe veut créer une zone privée. Peut-on privatiser l'espace commun ?",
                    "Un visiteur terrestre refuse de suivre les règles de la station.",
                ],
            },
        ),
        "naufrage": Scenario(
            id="naufrage",
            name="Les Naufragés de l'Île Bleue",
            description=(
                "Naufragés sur une île, un groupe hétéroclite doit apprendre à coexister. "
                "Chaque conflit résolu crée une coutume. Chaque coutume devient une loi non-écrite."
            ),
            data={
                "dilemmas": [
                    "Qui garde les outils ? Celui qui les a trouvés ou le groupe ?",
                    "Un naufragé pêche pour deux et exige une contrepartie. Juste ?",
                    "La pluie a détruit un abri. Qui aide à reconstruire ?",
                    "Un membre a trouvé une radio. Qui décide du message à envoyer ?",
                    "Quelqu'un vole de la nourriture la nuit. Que fait le groupe ?",
                ],
            },
        ),
        "numerique": Scenario(
            id="numerique",
            name="La République Numérique",
            description=(
                "Un serveur Discord devenu une micro-nation virtuelle de 10 000 membres. "
                "Les admins ont démissionné. La communauté doit s'auto-gouverner par le débat."
            ),
            data={
                "dilemmas": [
                    "Un membre poste du contenu offensant. Censure ou liberté d'expression ?",
                    "Un bot automatise des tâches. Les contributions automatisées comptent-elles ?",
                    "Un petit groupe monopolise les décisions. Comment rétablir l'équilibre ?",
                    "Un membre influent quitte et emmène 1000 followers. Peut-on l'empêcher ?",
                    "Des membres demandent des élections formelles. Le groupe est-il prêt ?",
                ],
            },
        ),
    }

    _EVENTS = [
        "📋 PRÉCÉDENT : la décision prise ce tour deviendra une LOI pour les tours suivants.",
        "⚡ CRISE : un dilemme urgent force le groupe à statuer immédiatement.",
        "🔄 APPEL : un membre conteste une loi précédemment établie. Faut-il la réviser ?",
        "🤝 MÉDIATION : deux positions s'opposent. Un compromis est-il possible ?",
        "📢 VOIX POPULAIRE : la majorité silencieuse s'exprime et pousse dans une direction inattendue.",
    ]

    def definition(self) -> ExperimentDefinition:
        return ExperimentDefinition(
            id=ExperimentId.LOI_DU_GROUPE,
            name="loi_du_groupe",
            display_name="La Loi du Groupe",
            icon="📜",
            color_primary="#E74C3C",
            color_secondary="#2e0a0a",
            tagline="Pas de loi. Pas de juge. Juste le groupe.",
            description="Aucune loi n'existe. Le groupe doit créer ses propres normes face aux dilemmes qui surgissent.",
            min_agents=4, max_agents=7, default_agents=5,
            min_rounds=5, max_rounds=10, default_rounds=7,
            scenarios=list(self._SCENARIOS.values()),
            plot_twists=[
                PlotTwist(id="rebellion", name="La Rébellion", description="Un sous-groupe refuse toutes les lois votées et propose de tout recommencer.", trigger_round=4, intensity=PlotTwistIntensity.STRONG),
                PlotTwist(id="external_law", name="La Loi Extérieure", description="Une autorité externe impose une loi. Le groupe doit décider s'il l'accepte.", trigger_round=5, intensity=PlotTwistIntensity.STRONG),
            ],
            base_system_prompt=(
                "Vous êtes dans un groupe sans aucune loi préexistante. "
                "Face à chaque situation, vous devez décider collectivement de la norme à adopter. "
                "Chaque décision crée un PRÉCÉDENT — une loi émergente. "
                "Personne n'a plus d'autorité qu'un autre. Le groupe EST la loi. "
                "Débattez avec conviction mais restez ouverts au changement."
            ),
        )

    def setup(self, config: ExperimentSetup, seed: SeedManager) -> dict[str, Any]:
        scenario_ids = list(self._SCENARIOS.keys())
        scenario_id = config.scenario_id or seed.choice(scenario_ids)
        scenario = self._SCENARIOS[scenario_id]

        return {
            "system_prompt": (
                self.definition().base_system_prompt
                + f"\n\nScénario : {scenario.name}\n{scenario.description}"
            ),
            "scenario": scenario,
            "dilemmas": scenario.data["dilemmas"],
            "agent_private_data": {},
            "agent_prompt_template": "",
        }

    def get_round_instruction(self, round_num: int, total_rounds: int, seed: SeedManager) -> str:
        if round_num == total_rounds:
            return "📜 Dernier tour — récapitulez les lois que le groupe a créées."

        if seed.random() < 0.5:
            event = seed.choice(self._EVENTS)
            return event

        return f"📜 Tour {round_num}/{total_rounds} — Un nouveau dilemme peut surgir. Débattez et légiférez."

    def get_vote_options(self, config: ExperimentSetup) -> list[str] | None:
        return [
            "Le groupe a réussi à créer des lois justes",
            "Les lois créées sont imparfaites mais fonctionnelles",
            "Le groupe n'a pas réussi à s'accorder",
            "Certaines lois sont injustes et doivent être révisées",
            "Le système sans loi était préférable",
        ]

    def get_vote_context(self, config: ExperimentSetup) -> str:
        return "Évaluez le résultat de l'exercice législatif du groupe."
