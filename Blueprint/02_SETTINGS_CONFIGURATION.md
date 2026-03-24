# ARENA — Settings & Configuration

## Vue d'ensemble

L'espace Settings est une zone globale accessible depuis n'importe quel écran de l'application. Il centralise la gestion des modèles IA, les paramètres d'expérience, les presets, la sauvegarde et les options avancées.

---

## 1. Gestion des Modèles

### 1.1 Modèles Cloud (OpenRouter)

**Source des données :** API OpenRouter (https://openrouter.ai/api/v1/models)

**Pour chaque modèle cloud, afficher :**
- Nom du modèle (ex: `anthropic/claude-sonnet-4-20250514`, `openai/gpt-4o`, `google/gemini-2.5-pro`)
- Provider (Anthropic, OpenAI, Google, Meta, Mistral, DeepSeek, etc.)
- Toggle ON/OFF (activer/désactiver pour les expériences)
- Badge : Gratuit / Payant
- Coût input par million de tokens
- Coût output par million de tokens
- Contexte max (tokens)
- Statut de connectivité : ✅ connecté / ❌ erreur / ⏳ test en cours
- Bouton "Test de connectivité" (ping rapide)

**Organisation visuelle :**
- Liste triable par : nom, provider, coût, contexte max
- Filtres : gratuit uniquement / payant / tous
- Filtres par provider
- Recherche textuelle
- Cards avec micro-animations : glow au hover, check animé à l'activation du toggle

**Configuration requise :**
- Champ pour la clé API OpenRouter
- Indicateur de validité de la clé
- Quotas restants si disponibles via l'API
- Bouton "Rafraîchir la liste des modèles"

---

### 1.2 Modèles Locaux

**Providers supportés :**
- **Ollama** : détection automatique via `http://localhost:11434/api/tags`
- **LM Studio** : détection via endpoint local configurable

**Pour chaque modèle local, afficher :**
- Nom du modèle (ex: `llama3.2:8b`, `mistral:7b`, `qwen2.5:14b`)
- Provider : Ollama / LM Studio
- Taille du modèle (paramètres)
- Toggle ON/OFF
- Statut : chargé en mémoire / disponible / indisponible / erreur
- Endpoint utilisé
- Badge "LOCAL" bien visible
- Bouton "Test local" (envoi d'un prompt de vérification)

**Organisation visuelle :**
- Séparation claire des modèles locaux vs cloud (tabs ou sections)
- Indicateur visuel de charge système (RAM/VRAM si accessible)
- Refresh automatique des modèles disponibles

**Configuration :**
- URL de l'endpoint Ollama (défaut : `http://localhost:11434`)
- URL de l'endpoint LM Studio (défaut : `http://localhost:1234`)
- Timeout de connexion
- Bouton "Scanner les modèles locaux"

---

## 2. Presets de Sélection de Modèles

Des configurations pré-enregistrées pour lancer rapidement des expériences.

### Presets prédéfinis :
| Preset | Description |
|--------|-------------|
| **Cloud Premium** | Uniquement les meilleurs modèles cloud (Claude, GPT-4o, Gemini Pro) |
| **Cloud Mix** | Mélange de modèles cloud variés (petits + gros) |
| **Local Only** | Uniquement les modèles locaux Ollama/LM Studio |
| **Tiny Models** | Modèles les plus petits/rapides (test de vitesse) |
| **Frontier Compare** | Top modèles de chaque provider pour comparaison directe |
| **Full Battle** | Tous les modèles activés (locaux + cloud) |

### Presets personnalisés :
- Bouton "Sauvegarder la sélection courante comme preset"
- Nom personnalisé
- Notes optionnelles
- Possibilité de supprimer/renommer les presets custom

---

## 3. Paramètres d'Expérience (globaux)

Ces paramètres ont des valeurs par défaut mais peuvent être modifiés dans le lobby de chaque expérience.

### 3.1 Agents
| Paramètre | Défaut | Options |
|-----------|--------|---------|
| Nombre d'agents | 5 | 3 à 12 |
| Attribution des modèles | Aléatoire parmi les activés | Manuelle ou aléatoire |
| Couleur d'identité | Automatique | Palette de 12 couleurs distinctes |

### 3.2 Rounds / Tours
| Paramètre | Défaut | Options |
|-----------|--------|---------|
| Nombre de rounds | 5 | 2 à 15 |
| Ordre de parole | Aléatoire par round | Aléatoire / Fixe / Tournant |
| Réaction courte | Activée | ON / OFF |
| Durée max réponse (tokens) | 300 | 100 à 800 |
| Durée max réaction (tokens) | 100 | 40 à 200 |

### 3.3 Vote
| Paramètre | Défaut | Options |
|-----------|--------|---------|
| Mode de vote | Public | Public / Secret / Mixte |
| Type de vote | Majorité simple | Majorité / Unanimité / Classement |
| Fréquence de vote | Chaque round | Chaque round / Tous les 2 rounds / Final uniquement |

### 3.4 Aléatoire & Rejouabilité
| Paramètre | Défaut | Options |
|-----------|--------|---------|
| Seed | Aléatoire | Fixe (saisie manuelle) / Aléatoire |
| Forcer même seed pour batch | Non | ON / OFF |
| Seed incrémentale (batch) | Oui | ON / OFF |

### 3.5 Mode Batch
| Paramètre | Défaut | Options |
|-----------|--------|---------|
| Nombre de runs | 1 | 1 à 500 |
| Pause entre runs (ms) | 2000 | 0 à 30000 |
| Variation de seed | Incrémentale | Incrémentale / Full random |
| Variation d'agents | Même sélection | Même / Rotation / Shuffle |

---

## 4. Paramètres de Sauvegarde

| Paramètre | Défaut | Options |
|-----------|--------|---------|
| Autosave | Activé | ON / OFF |
| Sauvegarder transcript MD | Oui | ON / OFF |
| Sauvegarder replay JSON | Oui | ON / OFF |
| Sauvegarder métriques | Oui | ON / OFF |
| Sauvegarder prompts complets | Oui | ON / OFF |
| Dossier de destination | `./data/runs/` | Chemin personnalisable |
| Compression des vieux runs | OFF | ON / OFF (zip après X jours) |

---

## 5. Paramètres d'Affichage & UX

| Paramètre | Défaut | Options |
|-----------|--------|---------|
| Thème global | Dark Premium | Dark Premium / Dark Contrast / Midnight |
| Animations | Activées | ON / OFF / Réduites |
| Vitesse d'animation | Normale | Lente / Normale / Rapide |
| Taille du texte | Moyenne | Petite / Moyenne / Grande |
| Layout Arena | Cercle | Cercle / Demi-cercle / Grille / Constellation |
| Afficher latence agents | Oui | ON / OFF |
| Afficher tokens consommés | Oui | ON / OFF |
| Son lors des votes | OFF | ON / OFF |

---

## 6. Paramètres d'Export

| Paramètre | Défaut | Options |
|-----------|--------|---------|
| Format d'export métriques | JSON + CSV | JSON / CSV / Les deux |
| Export transcript | Markdown | Markdown / JSON / Les deux |
| Inclure les prompts dans l'export | Non | ON / OFF |
| Export snapshot PNG | OFF | ON / OFF |
| Dossier d'export | `./data/exports/` | Chemin personnalisable |

---

## 7. Paramètres Avancés

### 7.1 Moteur de Session
| Paramètre | Défaut | Description |
|-----------|--------|-------------|
| Timeout réponse agent | 60s | Temps max avant de passer au suivant |
| Retry sur erreur | 1 | Nombre de tentatives si un agent ne répond pas |
| Fallback si modèle indisponible | Ignorer | Ignorer / Remplacer par un autre / Arrêter |
| Temperature globale | 0.7 | Température envoyée aux modèles (0.0 à 2.0) |
| Top-p global | 0.9 | Nucleus sampling (0.0 à 1.0) |

### 7.2 Plot Twists (Section Opérateur)
- Section spéciale visible uniquement par l'opérateur (pas dans les prompts)
- Toggle global : Activer / Désactiver les plot twists
- Pour chaque expérience : toggle spécifique
- Intensité des twists : Subtil / Modéré / Fort
- Moment d'injection : Début / Milieu / Fin / Aléatoire

### 7.3 Logs de Debug
| Paramètre | Défaut | Description |
|-----------|--------|-------------|
| Log complet des prompts | OFF | Sauvegarder chaque prompt envoyé exactement |
| Log des réponses brutes | OFF | Sauvegarder les réponses non parsées |
| Log des erreurs API | ON | Toujours actif par défaut |
| Console de debug visible | OFF | Panneau de debug en bas de l'écran |

---

## 8. Design de l'Écran Settings

### Layout :
- Navigation par tabs verticales à gauche :
  - 🤖 Modèles Cloud
  - 💻 Modèles Locaux
  - ⚡ Presets
  - 🎮 Expérience
  - 💾 Sauvegarde
  - 🎨 Affichage
  - 📤 Export
  - ⚙️ Avancé

### Style :
- Même dark mode premium que le reste de l'app
- Cards de paramètres avec labels clairs
- Toggles fluides avec animation de switch
- Sliders avec valeur affichée en temps réel
- Tooltips explicatifs au hover
- Bouton "Restaurer les valeurs par défaut" par section
- Bouton global "Sauvegarder" en bas (sticky)

### Cards de modèles :
- Disposition en grille ou liste
- Card avec : logo provider, nom, badges, toggle, infos
- Glow au hover
- Check animé vert à l'activation
- Croix rouge discrète à la désactivation
- Indicateur de santé en temps réel (petit cercle coloré)

---

## 9. Raccourcis & Actions Rapides

| Action | Raccourci |
|--------|-----------|
| Ouvrir Settings | `Ctrl + ,` |
| Toggle tous les modèles cloud | Bouton dédié |
| Toggle tous les modèles locaux | Bouton dédié |
| Scanner les modèles locaux | `Ctrl + R` dans Settings |
| Sauvegarder preset courant | `Ctrl + S` dans Settings |
| Lancer test de connectivité global | Bouton "Test All" |

---

## Résumé

Les Settings d'ARENA doivent être un panneau de contrôle complet mais intuitif. Un opérateur doit pouvoir en 30 secondes : activer ses modèles, choisir un preset, configurer les paramètres de base, et lancer. Mais il doit aussi pouvoir aller en profondeur pour des runs de recherche batch à grande échelle avec des paramètres fins.
