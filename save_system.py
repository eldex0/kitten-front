"""Sauvegardes JSON et paramètres persistants de KITTEN FRONT."""
from __future__ import annotations

from dataclasses import asdict
import json
from pathlib import Path

from dot_warfare import DotBattlefield, DotUnit
from game_model import Battle, Event, GameState, Province

ROOT = Path(__file__).resolve().parent
SAVE_PATH = ROOT / "savegame.json"
SETTINGS_PATH = ROOT / "frontline_settings.json"

DEFAULT_SETTINGS = {
    "language": "Français",
    "onboarding_complete": False,
    "fullscreen": False,
    "front_quality": "Élevée",
    "tooltips": True,
    "autosave": True,
    "default_difficulty": "Officier",
    "starting_resources": "Normales",
    "unit_density": "Normale",
    "day_length": "Normal",
    "capture_speed": "Normale",
    "default_speed": 1,
    "pause_on_capture": True,
    "always_health_bars": False,
    "show_front": True,
}


def load_settings(path: Path = SETTINGS_PATH) -> dict:
    settings = DEFAULT_SETTINGS.copy()
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(raw, dict):
            settings.update({k: raw[k] for k in DEFAULT_SETTINGS if k in raw})
    except (OSError, ValueError, TypeError):
        pass
    return settings


def save_settings(settings: dict, path: Path = SETTINGS_PATH) -> None:
    payload = {k: settings.get(k, v) for k, v in DEFAULT_SETTINGS.items()}
    _atomic_json(path, payload)


def has_save(path: Path = SAVE_PATH) -> bool:
    return path.is_file()


def save_game(game: GameState, field: DotBattlefield, meta: dict, path: Path = SAVE_PATH) -> None:
    game_data = asdict(game)
    payload = {
        "version": 1,
        "meta": meta,
        "game": game_data,
        "field": {
            "units": [asdict(u) for u in field.units],
            "next_uid": field.next_uid,
            "pending": {str(k): v for k, v in field.pending.items()},
            "eco": field.eco,
            "production": field.production,
            "heavy_ratio": field.heavy_ratio,
            "production_clock": field.production_clock,
            "capture": field.capture,
            "ai_clock": field.ai_clock,
            "difficulty": field.difficulty,
            "capture_duration": field.capture_duration,
        },
    }
    _atomic_json(path, payload)


def load_game(path: Path = SAVE_PATH) -> tuple[GameState, DotBattlefield, dict]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if raw.get("version") != 1:
        raise ValueError("Version de sauvegarde incompatible")
    gd = raw["game"]
    game = GameState(
        provinces={k: Province(**v) for k, v in gd.pop("provinces").items()},
        battles=[Battle(**v) for v in gd.pop("battles")],
        events=[Event(**v) for v in gd.pop("events")],
        **gd,
    )
    fd = raw["field"]
    field = DotBattlefield(game, fd.get("difficulty", "Officier"), spawn_initial=False)
    field.units = [DotUnit(**{**u, "path": [tuple(p) for p in u.get("path", [])]}) for u in fd["units"]]
    field.next_uid = fd["next_uid"]
    field.pending = {int(k): [tuple(p) for p in v] for k, v in fd.get("pending", {}).items()}
    for name in ("eco", "production", "heavy_ratio", "production_clock", "capture"):
        setattr(field, name, fd.get(name, getattr(field, name)))
    field.ai_clock = fd.get("ai_clock", 0.0)
    field.capture_duration = fd.get("capture_duration", 4.0)
    return game, field, raw.get("meta", {})


def _atomic_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    temporary.replace(path)
