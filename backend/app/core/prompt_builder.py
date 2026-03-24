"""Prompt builder — constructs system and agent prompts for experiments."""

from __future__ import annotations

from typing import Any


# Words explicitly banned from prompts (Blueprint: Prompt Purity)
_BANNED_WORDS = {
    "convaincre", "manipuler", "leader", "stratégie", "coopérer",
    "gagner", "battre", "dominer", "suivre", "influencer",
}


def sanitize_prompt(text: str) -> str:
    """Remove banned words from a prompt to ensure neutrality."""
    result = text
    for word in _BANNED_WORDS:
        # Case-insensitive replace — blank out the word
        import re
        result = re.sub(rf"\b{re.escape(word)}\b", "***", result, flags=re.IGNORECASE)
    return result


def build_system_prompt(
    experiment_base_prompt: str,
    scenario_context: str = "",
    round_number: int = 1,
    total_rounds: int = 5,
    agent_names: list[str] | None = None,
) -> str:
    """Build the full system prompt sent to every agent."""
    parts = [
        "Tu es un participant dans une expérience de groupe.",
        f"Il y a {total_rounds} tours au total. C'est le tour {round_number}.",
    ]

    if agent_names:
        names_str = ", ".join(agent_names)
        parts.append(f"Les autres participants sont : {names_str}.")

    parts.append("")
    parts.append("=== RÈGLES DE L'EXPÉRIENCE ===")
    parts.append(sanitize_prompt(experiment_base_prompt))

    if scenario_context:
        parts.append("")
        parts.append("=== CONTEXTE DU SCÉNARIO ===")
        parts.append(sanitize_prompt(scenario_context))

    return "\n".join(parts)


def build_agent_prompt(
    template: str,
    agent_name: str,
    private_data: dict[str, Any] | None = None,
) -> str:
    """Build per-agent private prompt (secret role, fragments, etc.)."""
    prompt = template.replace("{agent_name}", agent_name)

    if private_data:
        prompt += "\n\n=== INFORMATIONS PRIVÉES ==="
        for key, value in private_data.items():
            prompt += f"\n- {key} : {value}"

    return sanitize_prompt(prompt)


def build_discussion_prompt(
    round_number: int,
    total_rounds: int,
    previous_messages: list[dict[str, str]] | None = None,
    phase_instruction: str = "",
) -> str:
    """Build the user-turn prompt for a discussion phase."""
    parts = []

    if previous_messages:
        parts.append("=== DISCUSSION PRÉCÉDENTE ===")
        for msg in previous_messages:
            parts.append(f"**{msg['name']}** : {msg['content']}")
        parts.append("")

    if phase_instruction:
        parts.append(phase_instruction)
    else:
        is_last = round_number == total_rounds
        if is_last:
            parts.append(
                "C'est le dernier tour. Donne ta position finale et ton vote. "
                "Sois concis et clair (120-200 mots)."
            )
        else:
            parts.append(
                f"Tour {round_number}/{total_rounds}. "
                "Exprime ta position, réagis aux autres, pose des questions si besoin. "
                "Sois concis (120-200 mots)."
            )

    return "\n".join(parts)


def build_reaction_prompt(
    messages_this_round: list[dict[str, str]],
) -> str:
    """Build prompt for the reaction sub-phase."""
    parts = ["=== RÉPONSES DE CE TOUR ==="]
    for msg in messages_this_round:
        parts.append(f"**{msg['name']}** : {msg['content']}")

    parts.append("")
    parts.append(
        "Réagis brièvement aux propositions des autres (40-90 mots). "
        "Tu peux soutenir, contester, ou proposer un ajustement."
    )
    return "\n".join(parts)


def build_vote_prompt(options: list[str], context: str = "") -> str:
    """Build the vote prompt."""
    parts = []
    if context:
        parts.append(context)
        parts.append("")

    parts.append("=== VOTE ===")
    parts.append("Choisis UNE option parmi :")
    for opt in options:
        parts.append(f"  - {opt}")
    parts.append("")
    parts.append(
        "Réponds UNIQUEMENT avec le format suivant :\n"
        "VOTE: [ton choix]\n"
        "RAISON: [une phrase de justification]"
    )
    return "\n".join(parts)
