from __future__ import annotations

import json
import shutil
from pathlib import Path
from .marketing import generate_marketing_pack
from .spec import GameSpec, save_spec

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "templates" / "godot_minimal"


def generate_project(spec: GameSpec, out_root: str | Path) -> Path:
    spec.normalize()
    dest = Path(out_root) / spec.slug
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(TEMPLATE, dest)
    project_file = dest / "project.godot"
    project_file.write_text(project_file.read_text(encoding="utf-8").replace("__TITLE__", spec.title), encoding="utf-8")
    save_spec(spec, dest / "game_spec.json")
    generate_marketing_pack(spec, dest / "marketing")
    (dest / "factory-metadata.json").write_text(json.dumps({
        "generator": "autonomous-game-factory",
        "schema": 1,
        "source_mode": spec.mode,
        "seed": spec.seed,
    }, indent=2), encoding="utf-8")
    return dest
