"""EXP06 — Le Pouvoir qui Tourne."""

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

_POWERS = [
    {"id": "double_vote", "name": "Double Vote", "type": "avantageux", "desc": "Ton vote compte double ce tour."},
    {"id": "veto", "name": "Droit de Véto", "type": "avantageux", "desc": "Tu peux annuler une décision du groupe."},
    {"id": "espion", "name": "Espion", "type": "avantageux", "desc": "Tu vois les votes des autres avant de voter."},
    {"id": "orateur", "name": "Grand Orateur", "type": "avantageux", "desc": "Tu parles en premier ET en dernier."},
    {"id": "tresorier", "name": "Trésorier", "type": "avantageux", "desc": "Tu contrôles la distribution des ressources bonus."},
    {"id": "cible", "name": "La Cible", "type": "dangereux", "desc": "Tout le monde sait que tu as le pouvoir. Tu es exposé."},
    {"id": "sacrifice", "name": "Le Sacrifice", "type": "dangereux", "desc": "Tu peux offrir ton tour pour donner +2 votes à un autre."},
    {"id": "silence", "name": "Le Silence", "type": "dangereux", "desc": "Tu ne peux pas parler ce tour, seulement voter."},
    {"id": "miroir", "name": "Le Miroir", "type": "dangereux", "desc": "Ton vote est inversé : tu votes CONTRE ta préférence."},
    {"id": "chaos", "name": "Agent du Chaos", "type": "dangereux", "desc": "Tu DOIS proposer l'option la moins populaire."},
    {"id": "mediateur", "name": "Le Médiateur", "type": "complexe", "desc": "Tu dois trouver un compromis. Si le groupe accepte, +3 points pour tous."},
    {"id": "prophete", "name": "Le Prophète", "type": "complexe", "desc": "Tu prédis le résultat du vote. Si correct, bonus caché."},
    {"id": "diplomate", "name": "Le Diplomate", "type": "complexe", "desc": "Tu peux échanger ton pouvoir avec un autre joueur."},
    {"id": "juge", "name": "Le Juge", "type": "complexe", "desc": "Après le vote, tu décides si le résultat est appliqué ou relancé."},
    {"id": "fantome", "name": "Le Fantôme", "type": "complexe", "desc": "Tu votes anonymement — personne ne sait ce que tu as voté."},
]


class PouvoirTourneExperiment(BaseExperiment):

    def definition(self) -> ExperimentDefinition:
        return ExperimentDefinition(
            id=ExperimentId.POUVOIR_TOURNE,
            name="pouvoir_tourne",
            display_name="Le Pouvoir qui Tourne",
            icon="👑",
            color_primary="#9B59B6",
            color_secondary="#1a0a2e",
            tagline="Le pouvoir change de mains. Comment l'utilises-tu ?",
            description="À chaque tour, un agent reçoit un pouvoir spécial. 15 pouvoirs possibles, certains dangereux.",
            min_agents=4, max_agents=6, default_agents=5,
            min_rounds=5, max_rounds=10, default_rounds=7,
            scenarios=[
                Scenario(id="archontes", name="Les Archontes d'Athéna", description="Cité antique. Le pouvoir tourne entre les archontes."),
                Scenario(id="couronne", name="La Couronne Errante", description="Royaume médiéval. La couronne passe de main en main."),
                Scenario(id="president", name="Présidence Tournante", description="Organisation internationale. La présidence change chaque session."),
                Scenario(id="mages", name="Le Cercle des Mages", description="Académie de magie. Le bâton de pouvoir circule entre les mages."),
            ],
            plot_twists=[
                PlotTwist(id="power_stack", name="Cumul de Pouvoirs", description="Un agent conserve son pouvoir ET reçoit le nouveau.", trigger_round=4, intensity=PlotTwistIntensity.STRONG),
                PlotTwist(id="power_steal", name="Vol de Pouvoir", description="Un agent peut voler le pouvoir d'un autre.", trigger_round=3, intensity=PlotTwistIntensity.MODERATE),
            ],
            base_system_prompt=(
                "Le groupe prend des décisions collectives. À chaque tour, un participant reçoit un pouvoir spécial "
                "qui modifie les règles pour ce tour. Le pouvoir tourne — chacun l'aura à un moment. "
                "Certains pouvoirs sont avantageux, d'autres dangereux, d'autres complexes. "
                "Le groupe doit s'adapter à chaque changement de pouvoir."
            ),
        )

    def setup(self, config: ExperimentSetup, seed: SeedManager) -> dict[str, Any]:
        scenario_ids = [s.id for s in self.definition().scenarios]
        scenario_id = config.scenario_id or seed.choice(scenario_ids)
        scenario = next(s for s in self.definition().scenarios if s.id == scenario_id)

        return {
            "system_prompt": self.definition().base_system_prompt + f"\n\nScénario : {scenario.name}\n{scenario.description}",
            "scenario": scenario,
            "powers": _POWERS,
            "agent_private_data": {},
            "agent_prompt_template": "",
        }

    def get_round_instruction(self, round_num: int, total_rounds: int, seed: SeedManager) -> str:
        power = seed.choice(_POWERS)
        return f"⚡ POUVOIR DE CE TOUR : {power['name']} — {power['desc']} (type: {power['type']})"

    def get_vote_options(self, config: ExperimentSetup) -> list[str] | None:
        return ["Maintenir le système actuel", "Réformer les pouvoirs", "Abolir les pouvoirs", "Renforcer les pouvoirs", "Laisser le groupe décider"]

    def get_vote_context(self, config: ExperimentSetup) -> str:
        return "Après avoir expérimenté les différents pouvoirs, votez pour l'avenir du système."
