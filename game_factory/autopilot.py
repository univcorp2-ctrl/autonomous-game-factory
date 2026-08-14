from __future__ import annotations

import json
from pathlib import Path
from .generator import generate_project
from .ideation import concept_fingerprint, generate_ideas, load_preferences
from .qa import write_qa_report


def _rank(spec) -> float:
    m = spec.mechanics
    hook_bonus = len(set(spec.hooks)) * 7.5
    pacing = max(0.0, 25.0 - abs(float(m["spawn_interval"]) - 0.9) * 20.0)
    readability = min(20.0, len(set(spec.palette.values())) * 4.0)
    price_fit = 15.0 if spec.price_hint_usd <= 5.99 else 10.0
    return hook_bonus + pacing + readability + price_fit


def run_batch(count: int, keep: int, seed: int, out_root: str | Path, preferences: str | Path | None = None) -> dict:
    weights = load_preferences(preferences)
    ideas = generate_ideas(count, seed, weights)
    ranked = sorted(ideas, key=_rank, reverse=True)[:keep]
    root = Path(out_root)
    root.mkdir(parents=True, exist_ok=True)
    portfolio = []
    for spec in ranked:
        project = generate_project(spec, root)
        qa = write_qa_report(project)
        portfolio.append({
            "slug": spec.slug,
            "title": spec.title,
            "mode": spec.mode,
            "concept_fingerprint": concept_fingerprint(spec),
            "idea_score": round(_rank(spec), 2),
            "qa_score": qa.score,
            "path": str(project),
        })
    result = {"seed": seed, "generated": len(ideas), "kept": len(portfolio), "portfolio": portfolio}
    (root / "portfolio.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result
