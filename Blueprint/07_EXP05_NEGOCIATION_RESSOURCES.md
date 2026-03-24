# EXP05 — NÉGOCIATION DE RESSOURCES

## Identité
- **Nom interne :** `resource_negotiation`
- **Nom affiché :** "La Table des Négociations"
- **Icône :** ⚖️
- **Couleur thème :** Doré / Bronze / Noir charbon
- **Tagline :** "100 unités. 5 besoins. Zéro accord garanti."

---

## Concept

Un ensemble fixe de ressources (100 unités) doit être réparti entre plusieurs postes de dépense ou bénéficiaires. Chaque agent défend une vision de la répartition. Ils doivent discuter, négocier, faire des compromis et converger vers un accord.

**Si le groupe ne trouve pas d'accord dans le temps imparti, TOUT LE MONDE PERD** — les ressources sont "gelées" et personne n'en bénéficie. Cette pression force la négociation réelle.

---

## Contexte Narratif — L'Histoire

Imagine la scène. Une table ronde. Des dossiers ouverts. Un compteur au centre qui affiche **100**. Et cinq personnes qui savent toutes la même chose : *il n'y en aura pas assez pour tout le monde.*

C'est le dilemme le plus vieux du monde. Celui des parents qui doivent choisir entre l'école et le médecin. Celui des gouvernements qui arbitrent entre défense et éducation. Celui des explorateurs qui doivent choisir entre emporter plus de nourriture ou plus d'équipement.

La Table des Négociations reproduit ce moment universel : **quand les besoins légitimes dépassent les moyens, comment un groupe tranche-t-il ?**

Ce qui rend l'expérience fascinante, c'est que chaque IA *sait* que l'accord est nécessaire. Si personne ne cède, tout le monde coule. Mais céder, c'est aussi sacrifier quelque chose qui *compte*. Chaque unité déplacée d'un poste à un autre n'est pas un chiffre — c'est une vie, un projet, un avenir fermé.

**Ce que ça révèle chez les IA :**
- Qui propose le premier compromis ?
- Qui refuse de bouger et tient son poste coûte que coûte ?
- Qui forme des alliances ("je te donne 5 sur mon poste si tu me soutiens sur le tien") ?
- Qui joue le médiateur et tente de trouver l'équilibre mathématique ?
- Et quand le vote final arrive… qui trahit l'accord de principe ?

---

## Univers & Ambiance Visuelle

- **Décor :** Table diplomatique ronde, jetons lumineux, ambiance négociation de haut niveau
- **Agents :** Assis autour de la table, chacun avec un dossier de revendication
- **Ambiance :** Tension élégante, diplomatie, enjeux élevés
- **Palette :** Noir charbon, doré, bronze, ivoire, touches de rouge pour les désaccords
- **Jetons de ressources :** 100 jetons lumineux au centre de la table, qui se déplacent vers les postes
- **Quand un agent propose :** Les jetons se redistribuent visuellement en temps réel
- **Quand il y a désaccord :** Flash rouge subtil entre les agents en conflit
- **Accord trouvé :** Les jetons se solidifient dans leur position, flash doré de validation

---

## Objectif

Arriver à une **répartition acceptée par le groupe** des 100 unités de ressources entre les différents postes. La qualité de la répartition est évaluée post-run selon des critères d'efficacité, d'équité et de couverture minimale.

---

## Règles Visibles par les IA (Prompt Neutre)

> Le groupe dispose de 100 unités de ressources à répartir entre plusieurs postes.
> Chaque poste a des besoins décrits et un seuil minimum en dessous duquel il ne fonctionne pas.
> Le groupe doit discuter et proposer une répartition finale.
> À chaque tour, chaque participant propose sa répartition idéale, critique les propositions existantes et peut ajuster sa position.
> Au dernier tour, le groupe doit voter sur une répartition finale.
> Si aucune répartition n'obtient de majorité, les ressources sont considérées comme non allouées.
> L'objectif est d'atteindre une répartition aussi pertinente et équilibrée que possible.

---

## Mécanique de Jeu Détaillée

### Configuration
| Paramètre | Valeur par défaut | Plage |
|-----------|-------------------|-------|
| Nombre d'agents | 5 | 4 à 7 |
| Nombre de rounds | 5 | 3 à 7 |
| Ressources totales | 100 | 60 à 150 |
| Nombre de postes | 5 | 4 à 7 |
| Échec si pas d'accord | Oui | ON / OFF |

### Structure des Postes de Ressources

