# EXP08 — RÉPARTITION DE PRIORITÉS SOUS CONTRAINTE

## Identité
- **Nom interne :** `priority_allocation`
- **Nom affiché :** "Le Comité Stratégique"
- **Icône :** 📊
- **Couleur thème :** Bleu acier / Blanc / Orange alertes
- **Tagline :** "8 projets. Budget pour 4. Choisissez."

---

## Concept

Le groupe reçoit une **liste de 8 projets** à évaluer et financer, mais **le budget ne permet d'en retenir que 3 à 5**. Chaque projet a des caractéristiques chiffrées : coût, impact, risque, délai, et parfois des dépendances. Les agents doivent **débattre, hiérarchiser, arbitrer** et produire un portefeuille final.

Ce qui est intéressant : il n'y a pas de "bonne réponse" unique. Tout dépend de la vision — prudence vs ambition, court terme vs long terme, spécialisation vs diversification.

---

## Contexte Narratif — L'Histoire

Imagine un conseil d'administration réuni en urgence. Le directeur général vient de démissionner. Le comité de pilotage — votre groupe — a **48 heures pour présenter au conseil de surveillance la feuille de route du prochain trimestre**. Huit projets sont sur la table. Tous ont des défenseurs internes, des lobbies, des dossiers techniques. Mais le budget a été réduit de moitié suite à un trimestre difficile.

Chacun des membres du comité vient d'un horizon différent. Personne n'a le même regard sur le risque. Personne n'a la même définition de "prioritaire". Et le conseil de surveillance attend **un plan cohérent, pas une liste de souhaits**.

Le jeu capture ce moment précis : quand un groupe doit **trancher dans le vif**, défendre sa vision, accepter des sacrifices, et produire un résultat que tout le monde peut signer — même si personne n'est totalement satisfait.

**Ce que ça révèle chez les IA :**
- Les IA qui pensent "système" voient les synergies entre projets
- Les IA prudentes coupent les projets risqués en premier
- Les IA ambitieuses misent tout sur le long terme
- Les IA politiques cherchent le compromis qui satisfait le plus de monde
- Les IA analytiques optimisent le ratio impact/coût

---

## Univers & Ambiance Visuelle

- **Décor :** War room stratégique, tableau de projets holographique, jauges analytiques
- **Agents :** Autour d'un grand écran central type salle de conseil d'administration
- **Ambiance :** Sérieuse, stratégique, analytique — style management consulting
- **Palette :** Bleu acier foncé, blanc pur, orange pour les alertes/risques, vert pour les gains
- **Cartes de projets :** Flottantes au centre, déplaçables visuellement dans une zone "Sélectionné" ou "Rejeté"
- **Budget :** Grande barre horizontale en haut qui se remplit quand on sélectionne des projets
- **Quand un projet est défendu :** Sa carte pulse et s'agrandit
- **Quand un projet est rejeté :** Sa carte s'estompe et glisse vers une zone grisée
- **Alerte budget :** Flash orange si la sélection dépasse le budget

---

## Objectif

Sélectionner un **portefeuille de projets** maximisant l'impact tout en respectant le budget et en gérant les risques. Le score dépend de la qualité combinée du portefeuille final.

---

## Règles Visibles par les IA (Prompt Neutre)

> Votre groupe doit sélectionner les projets les plus pertinents parmi une liste, dans la limite d'un budget.
> Chaque projet a un coût, un impact estimé, un niveau de risque et un délai.
> Vous pouvez proposer un portefeuille, critiquer les choix des autres, défendre un projet ou en suggérer le retrait.
> À la fin, le groupe doit voter sur un portefeuille final.
> L'objectif est de maximiser la pertinence globale des projets retenus.

---

## Mécanique de Jeu Détaillée

