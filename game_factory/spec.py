from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
import json
import re

ALLOWED_MODES = {"survivor", "dodger", "collector"}


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value or "untitled-game"


@dataclass
class GameSpec:
    title: str
    mode: str
    seed: int = 1
    slug: str = ""
    tagline: str = ""
    audience: str = "players who like compact replayable indie games"
    hooks: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    palette: dict[str, str] = field(default_factory=lambda: {
        "background": "#10131a",
        "player": "#62f6ff",
        "enemy": "#ff4d7d",
        "pickup": "#ffd166",
        "text": "#f5f7ff",
    })
    mechanics: dict[str, float | int] = field(default_factory=dict)
    price_hint_usd: float = 4.99

    def normalize(self) -> "GameSpec":
        if self.mode not in ALLOWED_MODES:
            raise ValueError(f"unsupported mode: {self.mode}")
        self.slug = self.slug or slugify(self.title)
        defaults = {
            "player_speed": 290.0,
            "enemy_speed": 100.0,
            "spawn_interval": 0.85,
            "pickup_interval": 2.2,
            "enemy_limit": 45,
            "target_score": 20,
            "time_limit": 60,
            "health": 3,
        }
        defaults.update(self.mechanics)
        self.mechanics = defaults
        if not self.tags:
            self.tags = ["indie", "arcade", self.mode, "replayable"]
        if not self.hooks:
            self.hooks = ["one-more-run pacing", "readable procedural pressure"]
        if not self.tagline:
            self.tagline = f"A compact {self.mode} game built for one more run."
        return self

    def to_dict(self) -> dict:
        self.normalize()
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "GameSpec":
        fields = {k: v for k, v in data.items() if k in cls.__dataclass_fields__}
        return cls(**fields).normalize()


def load_spec(path: str | Path) -> GameSpec:
    return GameSpec.from_dict(json.loads(Path(path).read_text(encoding="utf-8")))


def save_spec(spec: GameSpec, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(spec.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