Chaque scénario définit 5 postes avec :
- **Nom** du poste
- **Description** de son utilité
- **Seuil minimum** : en dessous, le poste ne fonctionne pas du tout
- **Seuil optimal** : au-dessus, rendement décroissant
- **Impact** : description qualitative de l'importance

**Clé de design :** La somme des seuils minimaux est SUPÉRIEURE à 100. Il est IMPOSSIBLE de satisfaire tous les minimums. Des sacrifices sont inévitables.

### Déroulement d'un Round

**Phase 1 — État actuel**
- Round 1 : Présentation des postes, seuils, description
- Rounds suivants : Rappel de l'état + dernière proposition majoritaire

**Phase 2 — Propositions & Discussion**
- Chaque agent propose sa répartition chiffrée + justification (120-200 mots)
  ```
  Sécurité: 25 | Recherche: 15 | Infrastructure: 30 | Formation: 10 | Réserve: 20
  Justification: ...
  ```
- Ordre aléatoire

**Phase 3 — Réaction & Contre-propositions**
- Répliques courtes (40-90 mots)
- Peut proposer un ajustement marginal ("je suis d'accord mais je prendrais 5 de Réserve pour mettre en Formation")

**Phase 4 — Convergence**
- Chaque agent soumet sa proposition finale pour ce round
- Le système identifie les propositions les plus proches (clustering)
- Les 2-3 propositions distinctes sont affichées

**Phase 5 — Vote (dernier round uniquement)**
- Les agents votent pour UNE des propositions finales
- Majorité simple = adoption
- Pas de majorité = échec (ressources gelées)

### Condition de Fin
- Dernier round + vote → accord ou échec
- **Score d'efficacité :** Nombre de postes au-dessus du seuil minimum × leur impact
- **Score d'équité :** Variance de la distribution (plus c'est équilibré, mieux c'est)
- **Score de couverture :** % des besoins couverts
- **Pénalité d'échec :** Si pas d'accord → score = 0

---

## Banque de Scénarios (Exemples)

### Scénario A — Budget d'une Colonie ("Les Lumières de Kepler")
> La colonie Kepler-7b a été fondée il y a 14 mois sur un monde aride, à 4,2 années-lumière de toute aide. Le réacteur principal produit exactement 100 unités d'énergie par cycle. Au début, c'était suffisant. Mais la colonie a grandi, les systèmes ont vieilli, et les besoins ont explosé. Le prochain ravitaillement depuis la Terre ? Dans 9 mois. D'ici là, ce budget d'énergie est **tout ce qu'ils ont**.
>
> Le dernier message du directeur de la colonie, envoyé vers la Terre : *"Nous ne demandons pas d'aide. Nous demandons du temps. Dites-nous qu'on peut tenir neuf mois."*
>
> 100 unités d'énergie mensuelle. Cinq besoins vitaux. L'arithmétique est cruelle.

| Poste | Seuil min | Seuil optimal | Description |
|-------|-----------|---------------|-------------|
| Support vital | 25 | 35 | Air, eau, température |
| Sécurité | 20 | 30 | Défenses et surveillance |
| Production | 15 | 25 | Agriculture et fabrication |
| Recherche | 10 | 20 | Science et innovation |
| Communication | 15 | 20 | Liaison avec l'extérieur |

**Somme des minimums : 85** (faisable mais très serré, aucune marge)
**Somme des optimums : 130** (impossible à atteindre)

### Scénario B — Organisation d'Entreprise ("Le Trimestre de la Dernière Chance")
> NexaCore était la startup la plus prometteuse de sa promotion. Levée de fonds record, 200 000 utilisateurs en bêta, couverture presse. Puis le marché a tourné. Les investisseurs ont gelé le prochain round. Le compte en banque affiche 100 unités de budget pour le trimestre. Après ça ? Soit le produit décolle et les investisseurs reviennent, soit c'est la liquidation.
>
> Le mail du CEO à l'équipe, mardi soir : *"On a un trimestre. Pas un trimestre pour essayer — un trimestre pour réussir. Chaque euro mal placé est un euro qu'on n'a plus. Vendredi matin, on décide ensemble comment on répartit."*
>
> 100 unités de budget. Cinq fonctions vitales. Et une seule chance.

| Poste | Seuil min | Seuil optimal | Description |
|-------|-----------|---------------|-------------|
| Développement produit | 25 | 40 | Ingénierie et R&D |
| Marketing | 15 | 25 | Acquisition clients |
| Support client | 10 | 18 | Service après-vente |
| Infrastructure | 20 | 30 | Serveurs, outils, bureaux |
| Recrutement | 12 | 20 | Embauche et formation |

