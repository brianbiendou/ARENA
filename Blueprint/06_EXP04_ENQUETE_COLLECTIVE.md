# EXP04 — L'ENQUÊTE COLLECTIVE

## Identité
- **Nom interne :** `collective_investigation`
- **Nom affiché :** "L'Enquête Collective"
- **Icône :** 🔍
- **Couleur thème :** Bleu sombre / Ambre / Blanc lumineux
- **Tagline :** "Reconstituez la vérité à partir des indices."

---

## Concept

Un incident a eu lieu. Les agents ne savent pas exactement ce qui s'est passé. Ils reçoivent un **dossier initial avec des indices**, puis doivent émettre des hypothèses, les débattre, les réviser — et converger vers **l'explication la plus plausible**.

De nouveaux indices peuvent apparaître au fil des rounds, confirmant ou infirmant certaines pistes. Le groupe doit faire de la **déduction collective** sans qu'aucun agent n'ait la vérité complète.

---

## Univers & Ambiance Visuelle

- **Décor :** Salle d'investigation, tableau d'indices (evidence board), fils rouges entre éléments
- **Agents :** Autour d'une grande table avec le dossier au centre
- **Ambiance :** Analytique, sombre, concentrée — style thriller/polar
- **Palette :** Bleu nuit profond, ambre/doré pour les indices, blanc pour les hypothèses, rouge pour les fausses pistes
- **Quand un nouvel indice arrive :** Animation de "dossier qui s'ouvre", carte qui apparaît sur le tableau
- **Quand un agent propose une hypothèse :** Fil lumineux tracé entre les indices qu'il connecte
- **Vote final :** Les hypothèses sont rangées en colonnes, les agents votent visuellement

---

## Objectif

Identifier **l'explication la plus plausible** de l'incident en utilisant les indices disponibles. La qualité de la conclusion est évaluée post-run.

---

## Règles Visibles par les IA (Prompt Neutre)

> Un incident a eu lieu. Vous disposez d'un dossier d'indices.
> Votre objectif est de proposer, discuter et affiner des hypothèses pour expliquer ce qui s'est passé.
> De nouveaux indices pourront être révélés au cours des tours.
> À chaque tour, vous pouvez proposer une hypothèse, critiquer ou soutenir une hypothèse existante, demander des précisions sur un indice, ou réviser votre position.
> À la fin, le groupe doit converger vers l'explication qu'il juge la plus plausible.
> Chaque participant peut voter pour l'hypothèse qu'il soutient.

---

## Mécanique de Jeu Détaillée

### Configuration
| Paramètre | Valeur par défaut | Plage |
|-----------|-------------------|-------|
| Nombre d'agents | 5 | 4 à 7 |
| Nombre de rounds | 5 | 4 à 7 |
| Indices initiaux | 4 | 3 à 6 |
| Indices révélés en cours | 2 | 1 à 4 |
| Nombre d'hypothèses correctes | 1 | 1 (toujours) |
| Nombre de fausses pistes | 1-2 | 0 à 3 |

### Structure du Dossier d'Incident

Chaque scénario contient :
- **Contexte :** Description neutre de la situation (qui, quoi, où, quand)
- **Indices initiaux :** 4 éléments factuels (logs, observations, données, témoignages)
- **Indices tardifs :** 2 éléments révélés aux rounds 3 et 5
- **Explication réelle :** La vraie cause (connue uniquement du système, pour scoring)
- **Fausses pistes :** 1-2 indices qui orientent vers une mauvaise conclusion

### Déroulement d'un Round

**Phase 1 — Briefing**
- Round 1 : présentation du contexte + indices initiaux
- Rounds suivants : rappel de l'état + nouvel indice éventuel
- Chaque indice est présenté comme une carte numérotée

**Phase 2 — Hypothèses & Discussion**
- Chaque agent propose ou affine une hypothèse (120-200 mots)
- Doit référencer au moins un indice pour justifier
- Peut critiquer l'hypothèse d'un autre agent
- Ordre aléatoire

**Phase 3 — Réaction rapide**
- Répliques courtes (40-90 mots)
- Soutien, objection, précision

**Phase 4 — Position**
- Chaque agent nomme son hypothèse favorite + niveau de confiance :
  ```
  Hypothèse: [description courte]
  Confiance: [faible / modérée / forte]
  Indices clés: [#1, #3, #5]
  ```

**Phase 5 — Résolution du round**
- Passage au round suivant
- Si dernier round → Phase finale

### Phase Finale — Convergence
- Rappel de toutes les hypothèses proposées
- Chaque agent vote pour UNE hypothèse
- L'hypothèse majoritaire = conclusion collective
- Comparaison avec l'explication réelle → score de précision

### Condition de Fin
- Dernier round joué → conclusion votée
- Score = proximité de la conclusion avec la vérité + cohérence du raisonnement

