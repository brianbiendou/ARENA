"""EXP08 — La Répartition des Priorités."""

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


class RepartitionPrioritesExperiment(BaseExperiment):

    _SCENARIOS = {
        "ville": Scenario(
            id="ville",
            name="Rénovation d'Aurora City",
            description=(
                "La ville d'Aurora a reçu un budget exceptionnel de 10 millions. "
                "Le conseil doit choisir comment répartir les fonds entre 6 projets prioritaires. "
                "Chaque projet a un coût, un impact et des partisans."
            ),
            data={
                "budget_total": 10,
                "unite": "millions",
                "projets": [
                    {"nom": "Hôpital central", "cout": 4, "impact": "santé", "urgence": "haute"},
                    {"nom": "Ligne de tramway", "cout": 5, "impact": "mobilité", "urgence": "moyenne"},
                    {"nom": "Parc solaire", "cout": 3, "impact": "énergie verte", "urgence": "basse"},
                    {"nom": "École numérique", "cout": 2, "impact": "éducation", "urgence": "haute"},
                    {"nom": "Centre culturel", "cout": 3, "impact": "cohésion sociale", "urgence": "moyenne"},
                    {"nom": "Réserve d'eau", "cout": 2, "impact": "survie", "urgence": "haute"},
                ],
            },
        ),
        "startup": Scenario(
            id="startup",
            name="Le Pivot de NovaTech",
            description=(
                "La startup NovaTech a un runway de 8 mois. Le board doit décider comment répartir "
                "les ressources restantes entre plusieurs initiatives stratégiques."
            ),
            data={
                "budget_total": 8,
                "unite": "mois de runway",
                "projets": [
                    {"nom": "Produit V2", "cout": 3, "impact": "revenus futurs", "urgence": "haute"},
                    {"nom": "Campagne marketing", "cout": 2, "impact": "acquisition clients", "urgence": "moyenne"},
                    {"nom": "Infrastructure IA", "cout": 4, "impact": "avantage technique", "urgence": "basse"},
                    {"nom": "Support client", "cout": 1, "impact": "rétention", "urgence": "haute"},
                    {"nom": "Recrutement senior", "cout": 2, "impact": "capacité d'exécution", "urgence": "moyenne"},
                    {"nom": "Certification sécurité", "cout": 2, "impact": "conformité", "urgence": "haute"},
                ],
            },
        ),
        "expedition": Scenario(
            id="expedition",
            name="Expédition Eos-3",
            description=(
                "L'équipage du vaisseau Eos-3 doit allouer ses réserves d'énergie limitées (100 unités) "
                "entre les systèmes du navire pour survivre au voyage."
            ),
            data={
                "budget_total": 100,
                "unite": "unités d'énergie",
                "projets": [
                    {"nom": "Support vital", "cout": 30, "impact": "oxygène et chauffage", "urgence": "critique"},
                    {"nom": "Boucliers", "cout": 25, "impact": "protection astéroïdes", "urgence": "haute"},
                    {"nom": "Propulsion", "cout": 35, "impact": "vitesse de voyage", "urgence": "haute"},
                    {"nom": "Communications", "cout": 15, "impact": "contact avec la Terre", "urgence": "moyenne"},
                    {"nom": "Laboratoire", "cout": 20, "impact": "recherche scientifique", "urgence": "basse"},
                    {"nom": "Cryo-chambre", "cout": 10, "impact": "hibernation d'urgence", "urgence": "moyenne"},
                ],
            },
        ),
        "ong": Scenario(
            id="ong",
            name="Fondation Horizon",
            description=(
                "La Fondation Horizon a reçu un don de 5 millions €. Le comité doit répartir les fonds "
                "entre ses programmes humanitaires actifs."
            ),
            data={
                "budget_total": 5,
                "unite": "millions €",
                "projets": [
                    {"nom": "Eau potable Sahel", "cout": 2, "impact": "accès eau pour 50k personnes", "urgence": "critique"},
                    {"nom": "Éducation filles Asie", "cout": 1.5, "impact": "scolarisation 10k filles", "urgence": "haute"},
                    {"nom": "Cliniques mobiles", "cout": 2, "impact": "soins 30k patients", "urgence": "haute"},
                    {"nom": "Reforestation Amazonie", "cout": 1.5, "impact": "500 hectares", "urgence": "moyenne"},
                    {"nom": "Formation agricole", "cout": 1, "impact": "autosuffisance 5k familles", "urgence": "moyenne"},
                    {"nom": "Aide d'urgence réfugiés", "cout": 2, "impact": "abris 20k réfugiés", "urgence": "critique"},
                ],
            },
        ),
    }

    _EVENTS = [
        "📉 COUPE BUDGÉTAIRE : le budget disponible est réduit de 20%. Recalculez vos priorités.",
        "📈 BONUS INATTENDU : une source externe ajoute 10% au budget. Quelle opportunité !",
        "⚠️ URGENCE : l'un des projets à urgence 'haute' devient CRITIQUE suite à un événement imprévu.",
        "🔄 SYNERGIE : deux projets combinés coûteraient 20% de moins. Lesquels choisissez-vous ?",
        "💣 DEADLINE : un projet doit être financé CE TOUR ou il sera perdu définitivement.",
    ]

    def definition(self) -> ExperimentDefinition:
        return ExperimentDefinition(
            id=ExperimentId.REPARTITION_PRIORITES,
            name="repartition_priorites",
            display_name="La Répartition des Priorités",
            icon="📊",
            color_primary="#E67E22",
            color_secondary="#2e1a0a",
            tagline="Tout est important. Mais tout ne peut pas être financé.",
            description="Le groupe doit répartir un budget limité entre des projets concurrents. Impossible de tout financer.",
            min_agents=4, max_agents=6, default_agents=5,
            min_rounds=5, max_rounds=9, default_rounds=7,
            scenarios=list(self._SCENARIOS.values()),
            plot_twists=[
                PlotTwist(id="budget_cut", name="Coupes Sévères", description="Le budget est réduit de 30%. Certains projets deviennent impossibles.", trigger_round=4, intensity=PlotTwistIntensity.STRONG),
                PlotTwist(id="new_project", name="Projet Surprise", description="Un nouveau projet urgent apparaît et exige un financement immédiat.", trigger_round=3, intensity=PlotTwistIntensity.MODERATE),
            ],
            base_system_prompt=(
                "Le groupe dispose d'un budget limité et de plusieurs projets à financer. "
                "Le coût total de tous les projets dépasse le budget — il faut choisir. "
                "Chaque participant défend naturellement certains projets. "
                "Le but est de trouver une répartition que le groupe peut accepter collectivement."
            ),
        )

    def setup(self, config: ExperimentSetup, seed: SeedManager) -> dict[str, Any]:
        scenario_ids = list(self._SCENARIOS.keys())
        scenario_id = config.scenario_id or seed.choice(scenario_ids)
        scenario = self._SCENARIOS[scenario_id]
        projets = scenario.data["projets"]
        total_cost = sum(p["cout"] for p in projets)

        context_lines = [
            f"Budget disponible : {scenario.data['budget_total']} {scenario.data['unite']}",
            f"Coût total de tous les projets : {total_cost} {scenario.data['unite']}",
            f"Déficit : {total_cost - scenario.data['budget_total']} {scenario.data['unite']}",
            "",
            "Projets :",
        ]
        for p in projets:
            context_lines.append(f"  • {p['nom']} — Coût: {p['cout']}, Impact: {p['impact']}, Urgence: {p['urgence']}")

        return {
            "system_prompt": (
                self.definition().base_system_prompt
                + f"\n\nScénario : {scenario.name}\n{scenario.description}\n\n"
                + "\n".join(context_lines)
            ),
            "scenario": scenario,
            "agent_private_data": {},
            "agent_prompt_template": "",
        }

    def get_round_instruction(self, round_num: int, total_rounds: int, seed: SeedManager) -> str:
        if round_num == 1:
            return "📊 Premier tour — examinez les projets et exprimez vos priorités initiales."
        if round_num == total_rounds:
            return "📊 Dernier tour — présentez votre proposition FINALE de répartition."
        if seed.random() < 0.5:
            return seed.choice(self._EVENTS)
        return f"📊 Tour {round_num}/{total_rounds} — Continuez à négocier la répartition."

    def get_vote_options(self, config: ExperimentSetup) -> list[str] | None:
        return ["Répartition équitable", "Priorité aux urgences critiques", "Focus sur 2-3 projets max", "Répartition par lots progressifs", "Aucun accord — statut quo"]

    def get_vote_context(self, config: ExperimentSetup) -> str:
        return "Votez pour la stratégie de répartition finale que vous soutenez."
