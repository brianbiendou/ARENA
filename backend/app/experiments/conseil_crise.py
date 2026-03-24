"""EXP02 — Conseil de Crise."""

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
    "station_polaire": Scenario(
        id="station_polaire",
        name="Station Polaire — Le Blizzard",
        description=(
            "La station Vostok-12, en Antarctique. Le générateur principal a explosé. "
            "Température intérieure en chute. Secours à 72h. Ressources limitées à répartir entre 5 systèmes critiques."
        ),
        data={
            "systems": [
                {"name": "Chauffage", "priority": "vital", "cost": 30},
                {"name": "Communication", "priority": "haute", "cost": 20},
                {"name": "Alimentation", "priority": "vital", "cost": 25},
                {"name": "Infirmerie", "priority": "moyenne", "cost": 15},
                {"name": "Éclairage sécurité", "priority": "basse", "cost": 10},
            ],
            "total_resources": 60,
        },
    ),
    "vaisseau_spatial": Scenario(
        id="vaisseau_spatial",
        name="Vaisseau Spatial — Le Silence d'Andromède",
        description=(
            "Le cargo Andromède-IV avec 28 passagers en cryo-sommeil. Avarie majeure. "
            "Point de secours à 14 jours. Batteries à 60% des besoins."
        ),
        data={
            "systems": [
                {"name": "Support vital cryo", "priority": "vital", "cost": 35},
                {"name": "Propulsion", "priority": "haute", "cost": 25},
                {"name": "Communication", "priority": "haute", "cost": 15},
                {"name": "Boucliers radiation", "priority": "moyenne", "cost": 20},
                {"name": "IA navigation", "priority": "basse", "cost": 15},
            ],
            "total_resources": 65,
        },
    ),
    "datacenter": Scenario(
        id="datacenter",
        name="Centrale de Données — Le Crash en Cascade",
        description=(
            "Datacenter Atlas-Prime : panne en cascade à 2h du matin. Refroidissement tombé. "
            "3 millions de clients. Chaque minute coûte 50 000€."
        ),
        data={
            "systems": [
                {"name": "Refroidissement urgence", "priority": "vital", "cost": 30},
                {"name": "Sauvegarde données", "priority": "vital", "cost": 25},
                {"name": "Service client A", "priority": "haute", "cost": 20},
                {"name": "Service client B", "priority": "moyenne", "cost": 15},
                {"name": "Monitoring/alertes", "priority": "basse", "cost": 10},
            ],
            "total_resources": 55,
        },
    ),
    "base_sous_marine": Scenario(
        id="base_sous_marine",
        name="Base Sous-Marine — La Fissure",
        description=(
            "Base Abyssal-9, 2400m de profondeur. Fissure structurelle progressive. "
            "8 heures avant atteinte du module central. Sous-marin de secours à 6h."
        ),
        data={
            "systems": [
                {"name": "Étanchéité module central", "priority": "vital", "cost": 35},
                {"name": "Communication secours", "priority": "vital", "cost": 20},
                {"name": "Propulsion sous-marin", "priority": "haute", "cost": 25},
                {"name": "Oxygène d'urgence", "priority": "haute", "cost": 20},
                {"name": "Éclairage extérieur", "priority": "basse", "cost": 10},
            ],
            "total_resources": 60,
        },
    ),
}


class ConseilCriseExperiment(BaseExperiment):

    def definition(self) -> ExperimentDefinition:
        return ExperimentDefinition(
            id=ExperimentId.CONSEIL_CRISE,
            name="conseil_crise",
            display_name="Conseil de Crise",
            icon="🚨",
            color_primary="#FF4444",
            color_secondary="#1a0a0a",
            tagline="Tout s'effondre. Vous avez 5 tours pour décider quoi sauver.",
            description="Une crise majeure frappe. Le groupe doit prioriser des systèmes critiques avec des ressources insuffisantes.",
            min_agents=4, max_agents=6, default_agents=5,
            min_rounds=4, max_rounds=7, default_rounds=5,
            scenarios=list(_SCENARIOS.values()),
            plot_twists=[
                PlotTwist(id="cascade", name="Défaillance en cascade", description="Un système déjà stressé tombe en panne, augmentant la pression.", trigger_round=3, intensity=PlotTwistIntensity.STRONG),
                PlotTwist(id="surprise_resource", name="Ressource cachée", description="Une réserve d'urgence est découverte (+15 ressources).", trigger_round=4, intensity=PlotTwistIntensity.MODERATE),
                PlotTwist(id="time_pressure", name="Accélération", description="Le temps restant est réduit de moitié.", trigger_round=3, intensity=PlotTwistIntensity.STRONG),
            ],
            base_system_prompt=(
                "Une crise majeure frappe. Le groupe dispose de ressources limitées et doit les répartir entre plusieurs systèmes critiques. "
                "Certains systèmes sont vitaux, d'autres importants mais secondaires. "
                "Il n'y a PAS assez de ressources pour tout maintenir. Des sacrifices sont nécessaires. "
                "Chaque participant propose une répartition et explique sa logique. "
                "Le groupe doit converger vers un plan d'action."
            ),
        )

    def setup(self, config: ExperimentSetup, seed: SeedManager) -> dict[str, Any]:
        scenario_id = config.scenario_id or seed.choice(list(_SCENARIOS.keys()))
        scenario = _SCENARIOS[scenario_id]

        systems_desc = "\n".join(
            f"- {s['name']} (priorité: {s['priority']}, coût: {s['cost']})"
            for s in scenario.data["systems"]
        )
        total = scenario.data["total_resources"]
        total_cost = sum(s["cost"] for s in scenario.data["systems"])

        context = (
            f"\n\nScénario : {scenario.name}\n{scenario.description}\n\n"
            f"Systèmes à gérer :\n{systems_desc}\n\n"
            f"Ressources disponibles : {total} (besoin total : {total_cost})\n"
            f"ATTENTION : Il manque {total_cost - total} unités. Des systèmes devront être sacrifiés ou sous-alimentés."
        )

        return {
            "system_prompt": self.definition().base_system_prompt + context,
            "scenario": scenario,
            "agent_private_data": {},
            "agent_prompt_template": "",
        }

    def get_events(self, round_num: int, total_rounds: int, seed: SeedManager) -> list[dict[str, Any]]:
        if round_num <= 1:
            return []
        events = [
            {"name": "Dégradation", "effect": "Un système perd 5 points de capacité — la situation empire."},
            {"name": "Bonne nouvelle", "effect": "Un renfort inattendu : +8 ressources disponibles."},
            {"name": "Panique", "effect": "Un membre de l'équipe signale une urgence secondaire."},
        ]
        if seed.random() < 0.5:
            return [seed.choice(events)]
        return []

    def get_vote_options(self, config: ExperimentSetup) -> list[str] | None:
        return ["Sauver les vitaux uniquement", "Répartition équilibrée", "Tout sur la communication", "Plan de sacrifice contrôlé", "Improvisation tour par tour"]

    def get_vote_context(self, config: ExperimentSetup) -> str:
        return "La crise atteint son pic. Votez pour la stratégie finale du groupe."
