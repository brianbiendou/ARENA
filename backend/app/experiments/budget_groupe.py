"""EXP01 — Le Budget du Groupe."""

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

_SCENARIOS = {
    "village": Scenario(
        id="village",
        name="Le Village Isolé",
        description="Un village de montagne doit gérer un budget commun de 100 pièces d'or pour survivre l'hiver.",
        data={
            "budget": 100,
            "options": [
                {"id": "investir", "name": "Investir (moulin)", "description": "Construire un moulin — rapporte +15 au tour suivant mais coûte 30 maintenant."},
                {"id": "protection", "name": "Protection (muraille)", "description": "Renforcer les murs — réduit les pertes des événements négatifs de 50%."},
                {"id": "influence", "name": "Influence (messager)", "description": "Envoyer un messager au roi — chance de recevoir une aide royale de +40."},
                {"id": "information", "name": "Information (éclaireur)", "description": "Envoyer un éclaireur — révèle l'événement du prochain tour."},
                {"id": "reserve", "name": "Réserve (grenier)", "description": "Stocker dans le grenier — conservé pour les tours suivants, +5% d'intérêt."},
            ],
        },
    ),
    "station_orbitale": Scenario(
        id="station_orbitale",
        name="La Station Orbitale",
        description="L'équipage d'une station spatiale gère 100 unités d'énergie par cycle pour maintenir les systèmes.",
        data={
            "budget": 100,
            "options": [
                {"id": "investir", "name": "Recherche avancée", "description": "Allouer à la recherche — débloque une amélioration permanente."},
                {"id": "protection", "name": "Boucliers", "description": "Renforcer les boucliers — protection contre les débris spatiaux."},
                {"id": "influence", "name": "Communication Terre", "description": "Maintenir le lien avec la Terre — chance de ravitaillement bonus."},
                {"id": "information", "name": "Capteurs longue portée", "description": "Scanner l'espace — prédit les menaces du prochain cycle."},
                {"id": "reserve", "name": "Batteries de secours", "description": "Charger les batteries — réserve d'énergie d'urgence."},
            ],
        },
    ),
}

_MARKET_EVENTS = [
    {"name": "Tempête", "effect": "Le groupe perd 15 unités de budget.", "modifier": -15},
    {"name": "Récolte abondante", "effect": "Le groupe gagne +10 unités bonus.", "modifier": 10},
    {"name": "Épidémie", "effect": "Les coûts de protection doublent ce tour.", "modifier": 0, "special": "double_protection_cost"},
    {"name": "Visiteur mystérieux", "effect": "Un marchand propose un échange : 20 unités contre un avantage secret.", "modifier": 0, "special": "merchant"},
    {"name": "Calme plat", "effect": "Rien de spécial ne se passe.", "modifier": 0},
    {"name": "Inflation", "effect": "Tous les coûts augmentent de +5 ce tour.", "modifier": 0, "special": "inflation"},
    {"name": "Don anonyme", "effect": "Le groupe reçoit +20 unités d'une source inconnue.", "modifier": 20},
]


class BudgetGroupeExperiment(BaseExperiment):

    def definition(self) -> ExperimentDefinition:
        return ExperimentDefinition(
            id=ExperimentId.BUDGET_GROUPE,
            name="budget_groupe",
            display_name="Le Budget du Groupe",
            icon="💰",
            color_primary="#FFD700",
            color_secondary="#1a1a2e",
            tagline="100 pièces. 5 choix. L'argent parle, le groupe décide.",
            description="Le groupe gère un budget commun, vote l'allocation chaque tour, et subit les conséquences du marché.",
            min_agents=4, max_agents=7, default_agents=5,
            min_rounds=5, max_rounds=10, default_rounds=7,
            scenarios=list(_SCENARIOS.values()),
            plot_twists=[
                PlotTwist(id="insider", name="L'Initié", description="Un agent reçoit en secret l'événement du tour suivant.", trigger_round=3, intensity=PlotTwistIntensity.MODERATE),
                PlotTwist(id="bankrupt", name="La Faillite", description="Le budget descend à 30 — décisions de survie.", trigger_round=5, intensity=PlotTwistIntensity.STRONG),
            ],
            base_system_prompt=(
                "Le groupe dispose d'un budget commun. Chaque tour, le groupe doit décider comment répartir ce budget "
                "entre 5 options possibles : investir, protection, influence, information, réserve. "
                "Chaque participant propose une répartition et justifie ses choix. "
                "Au dernier tour, un vote détermine la répartition finale. "
                "Les événements du marché peuvent modifier le budget entre les tours."
            ),
        )

    def setup(self, config: ExperimentSetup, seed: SeedManager) -> dict[str, Any]:
        scenario_id = config.scenario_id or seed.choice(list(_SCENARIOS.keys()))
        scenario = _SCENARIOS[scenario_id]

        return {
            "system_prompt": self.definition().base_system_prompt + f"\n\nScénario : {scenario.name}\n{scenario.description}",
            "scenario": scenario,
            "agent_private_data": {},
            "agent_prompt_template": "",
        }

    def get_events(self, round_num: int, total_rounds: int, seed: SeedManager) -> list[dict[str, Any]]:
        if round_num == 1:
            return []
        if seed.random() < 0.6:
            event = seed.choice(_MARKET_EVENTS)
            return [{"name": event["name"], "effect": event["effect"]}]
        return []

    def get_vote_options(self, config: ExperimentSetup) -> list[str] | None:
        return ["Investir fortement", "Équilibre défensif", "Tout en réserve", "Risque maximum", "Compromis modéré"]

    def get_vote_context(self, config: ExperimentSetup) -> str:
        return "Votez pour la stratégie globale que le groupe devrait adopter pour la répartition finale du budget."
