# ⚔️ ARENA — Multi-Agent Experimental Platform

Plateforme expérimentale pour observer comment des agents LLM interagissent dans des scénarios de débat, négociation et prise de décision collective.

## 🏗️ Architecture

```
ARENA/
├── Blueprint/          # 12 fichiers de spécification
├── backend/            # Python + FastAPI
│   ├── app/
│   │   ├── api/        # Routes REST + WebSocket
│   │   ├── core/       # Engine, Agent, RoundManager, Seed, Prompts
│   │   ├── experiments/ # 10 expériences (EXP01-EXP10)
│   │   ├── models/     # Pydantic models
│   │   ├── providers/  # Ollama, LM Studio, OpenRouter
│   │   ├── storage/    # Persistance JSON + export
│   │   └── main.py     # Entry point FastAPI
│   └── data/           # Runs + presets (JSON)
└── frontend/           # React + TypeScript + Vite
    └── src/
        ├── components/ # Layout + UI (Button, Card, Slider, etc.)
        ├── pages/      # Hub, Lobby, Arena, Analysis
        ├── services/   # API client + WebSocket
        ├── stores/     # Zustand (experiments, arena, providers)
        └── types.ts    # TypeScript types
```

## 🚀 Lancement rapide

### Prérequis

- **Python 3.11+**
- **Node.js 18+**
- Un fournisseur LLM local ou cloud :
  - [Ollama](https://ollama.ai) (recommandé, localhost:11434)
  - [LM Studio](https://lmstudio.ai) (localhost:1234)
  - [OpenRouter](https://openrouter.ai) (cloud, nécessite une API key)

### Backend

```powershell
# PowerShell (Windows) — une commande par ligne, ou séparées par ;
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

```bash
# macOS / Linux
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Le backend sera accessible sur `http://localhost:8000`.  
Documentation API interactive : `http://localhost:8000/docs`

### Frontend

```bash
cd frontend

# Installer les dépendances
npm install

# Lancer le serveur de développement
npm run dev
```

Le frontend sera accessible sur `http://localhost:5173`.

## 🔧 Configuration

### Providers LLM

Au démarrage, l'application cherche les providers configurés dans `backend/data/settings.json`.

Par défaut :
- **Ollama** : `http://localhost:11434` (activé)
- **LM Studio** : `http://localhost:1234` (activé)
- **OpenRouter** : nécessite une API key

Pour ajouter une API key OpenRouter, modifiez les settings via l'API :
```bash
curl -X PUT http://localhost:8000/api/settings \
  -H "Content-Type: application/json" \
  -d '{"providers": {"openrouter": {"type": "openrouter", "enabled": true, "endpoint": "https://openrouter.ai/api/v1", "api_key": "sk-your-key"}}}'
```

## 🧪 Les 10 Expériences

| # | Nom | Icône | Type |
|---|-----|-------|------|
| 01 | Budget du Groupe | 💰 | Gestion de ressources |
| 02 | Conseil de Crise | 🚨 | Prise de décision sous pression |
| 03 | Le Traître Invisible | 🎭 | Rôle secret + déduction |
| 04 | Enquête Collective | 🔍 | Investigation collaborative |
| 05 | Négociation de Ressources | ⚖️ | Négociation multi-parties |
| 06 | Le Pouvoir qui Tourne | 👑 | Pouvoir rotatif |
| 07 | L'Information Fragmentée | 🧩 | Puzzle informationnel |
| 08 | Répartition des Priorités | 📊 | Portfolio de projets |
| 09 | Construction d'une Règle | ⚖️ | Mini-constitution |
| 10 | La Loi du Groupe | 📜 | Émergence de normes |

## 📡 API

| Méthode | Route | Description |
|---------|-------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/experiments` | Liste des expériences |
| GET | `/api/experiments/{id}` | Détail d'une expérience |
| GET | `/api/providers` | Liste des providers |
| GET | `/api/providers/{type}/models` | Modèles disponibles |
| POST | `/api/providers/{type}/test` | Tester un provider |
| GET | `/api/runs` | Historique des runs |
| POST | `/api/runs` | Lancer une expérience |
| GET | `/api/runs/{id}` | Détail d'un run |
| DELETE | `/api/runs/{id}` | Supprimer un run |
| GET | `/api/runs/{id}/export/{fmt}` | Export (json, csv, md) |
| GET/PUT | `/api/settings` | Configuration |
| WS | `/ws/arena` | WebSocket temps réel |

## 🎨 Flux utilisateur

1. **Hub** — Choix d'une expérience parmi les 10 cartes
2. **Lobby** — Configuration : modèle, scénario, agents, paramètres
3. **Arena** — Observation en temps réel du débat (WebSocket)
4. **Analysis** — Métriques, transcript, export

## 📝 Licence

Projet expérimental — usage personnel.