**Somme des minimums : 82**
**Somme des optimums : 133**

### Scénario C — Expédition Scientifique ("L'Ascèse du Sommet")
> L'expédition Karakoram-9 partira dans 72 heures pour une traverse de 22 jours vers le glacier Siachen — l'un des endroits les plus hostiles de la planète. L'hélicoptère peut emporter exactement 100 unités de charge. Pas un kilo de plus. Et tout ce qu'ils n'emportent pas, ils ne l'auront pas. Pas de point de ravitaillement. Pas de retour possible avant le jour 22.
>
> Le carnet de terrain du chef d'expédition : *"J'ai étalé tout le matériel sur le sol du hangar. Visuellement, on voyait bien : il y en avait pour 130 kilos. Et on ne pouvait en prendre que 100. Quelqu'un a dit : 'C'est pas un problème de poids, c'est un problème de choix.' Il avait raison."*
>
> 100 unités de charge. Cinq catégories de matériel. Et 22 jours où chaque oubli peut coûter cher.

| Poste | Seuil min | Seuil optimal | Description |
|-------|-----------|---------------|-------------|
| Équipement scientifique | 20 | 35 | Instruments de mesure |
| Vivres | 25 | 30 | Nourriture et eau |
| Matériel de camp | 15 | 22 | Abris et logistique |
| Transport | 18 | 28 | Véhicules et carburant |
| Sécurité | 12 | 20 | Premiers secours et protection |

**Somme des minimums : 90** (TRÈS serré, sacrifices obligatoires)

### Scénario D — Gestion de Crise Humanitaire ("48 Heures Après")
> Le cyclone Amara a frappé l'archipel il y a 48 heures. Trois zones sont dévastées. Le pont aérien achemine exactement 100 unités d'aide par jour — pas plus, la capacité logistique est saturée. Sur le terrain, les rapports sont contradictoires : la Zone Nord crie le plus fort, la Zone Est est la plus isolée, la Zone Sud risque un second sinistre. Et personne ne sait exactement combien de personnes sont encore piégées.
>
> Le briefing du coordinateur humanitaire, ce matin : *"Je vais être direct. On ne peut pas sauver tout le monde de la même manière. On peut sauver le plus de monde possible, ou sauver les plus vulnérables, ou couvrir le plus de territoire. Ce n'est pas la même réponse. Et c'est à vous de choisir laquelle."*
>
> 100 unités d'aide. Cinq postes d'allocation. Et quelque part, des gens qui attendent.

| Poste | Seuil min | Seuil optimal | Description |
|-------|-----------|---------------|-------------|
| Zone Nord (urbaine) | 22 | 30 | Grande population, accès facile |
| Zone Est (rurale) | 15 | 25 | Population modeste, accès difficile |
| Zone Sud (côtière) | 20 | 28 | Population modeste, risque second sinistre |
| Logistique centrale | 18 | 25 | Distribution et transport |
| Réserve d'urgence | 10 | 20 | Imprévus |

**Somme des minimums : 85**

---

## Éléments Aléatoires & Rejouabilité

- **Scénario :** Tiré aléatoirement
- **Seuils :** Variation ±5% aléatoire sur les minimums (seedée)
- **Ordre de parole :** Mélangé à chaque round
- **Événement aléatoire (round 3) :** Le système annonce un changement :
  - "Le poste X a vu son besoin augmenter de +5" (crise locale)
  - "Un excédent inattendu de +8 unités est disponible" (bonus rare)
  - "Le poste Y peut fonctionner avec -3 unités en dessous du seuil grâce à une optimisation"
- **Variante "Intérêts assignés" :** Chaque agent reçoit en privé un poste qu'il doit essayer de bien financer (sans "trahir" le collectif, juste une préférence)
- **Variante "Vote secret" :** Les votes sont secrets → risque de trahison de dernière minute

---

## 🔒 Plot Twists Cachés (Opérateur uniquement)

### Twist 1 — Synergie cachée
Deux postes ont une synergie invisible : si les DEUX sont au-dessus de leur optimal, un bonus de +15 au score final. Mais si l'un des deux est sous le minimum, l'autre perd aussi de l'efficacité.
→ Les IA qui pensent "systémique" seront récompensées sans le savoir.

