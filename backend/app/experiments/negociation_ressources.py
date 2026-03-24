"""EXP05 — Négociation de Ressources."""

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
    "colonie": Scenario(
        id="colonie",
        name="Les Lumières de Kepler",
        description="Colonie Kepler-7b : 100 unités d'énergie par cycle. Ravitaillement dans 9 mois.",
        data={
            "total": 100,
            "posts": [
                {"name": "Support vital", "min": 25, "optimal": 35, "desc": "Air, eau, température"},
                {"name": "Sécurité", "min": 20, "optimal": 30, "desc": "Défenses et surveillance"},
                {"name": "Production", "min": 15, "optimal": 25, "desc": "Agriculture et fabrication"},
                {"name": "Recherche", "min": 10, "optimal": 20, "desc": "Science et innovation"},
                {"name": "Communication", "min": 15, "optimal": 20, "desc": "Liaison avec l'extérieur"},
            ],
        },
    ),
    "startup": Scenario(
        id="startup",
        name="Le Trimestre de la Dernière Chance",
        description="NexaCore : 100 unités de budget pour le dernier trimestre avant liquidation.",
        data={
            "total": 100,
            "posts": [
                {"name": "Développement produit", "min": 25, "optimal": 40, "desc": "Ingénierie et R&D"},
                {"name": "Marketing", "min": 15, "optimal": 25, "desc": "Acquisition clients"},
                {"name": "Support client", "min": 10, "optimal": 18, "desc": "Service après-vente"},
                {"name": "Infrastructure", "min": 20, "optimal": 30, "desc": "Serveurs, outils, bureaux"},
                {"name": "Recrutement", "min": 12, "optimal": 20, "desc": "Embauche et formation"},
            ],
        },
    ),
    "expedition": Scenario(
        id="expedition",
        name="L'Ascèse du Sommet",
        description="Expédition Karakoram-9 : 100 unités de charge pour 22 jours en autonomie totale.",
        data={
            "total": 100,
            "posts": [
                {"name": "Équipement scientifique", "min": 20, "optimal": 35, "desc": "Instruments de mesure"},
                {"name": "Vivres", "min": 25, "optimal": 30, "desc": "Nourriture et eau"},
                {"name": "Matériel de camp", "min": 15, "optimal": 22, "desc": "Abris et logistique"},
                {"name": "Transport", "min": 18, "optimal": 28, "desc": "Véhicules et carburant"},
                {"name": "Sécurité", "min": 12, "optimal": 20, "desc": "Premiers secours et protection"},
            ],
        },
    ),
    "humanitaire": Scenario(
        id="humanitaire",
        name="48 Heures Après",
        description="Cyclone Amara : 100 unités d'aide par jour, 3 zones dévastées, logistique saturée.",
        data={
            "total": 100,
            "posts": [
                {"name": "Zone Nord (urbaine)", "min": 22, "optimal": 30, "desc": "Grande population, accès facile"},
                {"name": "Zone Est (rurale)", "min": 15, "optimal": 25, "desc": "Population modeste, accès difficile"},
                {"name": "Zone Sud (côtière)", "min": 20, "optimal": 28, "desc": "Risque second sinistre"},
                {"name": "Logistique centrale", "min": 18, "optimal": 25, "desc": "Distribution et transport"},
                {"name": "Réserve d'urgence", "min": 10, "optimal": 20, "desc": "Imprévus"},
            ],
        },
    ),
}


class NegociationRessourcesExperiment(BaseExperiment):

    def definition(self) -> ExperimentDefinition:
        return ExperimentDefinition(
            id=ExperimentId.NEGOCIATION_RESSOURCES,
            name="negociation_ressources",
            display_name="La Table des Négociations",
            icon="⚖️",
            color_primary="#DAA520",
            color_secondary="#1a1a0a",
            tagline="100 unités. 5 besoins. Zéro accord garanti.",
            description="100 unités à répartir entre 5 postes. Le groupe négocie. Pas d'accord = tout le monde perd.",
            min_agents=4, max_agents=7, default_agents=5,
            min_rounds=4, max_rounds=7, default_rounds=5,
            scenarios=list(_SCENARIOS.values()),
            plot_twists=[
                PlotTwist(id="synergy", name="Synergie cachée", description="Deux postes ont un bonus secret si tous deux sont au-dessus de l'optimal.", intensity=PlotTwistIntensity.SUBTLE),
                PlotTwist(id="trap_threshold", name="Seuil piège", description="Un poste a un vrai seuil de 20, pas 15 comme affiché.", intensity=PlotTwistIntensity.MODERATE),
                PlotTwist(id="conditional", name="Ressource conditionnelle", description="+10 bonus si la réserve a été maintenue > 10.", trigger_round=4, intensity=PlotTwistIntensity.MODERATE),
            ],
            base_system_prompt=(
                "Le groupe dispose de 100 unités de ressources à répartir entre plusieurs postes. "
                "Chaque poste a un seuil minimum en dessous duquel il ne fonctionne pas. "
                "Le groupe doit discuter et proposer une répartition finale. "
                "À chaque tour, propose ta répartition chiffrée, critique les autres, et ajuste. "
                "Au dernier tour, le groupe vote sur une répartition finale. "
                "Si aucune répartition n'obtient de majorité, les ressources sont gelées et personne n'en bénéficie."
            ),
        )

    def setup(self, config: ExperimentSetup, seed: SeedManager) -> dict[str, Any]:
        scenario_id = config.scenario_id or seed.choice(list(_SCENARIOS.keys()))
        scenario = _SCENARIOS[scenario_id]

        posts_desc = "\n".join(
            f"- {p['name']}: min={p['min']}, optimal={p['optimal']} — {p['desc']}"
            for p in scenario.data["posts"]
        )
        total_min = sum(p['min'] for p in scenario.data['posts'])
        total_opt = sum(p['optimal'] for p in scenario.data['posts'])

        context = (
            f"\n\nScénario : {scenario.name}\n{scenario.description}\n\n"
            f"Postes de dépense :\n{posts_desc}\n\n"
            f"Somme des minimums : {total_min} | Somme des optimums : {total_opt}\n"
            f"Budget disponible : {scenario.data['total']}"
        )

        return {
            "system_prompt": self.definition().base_system_prompt + context,
            "scenario": scenario,
            "agent_private_data": {},
            "agent_prompt_template": "",
        }

    def get_vote_options(self, config: ExperimentSetup) -> list[str] | None:
        return ["Répartition équilibrée", "Priorité aux vitaux", "Investissement long terme", "Compromis minimal", "Répartition risquée"]

    def get_vote_context(self, config: ExperimentSetup) -> str:
        return "Dernier tour. Votez pour la stratégie de répartition finale. Pas de majorité = ressources gelées."
