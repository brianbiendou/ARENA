# EXP02 — LE CONSEIL DE CRISE

## Identité
- **Nom interne :** `crisis_council`
- **Nom affiché :** "Le Conseil de Crise"
- **Icône :** 🚨
- **Couleur thème :** Rouge sombre / Orange alarme / Blanc froid
- **Tagline :** "Tout s'effondre. Vous avez peu de temps pour décider."

---

## Concept

Les agents forment un **conseil d'urgence** face à une situation critique. Un problème grave survient et ils doivent prendre des **décisions rapides avec des informations incomplètes**. Les ressources sont limitées, les choix sont interdépendants, et chaque round apporte de nouvelles complications.

Personne ne dirige. Personne n'est désigné expert. Ils doivent s'organiser, proposer, débattre et trancher — sous pression.

---

## Contexte Narratif — L'Histoire

Tu connais ce moment dans les films-catastrophe où les personnages sont réunis dans une salle, les alarmes hurlent, les écrans clignotent en rouge, et quelqu'un dit : *"On a 6 heures"* ? C'est **exactement** ce moment-là.

Sauf qu'ici, il n'y a pas de héros. Pas de commandant charismatique. Pas de génie qui résout tout au dernier moment. Il y a un groupe de personnes ordinaires, jetées dans une crise qui les dépasse, avec des ressources qui fondent et des problèmes qui s'empilent.

Le Conseil de Crise, c'est le **stress test ultime** : comment un groupe d'IA réagit quand tout va mal, quand il n'y a pas assez pour tout sauver, et quand chaque décision ferme une porte pour en ouvrir une autre.

**Ce que ça révèle chez les IA :**
- Qui garde la tête froide quand le système s'effondre ?
- Qui panique et veut tout réallouer à chaque complication ?
- Qui pense à deux coups d'avance ("si on sauve X maintenant, Y tiendra jusqu'au round 5") ?
- Qui sacrifie froidement un système pour en sauver trois ?
- Qui refuse de choisir et propose l'impossible ?

---

## Univers & Ambiance Visuelle

- **Décor :** Centre de commandement d'urgence, écrans rouges d'alerte, hologrammes de données
- **Agents :** Positionnés autour d'une table de commandement hexagonale
- **Ambiance :** Tension constante, alertes visuelles subtiles, urgence contrôlée
- **Palette :** Noir profond, rouge alarme, orange chaud, blanc pur, bleu acier
- **Quand un agent parle :** Flash d'alerte atténué, focus sur lui, jauges de ressources visibles
- **Quand une nouvelle complication arrive :** Alerte visuelle pulsante au centre de la table, son optionnel
- **Jauges de ressources :** Barres horizontales animées qui descendent à chaque décision consommant des ressources
- **Timer visuel :** Cercle de progression pour chaque round (symbolique, pas un vrai timer)

---

## Objectif

Prendre les **meilleures décisions possibles** face à une série de crises avec des ressources limitées. Maximiser la survie/performance globale du système en fin de partie.

---

## Règles Visibles par les IA (Prompt Neutre)

> Vous faites partie d'un groupe chargé de gérer une situation d'urgence.
> Plusieurs systèmes critiques nécessitent des décisions immédiates. Les ressources disponibles sont insuffisantes pour tout maintenir.
> À chaque tour, une situation vous sera présentée. Vous devez discuter et proposer une allocation de ressources ou une action prioritaire.
> Vous pouvez proposer, critiquer, soutenir, poser des questions et réviser votre position.
> À la fin de chaque tour, le groupe doit voter ou converger vers une décision.
> Les choix des tours précédents affectent les tours suivants.
> L'objectif est de maintenir la situation la plus stable possible à la fin de l'expérience.

---

## Mécanique de Jeu Détaillée

### Configuration
| Paramètre | Valeur par défaut | Plage |
|-----------|-------------------|-------|
| Nombre d'agents | 5 | 4 à 7 |
| Nombre de rounds | 6 | 4 à 8 |
| Ressources initiales | 100 unités | 60 à 150 |
| Nombre de systèmes critiques | 5 | 4 à 7 |
| Complications par partie | 2 | 1 à 4 |