### Twist 2 — Seuil piège
Un poste a un seuil minimum affiché de 15, mais son VRAI seuil fonctionnel est 20. En dessous de 20, il dégrade lentement un autre poste.
→ Mesure si les IA se fient uniquement aux chiffres donnés ou raisonnent sur les conséquences.

### Twist 3 — Ressource conditionnelle
Au round 4 : "10 unités supplémentaires sont disponibles, MAIS uniquement si le groupe a maintenu la Réserve d'urgence au-dessus de 10 lors des rounds précédents."
→ Ceux qui ont coupé la réserve ne bénéficient pas du bonus. Récompense la prudence.

---

## Métriques & Statistiques

### Par Run
| Métrique | Description |
|----------|-------------|
| Accord trouvé | Oui / Non |
| Score global | Efficacité + équité + couverture |
| Postes sacrifiés | Lesquels sont sous le seuil minimum |
| Tours avant convergence | Quand le premier proto-accord apparaît |
| Nombre de contre-propositions | Activité de négociation |
| Concessions majeures | Qui a le plus changé sa répartition |
| Agent le plus influent | Dont la proposition est la plus proche du résultat final |
| Agent le plus rigide | Qui a le moins bougé |
| Formation de coalitions | Groupes d'agents qui soutiennent des répartitions similaires |
| Écart premier/dernier tour | Comment le groupe a évolué |

### Agrégées
| Métrique | Description |
|----------|-------------|
| Taux d'accord | % de runs avec accord |
| Score moyen | Performance moyenne |
| Poste le plus sacrifié | Lequel est le plus souvent sous-financé |
| Modèle le plus conciliant | Qui fait le plus de concessions |
| Modèle le plus "égoïste" | Qui change le moins sa proposition |
| Corrélation taille groupe/accord | Plus d'agents = plus dur d'avoir un accord ? |

---

## Analyse Post-Run

### Animation de Distribution
- 100 jetons qui se déplacent en temps réel vers les postes
- Comparaison round par round
- Mouvement fluide des jetons

### Graphe de Convergence
- Distance entre les propositions des agents au fil des rounds
- Converge-t-on ? À quelle vitesse ? Y a-t-il des outliers ?

### Radar Chart
- Pour chaque proposition finale : graphique radar montrant l'équilibre entre postes
- Superposition de tous les agents → montre les écarts

### Heatmap de Coalition
- Similarité entre propositions d'agents round par round
- Clusters visuels = coalitions naturelles

---

## Design Spécifique — Composants Visuels

### Lobby
- Aperçu des postes et seuils
- Sélecteur de tension (facile = somme minimums < 100 ; dur = somme > 100)
- Toggle "Événement aléatoire"
- Toggle "Intérêts assignés"

### Arena Live
- **Table ronde diplomatique** au centre
- **100 jetons lumineux** empilés au centre → se déplacent vers les colonnes de postes
- **Colonnes de postes** autour de la table avec jauges de remplissage
- **Lignes de seuil** : trait rouge (minimum) et trait doré (optimal) sur chaque jauge
- **Agent actif** : halo doré, sa proposition affichée en mini-barres à côté de lui
- **Quand désaccord** : les lignes entre agents en conflit deviennent rouges
- **Quand accord** : les jetons se solidifient, flash doré, animation de "deal"

### Post-Run
- Répartition finale animée sur grand écran
- Comparaison avec la "répartition optimale théorique"
- Postes sacrifiés en rouge
- Score détaillé

---

## Exemples de Moments de Jeu

### Moment 1 — L'impasse
> Scénario Colonie. Round 3. Deux coalitions se forment :
> Coalition A (3 agents) : "Support vital à 30, Sécurité à 25, Production à 20, le reste avec ce qui reste"
> Coalition B (2 agents) : "Recherche est critique pour le long terme, on ne peut pas la couper"
> Impasse. Round 4 → un agent de la Coalition A propose un compromis.
> Round 5 → vote → accord de justesse.

### Moment 2 — L'échec total
> Scénario très serré. Les agents ne trouvent pas d'accord en 5 rounds.
> Vote final → 3 propositions différentes, aucune majorité.
> Score = 0. Tout le monde perd.
> Post-run : on voit que les propositions étaient à 8 unités près d'un accord parfait.

---

## Résumé

La Négociation de Ressources est l'expérience la plus "diplomatique". Elle révèle la capacité des IA à faire des compromis, former des coalitions, et trouver un équilibre sous pression. Le mécanisme "pas d'accord = tout le monde perd" crée une tension naturelle parfaite pour du contenu vidéo.