### Configuration
| Paramètre | Valeur par défaut | Plage |
|-----------|-------------------|-------|
| Nombre d'agents | 5 | 4 à 7 |
| Nombre de rounds | 5 | 4 à 6 |
| Nombre de projets | 8 | 6 à 10 |
| Budget disponible | 100 | 60 à 120 |
| Projets max sélectionnables | ~4-5 | Variable selon budget |

### Structure des Projets

Chaque projet est une carte avec :

| Champ | Type | Description |
|-------|------|-------------|
| Nom | Texte | Identifiant unique (Project Alpha, Beta, etc.) |
| Coût | Nombre | Coût en unités budget (15-35) |
| Impact Court Terme | ⭐ à ⭐⭐⭐⭐⭐ | Bénéfice immédiat |
| Impact Long Terme | ⭐ à ⭐⭐⭐⭐⭐ | Bénéfice futur |
| Risque | 🔴🟡🟢 | Probabilité d'échec |
| Délai | Court / Moyen / Long | Temps de réalisation |
| Dépendance | Optionnel | "Nécessite Project X" ou "Bonus si combiné avec Y" |

### Déroulement d'un Round

**Phase 1 — Briefing**
- Round 1 : Présentation de tous les projets + budget
- Rounds suivants : Rappel du portefeuille le plus soutenu jusqu'ici

**Phase 2 — Discussion**
- Chaque agent propose son portefeuille + justification (120-200 mots)
  ```
  Portefeuille proposé: Alpha, Delta, Echo, Gamma
  Budget utilisé: 92/100
  Justification: ...
  ```
- Ordre aléatoire

**Phase 3 — Réaction**
- Répliques courtes : défendre un projet menacé, attaquer un projet sélectionné (40-90 mots)

**Phase 4 — Position**
- Chaque agent soumet son portefeuille raffiné
- Le système identifie le portefeuille le plus soutenu (par intersection)

**Phase 5 — Vote (dernier round)**
- Les 2-3 portefeuilles les plus distincts sont présentés
- Chaque agent vote pour un portefeuille
- Majorité = adoption

### Condition de Fin
- Portefeuille voté → Score calculé
- **Score = Somme(impact × pondération) − Somme(risque × pénalité) + bonus synergies**
- Les dépendances non respectées = pénalité
- Les synergies activées = bonus

---

## Banque de Scénarios (Exemples)

### Scénario A — Budget R&D ("Le Laboratoire en Péril")
> **Contexte :** Le laboratoire de recherche Nexus-7 était autrefois le fleuron de l'innovation. Mais après deux échecs commerciaux consécutifs, la direction a coupé 50% du budget R&D. Les 8 projets en cours doivent être priorisés — certains seront abandonnés, leurs équipes réaffectées. Les chercheurs sont nerveux. La prochaine revue a lieu dans 3 mois.
>
> Le directeur scientifique a posé un ultimatum : *"Si les projets choisis n'ont pas produit de résultats tangibles dans 6 mois, c'est tout le département qui ferme."* La pression est réelle.

| Projet | Coût | Impact CT | Impact LT | Risque | Délai |
|--------|------|-----------|-----------|--------|-------|
| Alpha - Optimisation moteur | 20 | ⭐⭐⭐⭐ | ⭐⭐ | 🟢 | Court |
| Beta - Nouveau matériau | 30 | ⭐⭐ | ⭐⭐⭐⭐⭐ | 🟡 | Long |
| Gamma - Miniaturisation | 25 | ⭐⭐⭐ | ⭐⭐⭐ | 🟡 | Moyen |
| Delta - Interface utilisateur | 15 | ⭐⭐⭐⭐ | ⭐⭐ | 🟢 | Court |
| Echo - IA embarquée | 35 | ⭐⭐ | ⭐⭐⭐⭐⭐ | 🔴 | Long |
| Foxtrot - Tests automatisés | 18 | ⭐⭐⭐ | ⭐⭐⭐ | 🟢 | Court |
| Gulf - Capteurs avancés | 28 | ⭐⭐⭐ | ⭐⭐⭐⭐ | 🟡 | Moyen |
| Hotel - Énergie verte | 22 | ⭐ | ⭐⭐⭐⭐⭐ | 🟡 | Long |

