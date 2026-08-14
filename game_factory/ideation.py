from __future__ import annotations

import hashlib
import json
import random
from pathlib import Path
from .spec import GameSpec

ADJECTIVES = ["Neon", "Tiny", "Broken", "Last", "Lucky", "Void", "Chrome", "Pocket", "Midnight", "Solar", "Rust", "Echo"]
NOUNS = ["Harvest", "Drift", "Circuit", "Garden", "Vault", "Courier", "Beacon", "Swarm", "Signal", "Ritual", "Relay", "Orbit"]
HOOKS = [
    "difficulty rises every 15 seconds",
    "score multipliers reward risky movement",
    "short runs with immediate restarts",
    "enemy pressure changes with player score",
    "pickups force route-planning decisions",
    "high-contrast shapes keep the action readable",
    "a single rule twist changes the optimal route",
    "accessibility-friendly difficulty parameters",
]
PALETTES = [
    {"background":"#0b1020","player":"#53f6ff","enemy":"#ff477e","pickup":"#ffd166","text":"#f8fbff"},
    {"background":"#17110c","player":"#9cff57","enemy":"#ff6b35","pickup":"#ffe66d","text":"#fff8e7"},
    {"background":"#120d1f","player":"#c77dff","enemy":"#ff4d6d","pickup":"#80ffdb","text":"#f7f0ff"},
    {"background":"#071a16","player":"#64ffda","enemy":"#ff8a80","pickup":"#ffd54f","text":"#e8fff8"},
]


def _pick_mode(rng: random.Random, weights: dict[str, float] | None) -> str:
    modes = ["survivor", "dodger", "collector"]
    if not weights:
        return rng.choice(modes)
    vals = [max(0.01, float(weights.get(mode, 1.0))) for mode in modes]
    return rng.choices(modes, vals, k=1)[0]


def concept_fingerprint(spec: GameSpec) -> str:
    payload = json.dumps({
        "mode": spec.mode,
        "hooks": sorted(spec.hooks),
        "palette": spec.palette,
        "mechanics": spec.mechanics,
    }, sort_keys=True)
    return hashlib.sha256(payload.encode()).hexdigest()[:16]


def generate_ideas(count: int, seed: int, mode_weights: dict[str, float] | None = None) -> list[GameSpec]:
    rng = random.Random(seed)
    seen: set[str] = set()
    ideas: list[GameSpec] = []
    attempts = 0
    while len(ideas) < count and attempts < count * 20:
        attempts += 1
        mode = _pick_mode(rng, mode_weights)
        title = f"{rng.choice(ADJECTIVES)} {rng.choice(NOUNS)}"
        mechanics = {
            "player_speed": rng.randint(240, 370),
            "enemy_speed": rng.randint(75, 155),
            "spawn_interval": round(rng.uniform(0.5, 1.35), 2),
            "pickup_interval": round(rng.uniform(1.4, 3.2), 2),
            "enemy_limit": rng.randint(24, 64),
            "target_score": rng.randint(12, 36),
            "time_limit": rng.choice([45, 60, 75, 90]),
            "health": rng.choice([2, 3, 4]),
        }
        hooks = rng.sample(HOOKS, 3)
        spec = GameSpec(
            title=title,
            mode=mode,
            seed=rng.randint(1, 2_000_000_000),
            tagline=f"{title}: {hooks[0].capitalize()}.",
            hooks=hooks,
            tags=["indie", "arcade", mode, "short-session", "replayable"],
            palette=dict(rng.choice(PALETTES)),
            mechanics=mechanics,
            price_hint_usd=rng.choice([2.99, 3.99, 4.99, 5.99, 7.99]),
        ).normalize()
        fp = concept_fingerprint(spec)
        if fp not in seen:
            seen.add(fp)
            ideas.append(spec)
    return ideas


def load_preferences(path: str | Path | None) -> dict[str, float] | None:
    if not path:
        return None
    p = Path(path)
    if not p.exists():
        return None
    data = json.loads(p.read_text(encoding="utf-8"))
    return data.get("mode_weights")
