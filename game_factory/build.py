from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

TARGETS = {
    "windows": ("Windows Desktop", "build/windows/game.exe"),
    "linux": ("Linux", "build/linux/game.x86_64"),
    "web": ("Web", "build/web/index.html"),
}


def build_project(project_dir: str | Path, targets: list[str], godot: str | None = None, dry_run: bool = False) -> list[list[str]]:
    executable = godot or shutil.which("godot") or shutil.which("godot4")
    if not executable and not dry_run:
        raise RuntimeError("Godot executable not found")
    executable = executable or "godot"
    project = Path(project_dir).resolve()
    commands: list[list[str]] = []
    for target in targets:
        if target not in TARGETS:
            raise ValueError(f"unsupported build target: {target}")
        preset, rel = TARGETS[target]
        out = project / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        cmd = [executable, "--headless", "--path", str(project), "--export-release", preset, str(out)]
        commands.append(cmd)
        if not dry_run:
            subprocess.run(cmd, check=True, timeout=300)
    return commands