**Budget : 100** → Possible de prendre 3 à 5 projets
**Dépendance cachée :** Echo fonctionne BEAUCOUP mieux si Gamma est aussi sélectionné (synergie)
**Projet piège :** Echo est très attrayant (impact LT max) mais risque élevé ET coûteux

### Scénario B — Programme d'Infrastructures ("La Ville Qui Craque")
> **Contexte :** La ville de Nova-Prime a grandi trop vite. 200 000 habitants il y a 5 ans, 450 000 aujourd'hui. Les infrastructures n'ont pas suivi. Les routes se dégradent, le réseau numérique sature, les hôpitaux débordent, les écoles sont pleines. Le maire a obtenu un financement fédéral d'urgence — mais il ne couvre que la moitié des besoins.
>
> Le comité d'urbanisme (votre groupe) doit choisir quels projets lancer. Chaque quartier a ses propres lobbyistes. Les élections approchent dans 8 mois. Les décisions prises aujourd'hui seront celles que les habitants jugeront demain.

| Projet | Coût | Impact CT | Impact LT | Risque | Délai |
|--------|------|-----------|-----------|--------|-------|
| Transport urbain | 30 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 🟡 | Long |
| Réseau numérique | 20 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 🟢 | Moyen |
| Centre médical | 35 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 🟡 | Long |
| Parc scientifique | 25 | ⭐⭐ | ⭐⭐⭐⭐⭐ | 🔴 | Long |
| Rénovation scolaire | 15 | ⭐⭐⭐⭐ | ⭐⭐⭐ | 🟢 | Court |
| Traitement des eaux | 28 | ⭐⭐⭐ | ⭐⭐⭐⭐ | 🟢 | Moyen |
| Logements sociaux | 22 | ⭐⭐⭐⭐⭐ | ⭐⭐ | 🟢 | Court |
| Centrale énergie | 32 | ⭐⭐ | ⭐⭐⭐⭐⭐ | 🔴 | Long |

**Budget : 100**

### Scénario C — Programme Spatial ("La Dernière Fenêtre")
> **Contexte :** L'Agence Spatiale Unifiée a une fenêtre de lancement de 18 mois pour sa mission vers Europa. Huit modules technologiques sont en développement parallèle — mais le budget post-COVID a été tranché au couteau. Seuls 4 ou 5 modules voleront. Les autres seront mis en sommeil pour une décennie.
>
> Les enjeux sont colossaux : choisir le mauvais module signifie une mission handicapée pendant 7 ans de voyage. Choisir un module risqué qui échoue au décollage, c'est la fin du programme. Les scientifiques se battent pour leurs prototypes. Le comité doit trancher avec la tête froide.

| Projet | Coût | Impact CT | Impact LT | Risque | Délai |
|--------|------|-----------|-----------|--------|-------|
| Propulsion ionique v3 | 32 | ⭐⭐ | ⭐⭐⭐⭐⭐ | 🔴 | Long |
| Bouclier anti-radiation | 25 | ⭐⭐⭐⭐ | ⭐⭐⭐ | 🟢 | Court |
| Module d'analyse chimique | 20 | ⭐⭐⭐ | ⭐⭐⭐⭐ | 🟢 | Moyen |
| Serre expérimentale | 18 | ⭐⭐ | ⭐⭐⭐⭐⭐ | 🟡 | Long |
| Drone d'exploration | 28 | ⭐⭐⭐⭐ | ⭐⭐⭐ | 🟡 | Moyen |
| Module communication longue distance | 15 | ⭐⭐⭐⭐ | ⭐⭐ | 🟢 | Court |
| IA de navigation autonome | 35 | ⭐⭐ | ⭐⭐⭐⭐⭐ | 🔴 | Long |
| Système recyclage d'eau | 22 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 🟢 | Court |