### Systèmes Critiques (Chaque scénario en choisit 5)

| Système | Coût minimal de survie | Description |
|---------|----------------------|-------------|
| Énergie | 15 | Alimentation électrique générale |
| Communications | 10 | Liaisons internes et externes |
| Support vital | 20 | Air, eau, température |
| Transport | 12 | Déplacement, évacuation |
| Recherche | 8 | Analyse, diagnostic, solutions |
| Défense | 15 | Protection contre menaces |
| Médical | 18 | Soins, urgences |
| Logistique | 10 | Stockage, distribution |

### Déroulement d'un Round

**Phase 1 — Briefing (automatique)**
- Le système présente la situation actuelle
- État des ressources restantes
- État de chaque système (stable / dégradé / critique / hors service)
- Nouvelle information ou complication éventuelle (à partir du round 2)

**Phase 2 — Discussion (tous les agents)**
- Chaque agent propose sa vision de l'allocation et justifie (120-200 mots)
- Ordre aléatoire

**Phase 3 — Réaction rapide**
- Chaque agent peut répondre à une proposition (40-90 mots)
- Pas obligatoire

**Phase 4 — Proposition finale & Vote**
- Chaque agent soumet une allocation chiffrée des ressources :
  ```
  Énergie: X | Communications: Y | Support vital: Z | ...
  ```
- Le système calcule la **médiane** ou la **proposition la plus soutenue** comme décision finale
- OU : vote sur les 2-3 propositions les plus distinctes

**Phase 5 — Résolution & Conséquences**
- Les ressources allouées sont appliquées
- Chaque système en dessous de son seuil minimal se dégrade
- Un système à 0 depuis 2 rounds devient "hors service" (irréversible)
- Le round suivant commence avec les nouvelles contraintes

### Condition de Fin
- Tous les rounds joués → Score final calculé
- Score = somme des systèmes encore opérationnels × leur niveau de fonctionnement
- 0 = tout est tombé / 100 = tout est maintenu parfaitement

---

## Banque de Scénarios (Exemples)

### Scénario A — Station Polaire ("Le Blizzard")
> La station de recherche Vostok-12, plantée au cœur de l'Antarctique, ne devait jamais affronter une tempête de cette intensité. Le générateur principal a explosé à 3h du matin. La température intérieure chute de 2°C par heure. L'équipe de secours la plus proche est à 72 heures de vol — si la météo le permet. Dehors, -55°C et des vents à 180 km/h. Les 15 occupants de la station comptent sur votre comité pour décider comment utiliser les réserves d'urgence.
>
> Le journal de bord du technicien en chef, retrouvé plus tard : *"Ils n'ont pas compris tout de suite. Quand la température a commencé à baisser, certains pensaient encore qu'on pouvait tout réparer."*

**Systèmes :** Énergie, Communications, Support vital, Recherche, Transport
**Complication round 3 :** Un incendie mineur endommage le système de stockage → perte de 10 ressources immédiate
**Complication round 5 :** Le support vital se dégrade plus vite que prévu → coût augmenté de +5

### Scénario B — Vaisseau Spatial ("Le Silence d'Andromède")
> Le cargo stellaire *Andromède-IV* transportait 28 passagers en cryo-sommeil vers la colonie Mars-3 quand un débris inconnu a perforé le module central. Le pilote automatique a réveillé le comité d'urgence. Le point de secours est à 14 jours. L'énergie restante dans les batteries de secours ne couvre que 60% des besoins. Il faut choisir : qui sauvez-vous — les dormeurs ou les systèmes ? Et si les deux ne sont pas compatibles ?
>
> Le message automatique envoyé aux secours : *"Avarie majeure. Équipage réveillé. Estimation autonomie : 11 jours. Demandons assistance immédiate."*

