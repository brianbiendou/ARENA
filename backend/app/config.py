"""Application configuration management."""

from __future__ import annotations

import json
from pathlib import Path

from .models.settings import AppSettings

_CONFIG_FILE = "arena_settings.json"


def get_data_dir() -> Path:
    """Return the data directory, creating it if needed."""
    data_dir = Path(__file__).resolve().parent.parent / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


def get_config_path() -> Path:
    return get_data_dir() / _CONFIG_FILE


def load_settings() -> AppSettings:
    """Load settings from disk, or return defaults."""
    config_path = get_config_path()
    if config_path.exists():
        raw = json.loads(config_path.read_text(encoding="utf-8"))
        return AppSettings.model_validate(raw)
    return AppSettings()


def save_settings(settings: AppSettings) -> None:
    """Persist settings to disk."""
    config_path = get_config_path()
    config_path.write_text(
        settings.model_dump_json(indent=2),
        encoding="utf-8",
    )
