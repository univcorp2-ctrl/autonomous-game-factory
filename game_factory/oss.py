from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "config" / "oss_sources.json"


def clone_sources(names: list[str] | None = None, recommended: bool = False, dest_root: str | Path = "vendor/oss") -> dict:
    sources = json.loads(CATALOG.read_text(encoding="utf-8"))["sources"]
    if names:
        wanted = set(names)
        sources = [s for s in sources if s["name"] in wanted]
    elif recommended:
        sources = [s for s in sources if s.get("recommended")]
    root = Path(dest_root)
    root.mkdir(parents=True, exist_ok=True)
    lock = {"schema": 1, "sources": []}
    for src in sources:
        dest = root / src["name"]
        if not dest.exists():
            subprocess.run(["git", "clone", "--depth", "1", src["url"], str(dest)], check=True)
        commit = subprocess.check_output(["git", "-C", str(dest), "rev-parse", "HEAD"], text=True).strip()
        license_files = [p.name for p in dest.iterdir() if p.is_file() and p.name.lower().startswith("license")]
        if not license_files:
            raise RuntimeError(f"license file not found for {src['name']}; inspect before use")
        lock["sources"].append({**src, "commit": commit, "license_files": license_files})
    Path("vendor.lock.json").write_text(json.dumps(lock, indent=2), encoding="utf-8")
    return lock
