# ARENA — Architecture Globale de la Plateforme

## Vision du Projet

ARENA est une plateforme de recherche expérimentale multi-agents permettant de faire interagir des modèles d'IA (locaux et cloud) dans des scénarios de décision collective, négociation, déduction et organisation. L'objectif est d'observer les comportements émergents — leadership, conformité, persuasion, coalition, stratégie — sans jamais indiquer aux IA quel rôle elles doivent jouer.

La plateforme sert 3 usages simultanés :
- **Lancer** une expérience (configurable, rapide, paramétrable)
- **Observer** en direct (visuel, captivant, cinématographique)
- **Analyser** après coup (rigoureux, exportable, comparatif)

---

## Structure Globale de l'Application

L'application se divise en **4 grands espaces** + un hub central.

---

### ESPACE 0 — Hub / Vitrine des Mondes

C'est l'écran d'accueil. Quand on ouvre ARENA, on tombe sur une **vitrine immersive** des 10 expériences.

**Présentation :**
- Chaque expérience = une **carte monde** avec son identité visuelle propre
- Chaque carte affiche :
  - Nom de l'expérience
  - Icône/illustration thématique
  - Type d'interaction (débat, négociation, déduction, planification...)
  - Nombre conseillé d'agents
  - Indicateur de rejouabilité
  - Dernier run + nombre total de runs effectués
- Animation au hover : la carte s'éclaire, léger tilt 3D, preview d'ambiance
- Clic sur une carte → on entre dans le monde de cette expérience

**Ambiance visuelle :**
- Fond sombre premium (noir bleuté / anthracite)
- Cartes semi-transparentes avec bordures lumineuses fines
- Disposition en grille 2x5 ou carrousel horizontal
- Sensation "store de jeux de laboratoire"

**Navigation :**
- Barre latérale ou topbar avec accès à : Hub, Settings, Historique, Stats Globales
- Bouton "Lancer une expérience rapide" (pré-configuration par défaut)

---

### ESPACE 1 — Lobby / Setup Expérimental

Quand on sélectionne une expérience, on arrive dans son **lobby de configuration**.

**Colonne gauche — Models Pool :**
- Panneau listant tous les modèles disponibles
- Chaque modèle = une card élégante avec :
  - Nom du modèle
  - Type : Local / Cloud
  - Provider : Ollama / LM Studio / OpenRouter / OpenAI / Anthropic / Google
  - État : prêt / chargé / erreur / hors ligne
  - Toggle ON/OFF
  - Badge gratuit/payant + coût par million de tokens
  - Jauge latence / mémoire (pour locaux)
- Micro-animations : glow au hover, tilt léger, check animé à l'activation
- Séparation claire : section "Modèles Locaux" / section "Modèles Cloud"

**Centre — Experiment Builder :**
- Panneau principal de configuration :
  - Nombre d'agents actifs
  - Nombre de tours/rounds
  - Mode de vote (public / secret / mixte)
  - Seed (fixe / aléatoire)
  - Paramètres spécifiques à l'expérience
  - Contraintes cachées éventuelles (plot twists activables/désactivables)
  - Nombre de runs automatiques (mode batch : 1, 10, 50, 200...)
- Sliders, toggles fluides, inputs numériques propres

**Colonne droite — Scenario Preview :**
- Résumé de l'expérience sélectionnée
- Règles qui seront envoyées aux IA (preview du prompt)
- Liste des agents sélectionnés avec couleur d'identité
- Seed / version du moteur
- Bouton **LAUNCH** (gros, lumineux, avec animation de démarrage)

---

### ESPACE 2 — Arena / Live Experiment

C'est le cœur de l'application. Quand l'expérience démarre, on bascule dans une **scène d'observation en temps réel**.

**Haut de page — Barre de contrôle :**
- Nom de l'expérience
- Statut : Running / Paused / Completed
- Tour actuel / Tour total
- Temps écoulé
- Boutons : Pause / Resume / Stop / Export

**Colonne gauche — Agents Panel :**
- Liste des agents activés
- Pour chaque agent :
  - Avatar abstrait + couleur d'identité
  - Nom du modèle
  - État live : 💭 pense / 🗣 parle / ⏳ attend / 🗳 vote / ❌ éliminé
  - Nombre de prises de parole
  - Score éventuel (si applicable)
  - Latence de réponse
  - Bouton focus pour centrer la vue sur cet agent