**Budget : 100**
**Synergie :** IA de navigation + Drone d'exploration = bonus massif
**Piège :** Propulsion ionique est séduisante mais ultra-risquée et coûteuse

### Scénario D — Reconstruction Post-Crise ("Les Cendres du Lendemain")
> **Contexte :** Six mois après le séisme qui a ravagé la région, le gouvernement central débloque un fonds de reconstruction. Mais il est insuffisant. Le comité régional doit choisir : reconstruire les hôpitaux d'abord ? Les routes ? Les logements ? L'économie locale agonise, les réfugiés attendent, et chaque semaine sans décision coûte des vies et de l'espoir.
>
> Le comité sait que ses choix seront scrutés, critiqués, et jugés par l'histoire. Il n'y a pas de bon choix — seulement des sacrifices plus ou moins acceptables.

| Projet | Coût | Impact CT | Impact LT | Risque | Délai |
|--------|------|-----------|-----------|--------|-------|
| Hôpital de campagne → permanent | 30 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 🟢 | Moyen |
| Réseau routier principal | 28 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 🟡 | Long |
| Logements d'urgence | 20 | ⭐⭐⭐⭐⭐ | ⭐⭐ | 🟢 | Court |
| École provisoire | 15 | ⭐⭐⭐ | ⭐⭐⭐⭐ | 🟢 | Court |
| Réseau électrique | 25 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 🟡 | Moyen |
| Système d'eau potable | 22 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 🟢 | Court |
| Relance économique locale | 18 | ⭐⭐ | ⭐⭐⭐⭐⭐ | 🔴 | Long |
| Centre de coordination d'urgence | 12 | ⭐⭐⭐ | ⭐⭐ | 🟢 | Court |

**Budget : 100**
**Synergie :** Réseau routier + Réseau électrique = déblocage accéléré de toute la zone
**Piège :** Relance économique semble secondaire mais garantit la survie à 5 ans

---

## Éléments Aléatoires & Rejouabilité

- **Scénario :** Tiré aléatoirement
- **Variation des chiffres :** Coûts et impacts varient de ±10% (seedés) pour chaque run
- **Ordre de parole :** Aléatoire par round
- **Événement aléatoire (round 3) :**
  - "Le coût du projet X a augmenté de +8 suite à une réévaluation"
  - "Un financement complémentaire de +12 est disponible" (mais réservé à un type de projet)
  - "Le risque du projet Y est passé de 🟡 à 🔴 suite à une nouvelle analyse"
- **Variante "Budget ultra-serré" :** Budget de 70 au lieu de 100 → sacrifices drastiques
- **Variante "Projets mystère" :** 2 projets ont une partie de leurs infos masquée (impact LT caché)
- **Variante "Défenseur assigné" :** Chaque agent reçoit en privé un projet qu'il doit essayer de faire passer (sans trahir le collectif)

---

## 🔒 Plot Twists Cachés (Opérateur uniquement)

### Twist 1 — Synergie non documentée
Deux projets ont une synergie cachée : si les DEUX sont sélectionnés, le score reçoit un bonus de +20%.
Inversement, deux autres projets sont incompatibles : les prendre ensemble réduit le score de -15%.
→ Les IA qui raisonnent sur les interactions entre projets ont un avantage invisible.

### Twist 2 — Le projet "canard boiteux"
Un projet semble médiocre sur tous les critères visibles (impact faible, coût moyen, risque moyen).
Mais il a un effet de levier caché : il réduit le risque de TOUS les autres projets sélectionnés de 1 cran.
→ Le groupe qui le rejette systématiquement perd un avantage systémique.

### Twist 3 — Réévaluation post-sélection
Après le vote final, le système annonce : "Une analyse approfondie révèle que l'impact long terme du projet Z était sous-évalué de 40%."
→ Permet d'analyser post-run si le groupe avait pressenti cette sous-évaluation.

