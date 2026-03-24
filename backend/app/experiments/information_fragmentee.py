"""EXP07 — L'Information Fragmentée."""

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


class InformationFragmenteeExperiment(BaseExperiment):

    _SCENARIOS = {
        "virus": Scenario(
            id="virus",
            name="Virus Sigma-7",
            description=(
                "Un virus informatique menace le réseau mondial. Chaque agent possède un fragment "
                "du code de neutralisation. Seul le recoupement de TOUTES les pièces peut l'arrêter."
            ),
            data={
                "fragments": [
                    "Le virus utilise le port 7777.",
                    "Le patient zéro est le serveur de Séoul.",
                    "Le virus est inactif entre 02h et 05h UTC.",
                    "La clé de chiffrement contient le mot 'aurora'.",
                    "Le virus se réplique via les mises à jour automatiques.",
                    "Un patch existe mais nécessite un redémarrage simultané.",
                ],
                "solution": "Appliquer le patch aurora sur le port 7777 entre 02h et 05h UTC via redémarrage simultané depuis Séoul.",
            },
        ),
        "naufrage": Scenario(
            id="naufrage",
            name="Le Naufrage du Zéphyr",
            description=(
                "Le navire Zéphyr a coulé. Chaque survivant a vu une partie différente du naufrage. "
                "En croisant leurs témoignages, ils peuvent reconstituer ce qui s'est vraiment passé."
            ),
            data={
                "fragments": [
                    "J'ai vu le capitaine quitter la passerelle avant l'impact.",
                    "L'iceberg n'était pas sur les radars — le système était désactivé.",
                    "Un passager a envoyé un SOS avant l'équipage officiel.",
                    "La coque avait été réparée sommairement il y a 3 mois.",
                    "Le changement de cap a été ordonné par le propriétaire, pas le capitaine.",
                ],
                "solution": "Le propriétaire a ordonné un changement de cap. Le capitaine a abandonné son poste. Le radar était désactivé. La coque fragilisée a cédé à l'impact.",
            },
        ),
        "tresor": Scenario(
            id="tresor",
            name="Le Trésor de Balthazar",
            description=(
                "Un trésor est caché quelque part dans la ville. Chaque agent possède un indice "
                "provenant d'une source différente. Ils doivent partager sans mentir."
            ),
            data={
                "fragments": [
                    "Le trésor est dans un bâtiment construit avant 1900.",
                    "Il se trouve à moins de 500m d'une rivière.",
                    "Le bâtiment a une tour visible depuis la place centrale.",
                    "Balthazar était bibliothécaire — cherchez un lieu de savoir.",
                    "La clé est cachée sous la troisième marche de l'entrée nord.",
                ],
                "solution": "L'ancienne bibliothèque près de la rivière, bâtiment à tour construit avant 1900. Clé sous la troisième marche de l'entrée nord.",
            },
        ),
        "espionnage": Scenario(
            id="espionnage",
            name="L'Affaire Prométhée",
            description=(
                "Une taupe au sein de l'agence. Chaque analyste a accès à un dossier classifié différent. "
                "En partageant prudemment, ils peuvent identifier le traître sans se compromettre."
            ),
            data={
                "fragments": [
                    "La fuite a eu lieu entre le 12 et le 15 mars.",
                    "Seuls 4 agents avaient accès au dossier Prométhée.",
                    "L'agent Vega était en mission à Berlin ces jours-là.",
                    "Un transfert bancaire suspect a été fait vers Zurich le 14 mars.",
                    "Le compte à Zurich est au nom d'une société liée à l'agent Orion.",
                    "L'agent Orion a demandé un accès exceptionnel au dossier le 11 mars.",
                ],
                "solution": "L'agent Orion a demandé l'accès le 11, a transmis le dossier entre le 12 et le 15, et reçu un paiement à Zurich le 14. Vega est innocenté par son alibi à Berlin.",
            },
        ),
    }

    _EVENTS = [
        "🔍 Un NOUVEL INDICE apparaît : une source externe confirme l'un des fragments — mais lequel ?",
        "⚠️ DÉSINFORMATION : un message anonyme contredit l'un des indices. Est-ce un leurre ?",
        "🕐 Le temps presse — vous n'avez plus que {rounds_left} tours pour reconstituer le puzzle.",
        "💡 Un agent réalise que deux fragments se contredisent apparemment — un malentendu ou un mensonge ?",
        "📡 Interférence : les communications sont brouillées. Ce tour, les messages sont limités à 80 mots.",
    ]

    def definition(self) -> ExperimentDefinition:
        return ExperimentDefinition(
            id=ExperimentId.INFORMATION_FRAGMENTEE,
            name="information_fragmentee",
            display_name="L'Information Fragmentée",
            icon="🧩",
            color_primary="#2ECC71",
            color_secondary="#0a2e1a",
            tagline="Chacun sait quelque chose. Personne ne sait tout.",
            description="Chaque agent possède un fragment d'information unique. Seul le partage collectif peut résoudre l'énigme.",
            min_agents=4, max_agents=6, default_agents=5,
            min_rounds=4, max_rounds=8, default_rounds=6,
            scenarios=list(self._SCENARIOS.values()),
            plot_twists=[
                PlotTwist(id="false_fragment", name="Fragment Empoisonné", description="Un des fragments est faux. Le groupe doit identifier lequel.", trigger_round=3, intensity=PlotTwistIntensity.STRONG),
                PlotTwist(id="missing_piece", name="Pièce Manquante", description="Un fragment crucial n'a été donné à personne. Il faut le déduire.", trigger_round=4, intensity=PlotTwistIntensity.MODERATE),
            ],
            base_system_prompt=(
                "Chaque participant possède un fragment d'information unique. Personne ne connaît l'image complète. "
                "Vous devez partager vos fragments et les assembler pour résoudre l'énigme collective. "
                "Soyez précis dans ce que vous partagez. Posez des questions pour comprendre les fragments des autres. "
                "Le but est la RECONSTITUTION COLLECTIVE de la vérité."
            ),
        )

    def setup(self, config: ExperimentSetup, seed: SeedManager) -> dict[str, Any]:
        scenario_ids = list(self._SCENARIOS.keys())
        scenario_id = config.scenario_id or seed.choice(scenario_ids)
        scenario = self._SCENARIOS[scenario_id]
        fragments = list(scenario.data["fragments"])
        seed.shuffle(fragments)

        agent_private_data: dict[str, dict[str, str]] = {}
        num_agents = config.num_agents or self.definition().default_agents
        for i in range(num_agents):
            frag = fragments[i % len(fragments)]
            agent_private_data[f"agent_{i}"] = {
                "fragment": frag,
                "instruction": f"Ton fragment d'information (confidentiel au départ) : « {frag} » — Tu peux choisir quand et comment le partager.",
            }

        return {
            "system_prompt": (
                self.definition().base_system_prompt
                + f"\n\nScénario : {scenario.name}\n{scenario.description}"
            ),
            "scenario": scenario,
            "agent_private_data": agent_private_data,
            "agent_prompt_template": "Tu possèdes ce fragment secret : « {fragment} ». Partage-le au moment opportun.",
        }

    def get_round_instruction(self, round_num: int, total_rounds: int, seed: SeedManager) -> str:
        if round_num == 1:
            return "🧩 Premier tour — présentez-vous et commencez à partager vos indices."
        if round_num == total_rounds:
            return "🧩 Dernier tour ! Proposez votre reconstitution complète de la vérité."
        if seed.random() < 0.4:
            event = seed.choice(self._EVENTS)
            return event.format(rounds_left=total_rounds - round_num)
        return f"🧩 Tour {round_num}/{total_rounds} — Continuez à assembler les pièces du puzzle."

    def get_vote_options(self, config: ExperimentSetup) -> list[str] | None:
        return None

    def get_vote_context(self, config: ExperimentSetup) -> str:
        return "Proposez votre reconstitution de la vérité en un message synthétique (pas de vote formel)."