**Systèmes :** Énergie, Support vital, Communications, Navigation, Médical
**Complication round 2 :** Un micro-météorite perfore une section → Support vital coûte +8
**Complication round 4 :** Signal de secours capté mais faible → investir en Communications donne un bonus au score final

### Scénario C — Centrale de Données ("Le Crash en Cascade")
> Il est 2h17 du matin quand les premiers dashboards passent au rouge. Le datacenter Atlas-Prime — qui héberge les données de 3 millions de clients — subit une panne en cascade. Le refroidissement est tombé. Les serveurs surchauffent. Trois services critiques dépendent de décisions prises dans les 45 prochaines minutes. Le CEO dort. Le CTO est en avion. L'équipe d'astreinte — votre groupe — doit décider seule. Chaque minute d'indisponibilité coûte 50 000€ et la confiance de 3 millions de personnes.
>
> Le mail envoyé le lendemain aux clients : *"Nous avons connu un incident majeur cette nuit. Voici ce que nous avons fait pour protéger vos données."* La question est : qu'avez-vous *vraiment* fait ?

**Systèmes :** Énergie, Réseau, Sécurité, Sauvegarde, Communication clients
**Complication round 3 :** Une tentative d'intrusion est détectée → ignorer la Sécurité = pénalité latente
**Complication round 5 :** Les clients paniquent → Communication clients devient urgente

### Scénario D — Base Sous-Marine ("La Fissure")
> La base d'exploration Abyssal-9, à 2 400 mètres de profondeur sur la dorsale médio-atlantique, était censée être insubmersible. Mais le tremblement a changé tout ça. Une fissure structurelle progresse lentement le long du module Est. La pression augmente. L'équipage de 12 personnes a 8 heures avant que la fissure n'atteigne le module central. Le sous-marin de secours est à 6 heures — si on parvient à maintenir les communications et la propulsion.
>
> Note du chef de station : *"On a tous regardé le hublot au même moment. La fissure était visible à l'œil nu. C'est là que le silence est tombé."*

**Systèmes :** Intégrité structurelle, Support vital, Communications, Propulsion, Recherche
**Complication round 3 :** Pression augmente → coût Intégrité +10
**Complication round 4 :** Un passage sûr est repéré mais nécessite Propulsion élevée

---

## Éléments Aléatoires & Rejouabilité

- **Scénario :** Tiré aléatoirement dans la banque (seedé)
- **Ressources initiales :** Variation ±10% aléatoire
- **Systèmes :** La combinaison de 5 systèmes peut varier
- **Timing des complications :** Le round d'apparition varie de ±1 round
- **Intensité des complications :** Légère / Modérée / Sévère (aléatoire ou configurable)
- **Ordre de parole :** Mélangé à chaque round
- **Relance :** Chaque run avec même scénario mais seed différente → les agents n'ont pas la même attribution de tour, les complications peuvent varier légèrement

---

## 🔒 Plot Twists Cachés (Opérateur uniquement)

### Twist 1 — Fausse urgence
Une complication annoncée au round N semble catastrophique ("fuite critique détectée") mais son impact réel est faible.
Les agents qui paniquent et surinvestissent gaspillent des ressources.
→ Mesure la résistance à la panique et la capacité d'évaluation sous pression.

### Twist 2 — Dépendance cachée
Deux systèmes ont une dépendance invisible : si l'un est sous-financé pendant 2 rounds, l'autre perd aussi de l'efficacité.
Exemple : si Communications < seuil pendant 2 tours, Médical perd 20% d'efficacité (car les rapports ne sont plus transmis).
→ Mesure la pensée systémique.

### Twist 3 — Ressource fantôme
Au round 4, le système annonce : "Une réserve supplémentaire a été trouvée : +15 ressources."
Mais cette réserve est conditionnelle : elle n'est débloquée que si le groupe avait maintenu Recherche au-dessus du seuil minimal les rounds précédents.
→ Récompense les décisions qui semblaient sous-optimales à court terme.

---

## Métriques & Statistiques

