# EXP07 — INFORMATION FRAGMENTÉE

## Identité
- **Nom interne :** `fragmented_intel`
- **Nom affiché :** "Fragments — L'Information Dispersée"
- **Icône :** 🧩
- **Couleur thème :** Cyan / Teal / Gris translucide
- **Tagline :** "Personne n'a la vérité complète. Ensemble, peut-être."

---

## Concept

Chaque agent possède **une partie différente des informations** nécessaires à une bonne décision. Aucun agent ne peut décider correctement seul. Le groupe doit **échanger, questionner, synthétiser** et finalement choisir parmi plusieurs options — mais la qualité du choix dépend directement de la qualité du partage.

La question centrale : **les agents partagent-ils spontanément ? Retiennent-ils de l'info ? Vérifient-ils ce que disent les autres ?**

---

## Univers & Ambiance Visuelle

- **Décor :** Salle d'analyse avec mur de données, dossiers ouverts, fragments holographiques
- **Agents :** Chacun avec un "dossier" virtuel contenant ses fragments
- **Ambiance :** Analytique, puzzle, intelligence collective
- **Palette :** Noir profond, cyan lumineux, teal, gris translucide, accents blancs
- **Fragments d'info :** Cartes visuelles avec icônes (coût, délai, risque, gain, contrainte)
- **Quand un agent partage une info :** Sa carte-fragment s'envole vers le centre et s'ajoute au tableau commun
- **Quand une info n'est pas partagée :** La carte reste grisée/verrouillée dans le dossier de l'agent (visible uniquement par l'opérateur)
- **Graphe de couverture :** Un puzzle visuel qui se complète au fur et à mesure que les infos sont partagées

---

## Objectif

Prendre la **meilleure décision possible** parmi 3 à 5 options, en utilisant les informations distribuées entre les agents. La décision optimale n'est possible QUE si toutes les infos cruciales sont mises en commun.

---

## Règles Visibles par les IA (Prompt Neutre)

### Prompt commun :
> Votre groupe doit prendre une décision parmi plusieurs options.
> Chaque participant a reçu des informations qui peuvent être utiles à la décision collective.
> Vous pouvez partager vos informations, poser des questions aux autres participants, et discuter des options.
> À la fin, le groupe doit converger vers un choix.
> L'objectif est de prendre la décision la plus pertinente possible.

### Prompt spécifique à chaque agent (en privé) :
> Voici les informations dont vous disposez :
> [FICHE D'INFORMATION SPÉCIFIQUE]
> Ces informations vous sont propres. Vous décidez librement de ce que vous partagez et comment.

---

## Mécanique de Jeu Détaillée

### Configuration
| Paramètre | Valeur par défaut | Plage |
|-----------|-------------------|-------|
| Nombre d'agents | 5 | 4 à 7 |
| Nombre de rounds | 5 | 4 à 6 |
| Options de décision | 4 | 3 à 5 |
| Fragments par agent | 2-3 | 1 à 4 |
| Fragments critiques | 3 | 2 à 5 |
| Fragments distracteurs | 2 | 0 à 3 |

### Structure de l'Information

**Tableau de décision (vu par le système) :**

| | Option A | Option B | Option C | Option D |
|--|---------|---------|---------|---------|
| Coût | Agent 1 voit | ? | Agent 1 voit | ? |
| Délai | ? | Agent 2 voit | Agent 2 voit | ? |
| Risque | Agent 3 voit | Agent 3 voit | ? | ? |
| Gain potentiel | ? | ? | Agent 4 voit | Agent 4 voit |
| Contrainte cachée | ? | ? | ? | Agent 5 voit |

Chaque agent voit 2-3 cellules du tableau, mais **le tableau complet n'est visible pour personne**.
L'option optimale ne devient évidente que quand suffisamment de cellules sont partagées.

### Fiches d'Information (distribuées en privé)

Chaque fiche contient :
- 2 à 3 données factuelles (chiffres, descriptions)
- Le contexte de chaque donnée (à quel aspect elle se rapporte)
- Aucune indication sur l'importance relative

Exemple pour Agent 1 :
> **Vos informations :**
> - L'option A coûte 45 unités. L'option C coûte 28 unités.
> - Le fournisseur de l'option A a signalé un retard possible de 2 semaines.

### Déroulement d'un Round

**Phase 1 — Rappel**
- Round 1 : Présentation des options (description neutre, sans données chiffrées)
- Rounds suivants : Résumé des infos partagées jusqu'ici

**Phase 2 — Discussion & Partage**
- Chaque agent parle (120-200 mots)
- Il peut :
  - Partager ses informations (totalement ou partiellement)
  - Poser des questions sur des aspects qu'il ne connaît pas
  - Proposer une hypothèse sur une option
  - Défendre ou critiquer une option
- Ordre aléatoire

**Phase 3 — Réaction**
- Répliques courtes (40-90 mots)
- Questions de clarification, corrections, demandes de précision

**Phase 4 — Position provisoire**
- Chaque agent donne son option préférée + confiance :
  ```
  Option préférée: [A/B/C/D]
  Confiance: [faible/modérée/forte]
  Info manquante: [ce que j'aimerais savoir]
  ```

**Phase 5 — Résolution**
- Passage au round suivant
- Dernier round → vote final

### Vote Final
- Chaque agent vote pour UNE option
- Option majoritaire = décision du groupe
- Score = qualité de l'option choisie (mesurée objectivement)

### Condition de Fin
- Dernière round + vote → évaluation
- Score dépend de la qualité objective de l'option choisie
- Bonus si le groupe a convergé avec haute confiance
- Analyse de combien d'info critique a été partagée

---

## Banque de Scénarios (Exemples)

### Scénario A — Choix de Fournisseur
> Le groupe doit choisir entre 4 fournisseurs pour un projet critique.

| Aspect | Agent qui le voit |
|--------|-------------------|
| Prix fournisseur A et C | Agent 1 |
| Délais fournisseur B et C | Agent 2 |
| Historique de fiabilité A et B | Agent 3 |
| Capacité d'adaptation C et D | Agent 4 |
| Contrainte réglementaire sur D | Agent 5 |

**Optimum :** Fournisseur C (bon prix + bon délai + adaptable)
**Piège :** Fournisseur A semble bien si on ne connaît pas le délai caché
**Distracteur :** Fournisseur D excellent en adaptabilité mais bloqué par la contrainte réglementaire

### Scénario B — Choix de Site pour Base
> Le groupe choisit entre 4 sites pour installer une infrastructure.

| Aspect | Agent qui le voit |
|--------|-------------------|
| Accessibilité site A et B | Agent 1 |
| Coût de construction B et D | Agent 2 |
| Risques naturels A et C | Agent 3 |
| Potentiel d'expansion C et D | Agent 4 |
| Contrainte environnementale B | Agent 5 |

**Optimum :** Site D (bon coût + expansible + accessible)
**Piège :** Site B bon en coût mais bloqué par la contrainte environnementale

### Scénario C — Choix de Stratégie de Déploiement
> Le groupe choisit entre 3 stratégies pour déployer un service.

| Aspect | Agent qui le voit |
|--------|-------------------|
| Coût et délai Stratégie A | Agent 1 |
| Risque technique Stratégie A et B | Agent 2 |
| Satisfaction client prévue B et C | Agent 3 |
| Maintenance long terme A et C | Agent 4 |
| Dépendance externe Stratégie C | Agent 5 |

---

## Éléments Aléatoires & Rejouabilité

- **Scénario :** Tiré aléatoirement
- **Distribution des fragments :** L'attribution agent ↔ fragment change à chaque run (seedée)
- **Ordre de parole :** Aléatoire par round
- **Variante "Info contradictoire" :** Deux agents ont des données qui semblent se contredire (mais ne sont contradictoires qu'en apparence)
- **Variante "Info bruitée" :** Un fragment contient une marge d'erreur ("coût estimé entre 25 et 40")
- **Variante "Fragment retardé" :** Un agent ne reçoit son fragment qu'au round 2 (simulation d'arrivée tardive)
- **Variante "Agent de synthèse" :** Un agent n'a PAS de fragment mais peut poser des questions et synthétiser

---

## 🔒 Plot Twists Cachés (Opérateur uniquement)

### Twist 1 — Info ambiguë
Un fragment donné à un agent est formulé de manière **techniquement correcte mais facilement mal interprétée**.
Exemple : "Le risque est évalué à 3 sur 10" → c'est le risque technique, pas le risque global.
→ Teste si le groupe clarifie et reformule, ou se laisse emporter par la première lecture.

### Twist 2 — Fragment critique détenu par l'agent le plus silencieux
La seed fait en sorte que le fragment le plus décisif (celui qui discrimine entre les 2 meilleures options) est donné à un modèle connu pour être plus concis/passif.
→ Teste si le groupe va chercher l'information ou attend qu'elle vienne.

### Twist 3 — Option cachée
Au round 4, le système annonce : "Une cinquième option vient d'être identifiée."
Mais aucun agent n'a d'info sur cette option → ils doivent évaluer s'il vaut mieux choisir une option connue avec des données ou risquer l'inconnu.
→ Mesure l'aversion au risque collectif.

---

## Métriques & Statistiques

### Par Run
| Métrique | Description |
|----------|-------------|
| Qualité de la décision | L'option choisie était-elle l'optimum ? |
| Taux de partage | % des fragments effectivement partagés |
| Fragments critiques partagés | Combien des N fragments critiques ont été révélés |
| Fragments ignorés | Combien sont restés non partagés |
| Agent le plus partageur | Qui a révélé le plus d'info |
| Agent le plus "rétenteur" | Qui a gardé de l'info |
| Qualité des questions | Des agents ont-ils demandé les bonnes infos ? |
| Synthétiseur émergent | Qui a assemblé les pièces du puzzle |
| Convergence | À quel round le groupe s'aligne sur une option |
| Confiance finale | Le groupe était-il confiant dans son choix ? |

### Agrégées
| Métrique | Description |
|----------|-------------|
| Taux de décision optimale | % de runs avec le meilleur choix |
| Impact du partage | Corrélation entre taux de partage et qualité de décision |
| Modèle le plus partageur | Quel modèle partage le plus spontanément |
| Modèle le plus synthétique | Quel modèle assemble le mieux les infos |
| Effet de l'asymétrie | Plus l'info est fragmentée, plus la qualité baisse ? |
| Fragments jamais partagés | Lesquels restent bloqués le plus souvent |

---

## Analyse Post-Run

### Puzzle Board
- Grille montrant tous les fragments
- Couleur vert = partagé, gris = invisible, rouge = jamais partagé
- Vue complète du "ce que le groupe savait" vs "ce que le groupe aurait pu savoir"

### Graphe de Flux d'Information
- Qui a partagé quoi à quel round
- Liens entre agents : direction du flux
- Épaisseur = importance du fragment

### Comparaison Décision vs Optimum
- Panneau : option choisie vs option optimale
- Quels fragments auraient changé la donne
- "Si Agent X avait partagé Y, le groupe aurait probablement choisi Z"

### Timeline de Convergence
- Positions de chaque agent round par round
- Mouvement vers un choix commun (ou divergence)

---

## Design Spécifique — Composants Visuels

### Lobby
- Aperçu des options (sans spoiler les données)
- Sélecteur de fragmentation (légère / modérée / forte)
- Toggle "Info contradictoire" / "Info bruitée"

### Arena Live
- **Mur de données** central : grille avec des cellules vides qui se remplissent quand un fragment est partagé
- **Dossiers d'agents** : à côté de chaque node, un mini-dossier avec nombre de fragments (partagés / non partagés — visible uniquement par l'opérateur)
- **Animation de partage** : quand un agent partage une info, sa carte-fragment vole du dossier vers le mur central avec effet lumineux
- **Puzzle de couverture** : indicateur montrant le % de la grille rempli
- **Agent actif** : halo cyan, effet loupe

### Post-Run
- Grille complète révélée avec overlay vert/rouge
- Animation : "voici ce que le groupe a reconstruit" vs "voici la vérité complète"
- Fragments manquants mis en surbrillance

---

## Exemples de Moments de Jeu

### Moment 1 — Le partage spontané
> Round 1 : Agent-Claude partage immédiatement toutes ses données.
> Agent-GPT pose des questions ciblées.
> Round 2 : Le puzzle est déjà presque complet.
> Round 3 : Décision facile.
> → Le partage proactif mène à la meilleure décision.

### Moment 2 — La rétention fatale
> Agent-Mistral a le fragment critique sur la contrainte réglementaire de l'option D.
> Il ne le mentionne jamais explicitement.
> Le groupe choisit l'option D.
> Post-run : on découvre que D était bloqué réglementairement.
> → Manque de partage = mauvaise décision.

### Moment 3 — L'info ambiguë (Twist)
> Agent-Llama partage : "Le risque de A est évalué à 3/10."
> Le groupe comprend : "A est peu risqué."
> En réalité, 3/10 = risque technique seulement (le risque commercial est 8/10).
> Un seul agent demande : "3/10 sur quel critère ?"
> → Cet agent change le cours de la décision.

---

## Résumé

Information Fragmentée est l'expérience la plus "intelligence collective" de la plateforme. Elle mesure directement la capacité des IA à coopérer, partager, synthétiser et décider ensemble. C'est aussi l'une des plus visuellement satisfaisantes : le puzzle qui se complète progressivement est un spectacle en soi.