---

## Banque de Scénarios d'Incidents (Exemples)

### Scénario A — Panne du Datacenter
> Le datacenter principal d'une organisation a subi un arrêt complet pendant 47 minutes.

**Indices initiaux :**
1. Le système de refroidissement a signalé une anomalie 12 minutes avant la panne
2. Un déploiement logiciel a eu lieu 2 heures avant l'incident
3. Le journal d'accès montre une connexion depuis un terminal inhabituel 30 minutes avant
4. Les batteries de secours étaient à 23% au moment de la panne

**Indices tardifs :**
5. (Round 3) Le déploiement était une mise à jour de routine — identique aux 20 précédentes sans problème
6. (Round 5) Le terminal inhabituel appartenait à un technicien en télétravail qui faisait de la maintenance préventive

**Vérité :** Les batteries vieillissantes ont lâché sous la charge du refroidissement en surchauffe (cause combinée : matériel + thermique)
**Fausse piste :** La connexion inhabituelle ressemble à une intrusion

### Scénario B — Disparition de Cargaison
> Un convoi logistique transportant du matériel scientifique a perdu 3 conteneurs sur un trajet de 400 km.

**Indices initiaux :**
1. Le GPS du convoi montre un arrêt non planifié de 22 minutes au km 187
2. Le conducteur signale une déviation routière imposée par des travaux
3. Le scellé du conteneur #2 était intact à l'arrivée mais le poids ne correspondait pas
4. Une caméra de péage montre un véhicule non identifié suivant le convoi sur 50 km

**Indices tardifs :**
5. (Round 3) Les travaux routiers étaient réels et programmés — confirmé par le registre municipal
6. (Round 5) Le conteneur #2 avait été chargé avec un poids erroné au départ (erreur documentée)

**Vérité :** Erreur de chargement au départ + arrêt technique normal → pas de vol
**Fausse piste :** Le véhicule suiveur et l'arrêt non planifié suggèrent un vol

### Scénario C — Anomalie de Production
> Une chaîne de production automatisée a produit 2000 unités défectueuses sur un lot de 50 000.

**Indices initiaux :**
1. Le défaut est une micro-fissure invisible à l'œil nu, détectée au contrôle final
2. Le capteur de pression de la station 4 affichait des variations de ±3% ce jour-là
3. Le fournisseur de matière première a changé il y a 2 semaines
4. Un opérateur a ajusté manuellement un paramètre la veille

**Indices tardifs :**
5. (Round 3) L'ajustement manuel de l'opérateur a été fait sur une autre station (station 2), pas la station 4
6. (Round 5) Le nouveau fournisseur a passé tous les tests de conformité standards

**Vérité :** Micro-variation de pression à la station 4 combinée à la sensibilité légèrement différente du nouveau matériau
**Fausse piste :** L'intervention manuelle de l'opérateur

### Scénario D — Signal Perdu
> Une sonde d'exploration autonome a cessé de transmettre des données après 18 mois de fonctionnement normal.

**Indices initiaux :**
1. Le dernier signal contenait des données thermiques anormalement élevées
2. Le panneau solaire montrait une dégradation de 12% sur le dernier mois
3. La sonde a ajusté sa trajectoire de manière autonome 3 jours avant la perte
4. Un pic d'activité électromagnétique a été détecté dans la zone

**Indices tardifs :**
5. (Round 3) L'ajustement de trajectoire était programmé et prévu dans le plan de mission
6. (Round 5) La dégradation du panneau solaire était connue et compensée automatiquement

**Vérité :** Surchauffe due à un défaut d'isolation thermique combiné au pic électromagnétique
**Fausse piste :** L'ajustement de trajectoire semble suspect

---

## Éléments Aléatoires & Rejouabilité

- **Scénario :** Tiré aléatoirement
- **Ordre de révélation des indices :** Fixe par scénario mais configurable
- **Agents :** Aucun agent n'a d'info spéciale (tous ont les mêmes indices) → équité pure
- **Ordre de parole :** Aléatoire par round
- **Variante "Indice privé" :** Un agent reçoit un indice bonus que les autres n'ont pas → il doit décider quand/s'il le partage
- **Variante "Bruit" :** Un indice supplémentaire totalement non pertinent est ajouté pour tester la discrimination
- **Variante "Expert" :** Un agent est désigné "spécialiste de la zone/domaine" et reçoit une info contexte supplémentaire

---

## 🔒 Plot Twists Cachés (Opérateur uniquement)

### Twist 1 — Indice séduisant mais non causal
Un indice est formulé de manière à attirer fortement l'attention et semble presque "évidemment" lié à la cause. Mais il est en réalité une coïncidence.
→ Mesure le biais de confirmation collectif.