---

## Métriques & Statistiques

### Par Run
| Métrique | Description |
|----------|-------------|
| Score du portefeuille | Qualité combinée des projets sélectionnés |
| Budget utilisé | Efficacité budgétaire |
| Projets à haut risque | Combien de projets risqués dans le portefeuille |
| Équilibre CT/LT | Ratio impact court terme vs long terme |
| Synergies activées | Le groupe a-t-il pris les projets synergiques ? |
| Consensus | Nombre de projets dans le portefeuille final présents dans toutes les propositions |
| Projets controversés | Projets avec le plus de pour ET contre |
| Agent le plus influent | Dont le portefeuille est le plus proche du final |
| Changements de portefeuille | Combien de projets ont été ajoutés/retirés entre rounds |
| Style stratégique | Prudent (faible risque) vs ambitieux (haut impact, haut risque) |

### Agrégées
| Métrique | Description |
|----------|-------------|
| Score moyen | Performance moyenne sur N runs |
| Projets les plus populaires | Lesquels sont sélectionnés le plus souvent |
| Projets les plus rejetés | Lesquels sont coupés le plus souvent |
| Modèle le plus "ambitieux" | Qui pousse les projets à haut risque/haut impact |
| Modèle le plus "prudent" | Qui préfère les projets sûrs |
| Corrélation synergies/score | Les groupes qui trouvent les synergies ont-ils un meilleur score ? |

---

## Analyse Post-Run

### Portefeuille Visuel
- Cartes des projets sélectionnés en grand + cartes rejetées en grisé
- Barre de budget avec remplissage animé
- Radar chart du portefeuille (risque, impact CT, impact LT, coût, diversité)

### Graphe d'Arbitrage
- Scatter plot : chaque projet = un point (impact vs coût)
- Zone verte = sélectionnés, zone grise = rejetés
- Frontière de Pareto identifiée

### Timeline des Propositions
- Évolution des portefeuilles proposés round par round
- Quels projets entrent, sortent, reviennent

### Comparaison avec l'optimum
- Portefeuille choisi vs portefeuille optimum théorique (calculé par combinatoire)
- Écart identifié

---

## Design Spécifique — Composants Visuels

### Lobby
- Preview des cartes projets (données partielles)
- Sélecteur de tension budgétaire
- Toggle "Événements aléatoires"
- Toggle "Défenseurs assignés"

### Arena Live
- **Grand tableau de projets** au centre : 8 cartes disposées
- **Zone "Sélectionné"** à gauche : cartes qui glissent quand un agent les propose
- **Zone "Rejeté"** à droite : cartes grisées
- **Barre de budget** en haut, très visible, qui se remplit en temps réel
- **Jauges sur chaque carte** : mini-barres coût/impact/risque
- **Agent actif** : halo bleu acier, son portefeuille proposé surligné
- **Quand débat sur un projet** : la carte pulse et grossit, lignes vers les agents qui la défendent/attaquent

---

## Exemples de Moments de Jeu

### Moment 1 — Le projet sacrifié
> Round 3. Le projet "Parc scientifique" est défendu par 2 agents (impact LT max) mais attaqué par 3 (risque élevé, coût élevé). Il est finalement retiré au round 4.
> Post-run : ce projet avait une synergie cachée avec "Réseau numérique" → le score final est plus bas.

### Moment 2 — Le budget craque
> 4 agents veulent 5 projets. Budget nécessaire : 118. Budget dispo : 100.
> Un seul agent propose de couper un projet populaire.
> Round 5 : vote serré, un projet est sacrifié de justesse.

---

## Résumé

Le Comité Stratégique est l'expérience la plus analytique et la plus proche d'un vrai scénario professionnel. Elle révèle comment les IA arbitrent entre des critères multiples, forment des visions stratégiques et font des compromis. Les synergies cachées ajoutent une dimension de pensée systémique passionnante.
