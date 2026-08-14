from __future__ import annotations

import json
from pathlib import Path
from .spec import GameSpec


def generate_marketing_pack(spec: GameSpec, out_dir: str | Path) -> Path:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    hooks = "\n".join(f"- {h}" for h in spec.hooks)
    tags = ", ".join(spec.tags)
    short = f"{spec.title} is a compact {spec.mode} game where {spec.hooks[0]}."
    long_copy = f"""# {spec.title}\n\n**{spec.tagline}**\n\n{short} Designed around short sessions, instant readability, and repeatable runs.\n\n## Key features\n{hooks}\n\n## Audience\n{spec.audience}\n\n## Suggested tags\n{tags}\n\n## Pricing hypothesis\nUSD {spec.price_hint_usd:.2f} before regional pricing and store review.\n"""
    (out / "store-copy.md").write_text(long_copy, encoding="utf-8")
    (out / "social-posts.md").write_text(
        f"""# Social copy\n\n1. {spec.tagline} Wishlist / follow for playtest updates. #{spec.mode} #indiedev\n\n2. Built around: {spec.hooks[1]}. Would you optimize for safety or score?\n\n3. New prototype: {spec.title}. Short runs, readable pressure, fast restart.\n""",
        encoding="utf-8",
    )
    (out / "trailer-shotlist.md").write_text(
        """# 30-second trailer shot list\n\n- 0-03s: title + strongest visual contrast\n- 03-08s: player movement and core objective\n- 08-14s: pressure escalation\n- 14-20s: scoring / pickup decision\n- 20-25s: near-failure moment\n- 25-30s: title, CTA, platform logos only after store approval\n""",
        encoding="utf-8",
    )
    asset_manifest = {
        "capsule": ["header", "small_capsule", "main_capsule", "library_hero"],
        "screenshots": 6,
        "trailer_seconds": 30,
        "copy": ["short_description", "long_description", "feature_bullets", "tags"],
        "notes": "Generate final dimensions from each store's current official requirements before submission.",
    }
    (out / "asset-manifest.json").write_text(json.dumps(asset_manifest, indent=2), encoding="utf-8")
    return out
