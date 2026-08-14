from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import dataclass, asdict
from pathlib import Path
from .spec import load_spec


@dataclass
class QAResult:
    ok: bool
    score: int
    checks: list[str]
    errors: list[str]

    def to_dict(self) -> dict:
        return asdict(self)


def quality_score(project_dir: str | Path) -> QAResult:
    project = Path(project_dir)
    checks: list[str] = []
    errors: list[str] = []
    required = ["project.godot", "main.tscn", "main.gd", "game_spec.json", "marketing/store-copy.md"]
    for rel in required:
        if (project / rel).exists():
            checks.append(f"exists:{rel}")
        else:
            errors.append(f"missing:{rel}")
    try:
        spec = load_spec(project / "game_spec.json")
        if len(spec.hooks) >= 2:
            checks.append("concept:multiple-hooks")
        else:
            errors.append("concept:weak-hooks")
        if 0.35 <= float(spec.mechanics["spawn_interval"]) <= 2.5:
            checks.append("mechanics:spawn-range")
        else:
            errors.append("mechanics:spawn-outlier")
        if len(set(spec.palette.values())) >= 4:
            checks.append("visual:palette-contrast-intent")
        else:
            errors.append("visual:palette-low-variety")
    except Exception as exc:
        errors.append(f"spec:{exc}")
    score = max(0, min(100, 100 - len(errors) * 18))
    return QAResult(ok=not errors, score=score, checks=checks, errors=errors)


def run_headless(project_dir: str | Path, godot: str | None = None, frames: int = 120) -> tuple[bool, str]:
    executable = godot or shutil.which("godot") or shutil.which("godot4")
    if not executable:
        return False, "Godot executable not found; static QA completed only."
    cmd = [executable, "--headless", "--path", str(Path(project_dir).resolve()), "--quit-after", str(frames)]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    output = (proc.stdout + "\n" + proc.stderr).strip()
    return proc.returncode == 0, output[-5000:]


def write_qa_report(project_dir: str | Path) -> QAResult:
    result = quality_score(project_dir)
    p = Path(project_dir) / "qa-report.json"
    p.write_text(json.dumps(result.to_dict(), indent=2), encoding="utf-8")
    return result
