from __future__ import annotations

import json
import os
import re
import urllib.request
from .ideation import concept_fingerprint, generate_ideas
from .spec import GameSpec


def _extract_json(value: str):
    value = value.strip()
    value = re.sub(r"^```(?:json)?\s*", "", value)
    value = re.sub(r"\s*```$", "", value)
    return json.loads(value)


def generate_ai_ideas(count: int, seed: int, mode_weights: dict[str, float] | None = None) -> list[GameSpec]:
    endpoint = os.getenv("GAME_FACTORY_LLM_ENDPOINT")
    if not endpoint:
        raise RuntimeError("GAME_FACTORY_LLM_ENDPOINT is not configured")
    model = os.getenv("GAME_FACTORY_LLM_MODEL", "game-planner")
    bearer = os.getenv("GAME_FACTORY_LLM_BEARER")
    prompt = f"""Generate {count} original small commercial indie game concepts as a JSON array.
Seed: {seed}. Preferred mode weights: {mode_weights or {}}.
Each object must have: title, mode (survivor|dodger|collector), tagline, hooks (3), tags (5), palette, mechanics, price_hint_usd.
mechanics must include player_speed, enemy_speed, spawn_interval, pickup_interval, enemy_limit, target_score, time_limit, health.
Do not imitate named games, characters, brands, copyrighted settings, or trademarks. Prefer a mechanically clear one-sentence hook, primitive/procedural visuals, short sessions, and testable rules. Return JSON only."""
    payload = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a game portfolio planner. Output valid JSON only."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.9,
    }).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if bearer:
        headers["Authorization"] = f"Bearer {bearer}"
    req = urllib.request.Request(endpoint, data=payload, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=90) as response:
        data = json.loads(response.read().decode("utf-8"))
    if isinstance(data, list):
        raw = data
    elif isinstance(data, dict) and isinstance(data.get("ideas"), list):
        raw = data["ideas"]
    else:
        content = data["choices"][0]["message"]["content"]
        raw = _extract_json(content)
    ideas: list[GameSpec] = []
    seen: set[str] = set()
    for idx, item in enumerate(raw[:count]):
        item = dict(item)
        item.setdefault("seed", seed + idx + 1)
        spec = GameSpec.from_dict(item)
        fp = concept_fingerprint(spec)
        if fp not in seen:
            seen.add(fp)
            ideas.append(spec)
    if len(ideas) < count:
        for spec in generate_ideas(count * 2, seed + 991, mode_weights):
            fp = concept_fingerprint(spec)
            if fp not in seen:
                seen.add(fp)
                ideas.append(spec)
            if len(ideas) >= count:
                break
    return ideas[:count]
