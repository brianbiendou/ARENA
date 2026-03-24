"""Application configuration management."""

from __future__ import annotations

import json
import os
from pathlib import Path

from dotenv import load_dotenv

from .models.settings import AppSettings, ProviderType

_CONFIG_FILE = "arena_settings.json"

# Load .env from backend root
load_dotenv(Path(__file__).resolve().parent.parent / ".env")


def get_data_dir() -> Path:
    """Return the data directory, creating it if needed."""
    data_dir = Path(__file__).resolve().parent.parent / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


def get_config_path() -> Path:
    return get_data_dir() / _CONFIG_FILE


def load_settings() -> AppSettings:
    """Load settings from disk, or return defaults.  Inject env-based API key."""
    config_path = get_config_path()
    if config_path.exists():
        raw = json.loads(config_path.read_text(encoding="utf-8"))
        settings = AppSettings.model_validate(raw)
    else:
        settings = AppSettings()

    # Inject OpenRouter key from env if not already set in saved config
    env_key = os.getenv("OPENROUTER_API_KEY")
    if env_key:
        or_config = settings.providers.get(ProviderType.OPENROUTER)
        if or_config and not or_config.api_key:
            or_config.api_key = env_key

    return settings


def save_settings(settings: AppSettings) -> None:
    """Persist settings to disk."""
    config_path = get_config_path()
    config_path.write_text(
        settings.model_dump_json(indent=2),
        encoding="utf-8",
    )