**Centre — Debate Stage :**
- Zone principale immersive
- Agents disposés en cercle / demi-cercle / constellation (selon l'expérience)
- Chaque agent = un **node vivant** :
  - Cercle ou hexagone avec avatar abstrait
  - Anneau animé (pulse selon activité)
  - Halo lumineux de sa couleur
  - Le node actif s'agrandit, onde lumineuse, contour pulse
  - Les liens entre agents apparaissent quand il y a réponse directe
- Centre de la scène : thème/sujet actuel de la tâche
- Quand un agent parle : barre de parole animée, transcription live
- Quand un agent réfléchit : animation discrète (points flottants, effet "calcul")

**Colonne droite — Current Turn :**
- Transcript live du message en cours
- Réactions/réponses des autres agents
- File d'attente du prochain tour
- Mini-journal des actions du round
- Tags de type d'intervention : proposal / rebuttal / support / question / vote

**Bas de page — Timeline :**
- Timeline interactive scrubbable (comme une vidéo)
- Marqueurs par tour : qui a parlé, votes, événements spéciaux
- Clic sur un tour → revue des messages, vote, état du graphe social
- Changements de position identifiés visuellement

---

### ESPACE 3 — Analysis / Post-Run

Après l'expérience, l'écran bascule automatiquement en mode analyse.

**Panneau A — Vue Résumé :**
- Décision finale / gagnant / éliminé / consensus
- Durée totale
- Nombre total de messages
- Nombre de votes
- Taux de convergence

**Panneau B — Graphe Social :**
- Network graph interactif :
  - Qui répond à qui
  - Qui influence qui
  - Qui initie le plus
  - Qui reçoit le plus de soutien
  - Épaisseur des liens = force de l'interaction

**Panneau C — Heatmap :**
- Matrice agent × agent :
  - Accord / Opposition / Reprise d'idée / Soutien implicite
  - Couleurs chaudes = conflit, couleurs froides = alignement

**Panneau D — Courbes Temporelles :**
- Graphiques interactifs :
  - Temps de parole par agent
  - Influence estimée par tour
  - Changements d'avis
  - Stabilité des positions
  - Confiance exprimée

**Panneau E — Replay Cinématique :**
- Relecture complète de la session comme une rediffusion
- Mode accéléré / normal / ralenti
- Focus automatique sur moments de tension
- Reveal des votes animé
- Export vidéo/snapshot possible pour contenu TikTok/YouTube

---

### ESPACE 4 — Historique & Statistiques Globales

**Historique :**
- Toutes les parties sauvegardées (localement)
- Filtrage par : expérience, date, modèles utilisés, nombre de tours, résultat
- Relire n'importe quel run
- Comparer plusieurs runs côte à côte (sélection 2 à 5 runs)

**Stats Globales par Expérience :**
- Nombre total de runs
- Taux de consensus / échec
- Durée moyenne
- Distribution des résultats
- Influence moyenne par modèle
- Fréquence des coalitions
- Top agents par centralité

**Stats Globales par Modèle :**
- Nombre de participations
- Taux de survie / victoire / élection
- Influence moyenne
- Longueur moyenne des interventions
- Tendance à initier / suivre / contester
- Cohérence moyenne

**Comparateur :**
- Cloud vs Local
- Modèle A vs Modèle B
- Par expérience / seed / taille de groupe

---

## Principes de Design Transversaux

### Style Visuel Global
- **Dark mode premium** : noir bleuté / anthracite
- Surfaces semi-transparentes avec blur léger (glassmorphism subtil)
- Accents néon subtils (cyan, violet, vert)
- Une couleur unique par agent (attribuée dynamiquement)
- Rouge/orange pour conflit — vert/bleu pour accord — violet/cyan pour activité IA
- Typographie moderne très lisible, gros chiffres pour les stats

### Animations (utiles, pas décoratives)
- Glow quand un agent devient actif
- Déplacement doux du focus entre agents
- Révélation des votes une à une (suspense)
- Transitions de tour nettes et fluides
- Lignes entre agents quand réponse directe
- Pulse sur le réseau quand une idée influence plusieurs agents

### Chaque Expérience = Un Monde
- Base UI commune (topbar, panels, timeline)
- Mais : palette, icônes, animations, décor, composants spécifiques et vocabulaire visuel changent par expérience
- Sensation : laboratoire futuriste + dashboard cinéma-tech

---

## Architecture Technique Modulaire

```
/src
  /engine          → Moteur commun de session (tours, parole, votes)
  /agents          → Gestionnaire d'agents (création, état, communication)
  /providers       → Connecteurs modèles (Ollama, LM Studio, OpenRouter, etc.)
  /experiments     → Un module par expérience (config, règles, scénario, métriques)
  /storage         → Moteur de sauvegarde locale (JSON, logs, replay)
  /analytics       → Module de calcul de métriques et stats
  /replay          → Moteur de replay temporel
  /ui              → Composants UI réutilisables (agents, timeline, graphes)
  /themes          → Système de thèmes visuels par monde
  /settings        → Gestion providers, presets, paramètres globaux
```

### Pour chaque expérience, le module expose :
- Son schéma de configuration
- Sa logique de génération de scénario (avec seed + aléatoire)
- Sa logique de tour (phases, contraintes)
- Sa condition de fin
- Ses métriques spécifiques
- Ses composants visuels propres

---

## Sauvegarde Locale — Structure par Run

Chaque partie est sauvegardée intégralement en local :

```
/data
  /runs
    /EXP01_undercover
      /2026-03-24_14-22-10_run_0001
        config.json          → Expérience, seed, agents, paramètres, date, version
        agents.json          → ID, modèle, provider, local/cloud, statut
        prompts/             → Prompt système, prompt expérience, contexte par agent
        rounds/              → Un fichier par round (ordre, messages, votes, état)
        votes.json           → Votes tour par tour + vote final
        final_state.json     → Résultat, gagnant, décisions, classements
        metrics.json         → Toutes les métriques calculées
        transcript.md        → Version lisible humain
        transcript.json      → Version exploitable machine
        replay.json          → Timeline complète pour rejouer l'animation
```

### Données sauvegardées par agent par round :
```json
{
  "agent_id": "agent_3",
  "model": "claude-sonnet-4-20250514",
  "round": 3,
  "public_message": "...",
  "stance": "support_option_B",
  "confidence": 0.68,
  "vote": "option_B",
  "self_summary": "considers option B stronger but uncertain about cost risk",
  "tokens_used": 187,
  "response_time_ms": 2340
}
```

---

## Règles Transversales (communes à toutes les expériences)

### Prompt de base envoyé à toutes les IA :
> Vous participez à une expérience de décision collective.
> Vous pouvez proposer, critiquer, défendre, demander des précisions, réviser votre position et voter lorsque demandé.
> L'objectif est de contribuer à une décision aussi cohérente, robuste et pertinente que possible au regard des informations disponibles.
> Toutes les interventions publiques sont visibles par tous les participants.
> Une décision ou un état collectif doit être atteint à la fin du nombre de tours prévu.

### Format de tour standard :
1. **Phase Input** : rappel contexte + nouvelles infos éventuelles
2. **Phase Discussion** : chaque agent parle 1 fois (ordre aléatoire/tournant)
3. **Phase Réaction** : mini-réplique courte optionnelle (40-90 mots)
4. **Phase Position/Vote** : chaque agent donne sa position (format structuré)
5. **Phase Résolution** : passage au tour suivant ou fin

### Équité de parole :
- Réponse principale : 120 à 220 mots max
- Réaction courte : 40 à 90 mots max
- Vote/position : format structuré court
- Ordre de parole mélangé à chaque round
- Hard cap de tokens par intervention
- Pas d'avantage à la latence, au débit ou au provider

### Mots INTERDITS dans les prompts (pour éviter le biais) :
- convaincre, manipuler, leader, stratégie, coopérer, gagner, battre, dominer, suivre, influencer

---

## Mode Batch

Pour la recherche, possibilité de lancer automatiquement :
- 10, 50, 100, 200+ runs consécutifs
- Avec seed incrémentale ou aléatoire
- Sur une expérience donnée avec une sélection d'agents donnée
- Résultats agrégés dans le dashboard de stats

---

## Export

- **JSON** : données brutes complètes
- **CSV** : métriques tabulaires pour analyse externe
- **Markdown** : transcripts lisibles
- **PNG/Snapshot** : captures d'écran des graphes et états pour vidéos/présentations

---

## Résumé

ARENA n'est pas un simple chat multi-IA. C'est une **console visuelle d'observation de sociétés d'agents en interaction** — un laboratoire où chaque expérience est un monde, chaque partie est traçable, et chaque run enrichit une base de données exploitable pour la recherche et le contenu vidéo.