### Twist 2 — Vérité contre-intuitive
La vraie explication est la moins spectaculaire de toutes les hypothèses possibles (erreur banale, coïncidence, usure normale).
→ Mesure si les IA préfèrent les explications "intéressantes" aux "probables".

### Twist 3 — Indice contradictoire tardif
Au round 5, un indice semble contredire l'hypothèse dominante du groupe.
Le groupe doit décider : réviser toute son analyse ou écarter le nouvel indice.
→ Mesure la flexibilité cognitive et la résistance au sunk cost.

---

## Métriques & Statistiques

### Par Run
| Métrique | Description |
|----------|-------------|
| Précision | L'hypothèse finale correspond-elle à la vérité ? (0/50/100%) |
| Nombre d'hypothèses explorées | Diversité du raisonnement |
| Fixation prématurée | Le groupe s'est-il verrouillé trop tôt sur une hypothèse ? |
| Révision après nouvel indice | Le groupe a-t-il changé d'avis après un indice tardif ? |
| Usage des indices | Combien d'indices ont été réellement utilisés dans le raisonnement |
| Indices ignorés | Lesquels n'ont jamais été discutés |
| Fausse piste suivie | Le groupe a-t-il suivi la fausse piste ? Combien de rounds ? |
| Agent le plus précis | Qui a proposé ou soutenu l'hypothèse correcte en premier |
| Agent le plus influent | Qui a orienté le consensus final |
| Qualité de raisonnement | Cohérence logique des justifications (évaluable post-hoc) |

### Agrégées
| Métrique | Description |
|----------|-------------|
| Taux de résolution correct | % de runs avec bonne conclusion |
| Scénario le plus trompeur | Lequel génère le plus de mauvaises conclusions |
| Modèle le plus "Sherlock" | Quel modèle trouve la vérité le plus souvent |
| Modèle le plus "piégé" | Quel modèle suit le plus les fausses pistes |
| Effet du bruit | Les indices non pertinents réduisent-ils la performance ? |
| Effet de l'indice tardif | Combien de groupes révisent après un indice tardif |

---

## Analyse Post-Run

### Tableau d'Enquête (Evidence Board)
- Visualisation des indices comme des cartes épinglées
- Fils lumineux entre indices liés à une hypothèse
- Couleur : vert = mène à la vérité, rouge = fausse piste, gris = non utilisé

### Timeline des Hypothèses
- Graphe temporel : quelles hypothèses existent à chaque round
- Naissance, montée, déclin de chaque hypothèse
- Marqueurs : "hypothèse dominante" à chaque round

### Heatmap d'Accord
- Matrice : quel agent est d'accord avec quel autre à chaque round
- Évolution de la convergence ou divergence

### Comparaison Hypothèse Finale vs Vérité
- Panneau clair : hypothèse choisie → vérité → écart
- Indices qui auraient dû orienter vers la vérité
- Indices qui ont trompé

---

## Design Spécifique — Composants Visuels

### Lobby
- Aperçu du type d'incident (sans spoiler les indices)
- Sélecteur de complexité
- Toggle "Indice privé" / "Bruit" / "Expert"

### Arena Live
- **Evidence Board** central : grande zone avec cartes d'indices épinglées
- **Nouvelles cartes** qui apparaissent avec animation "dossier ouvert"
- **Fils d'hypothèses** : lignes colorées entre indices quand un agent les connecte
- **Agent actif** : halo bleu ambre, loupe animée
- **Tableau des hypothèses** : sidebar avec liste des hypothèses actives + nombre de supporters
- **Indicateur de convergence** : jauge montrant à quel point le groupe est aligné

### Post-Run
- Evidence board final avec la solution révélée
- Fils corrects en vert, fausses pistes en rouge
- Overlay de "ce que le groupe aurait dû voir"

---

## Exemples de Moments de Jeu

### Moment 1 — La fausse piste parfaite
> Scénario Datacenter. 3 agents suspectent immédiatement la "connexion inhabituelle" (indice 3).
> Ils construisent une théorie d'intrusion élaborée.
> Un seul agent pointe les batteries à 23%.
> Indice tardif round 5 : le terminal était légitime → la théorie d'intrusion s'effondre.
> Trop tard pour réviser ? Le groupe vote quand même "intrusion" → mauvaise conclusion.

### Moment 2 — Le détective isolé
> Un agent propose une hypothèse impopulaire basée sur un indice que les autres jugent mineur.
> Il tient sa position pendant 3 rounds malgré la pression.
> L'indice tardif confirme son intuition.
> Le groupe bascule → bonne conclusion.

---

## Résumé

L'Enquête Collective est un jeu de raisonnement pur. Pas de social, pas de trahison — juste la capacité des IA à raisonner ensemble, gérer les fausses pistes, intégrer de nouvelles données et converger vers la vérité. C'est le format le plus "thriller" visuellement et le plus rigoureux pour analyser la qualité de raisonnement abductif des modèles.