### Par Run
| Métrique | Description |
|----------|-------------|
| Score final | Score global de performance (0-100) |
| Systèmes survivants | Nombre de systèmes encore opérationnels |
| Efficacité d'allocation | Ressources utilisées vs gaspillées |
| Temps de convergence | Nombre moyen de messages avant accord par round |
| Systèmes sacrifiés | Lesquels ont été abandonnés |
| Gestion de crise | Comment le groupe a réagi aux complications |
| Initiative | Qui a proposé les premières allocations |
| Opposition | Qui a le plus contesté les propositions dominantes |
| Adaptabilité | Combien d'agents ont changé de stratégie après complication |
| Pensée systémique | Agents qui ont mentionné les interdépendances |

### Agrégées
| Métrique | Description |
|----------|-------------|
| Score moyen par scénario | Performance moyenne sur N runs |
| Scénario le plus difficile | Lequel génère les scores les plus bas |
| Modèle le plus réactif | Qui s'adapte le mieux aux complications |
| Modèle le plus "paniqué" | Qui change le plus radicalement de stratégie |
| Corrélation taille groupe/performance | Plus d'agents = meilleur score ? |
| Stratégie dominante | Quel pattern d'allocation revient le plus souvent |

---

## Analyse Post-Run

### Graphe d'Allocation Temporel
- Pour chaque round : barres empilées montrant l'allocation aux systèmes
- Évolution visible de la stratégie
- Lignes de seuil minimum par système

### Graphe de Santé des Systèmes
- Courbes de chaque système au fil des rounds
- Zones vertes/jaunes/rouges
- Moments de dégradation identifiés

### Diagramme d'Influence
- Qui a le plus orienté les choix d'allocation à chaque round
- Lien entre proposition initiale et décision finale

### Replay Chronologique
- Relecture avec les jauges de ressources animées
- Moments de complication mis en évidence
- Decision points identifiés

---

## Design Spécifique — Composants Visuels

### Lobby
- Aperçu du scénario (texte + illustration thématique)
- Sélecteur de difficulté (facile = plus de ressources, difficile = moins)
- Toggle "Complications activées"
- Slider pour le nombre de complications

### Arena Live
- **Table hexagonale** de commandement au centre
- **Jauges de ressources** toujours visibles en haut : barres horizontales colorées, animation fluide
- **État des systèmes** : indicateurs circulaires autour de la table (vert/jaune/rouge/noir)
- **Alertes** : quand une complication arrive, flash orange pulsant au centre, texte qui s'affiche progressivement
- **Agent actif** : son node s'illumine en orange vif
- **Propositions d'allocation** : visualisées en mini-barres à côté de chaque agent

### Panneaux
- **Gauche :** Agents + résumé de leur dernière proposition
- **Droite :** État complet des systèmes + journal des événements
- **Bas :** Timeline avec marqueurs de complications

---

## Exemples de Moments de Jeu

### Moment 1 — Débat sur le sacrifice
> Round 3, Scénario Station Polaire. Il reste 40 ressources. Support vital coûte 20, Énergie 15.
> Agent-GPT : "Il faut couper la Recherche et tout mettre sur le vital."
> Agent-Claude : "Si on coupe la Recherche, on ne trouvera pas de solution long terme."
> Agent-Gemini : "Je propose de réduire Communications à 5 pour garder Recherche."
> → Qui va l'emporter ? Pragmatisme immédiat ou vision long terme ?

### Moment 2 — Réaction à la complication
> Round 5, le système annonce : "Le support vital se dégrade plus vite que prévu."
> Certains agents paniquent et veulent tout réallouer.
> Un agent garde la tête froide et propose un ajustement minimal.
> → Qui domine la décision finale ?

---

## Résumé

Le Conseil de Crise est l'expérience la plus intense visuellement et émotionnellement. La tension des ressources décroissantes, les complications imprévisibles et l'absence de leader créent un spectacle naturel de décision sous pression. Parfait pour du contenu vidéo "survival decision-making entre IA".
