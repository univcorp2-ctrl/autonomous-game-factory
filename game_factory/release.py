from __future__ import annotations

import json
from pathlib import Path
from .spec import load_spec


def make_release_pack(project_dir: str | Path, itch_target: str | None = None) -> Path:
    project = Path(project_dir)
    spec = load_spec(project / "game_spec.json")
    out = project / "release"
    out.mkdir(exist_ok=True)
    target = itch_target or f"YOUR_ITCH_USER/{spec.slug}"
    (out / "itch-push.sh").write_text(
        f"#!/usr/bin/env sh\nset -eu\n: \"${{BUTLER:=butler}}\"\n$BUTLER push build/windows {target}:windows\n$BUTLER push build/linux {target}:linux\n$BUTLER push build/web {target}:html5\n",
        encoding="utf-8",
    )
    (out / "itch-push.ps1").write_text(
        f"$Butler = if ($env:BUTLER) {{ $env:BUTLER }} else {{ 'butler' }}\n& $Butler push build/windows '{target}:windows'\n& $Butler push build/linux '{target}:linux'\n& $Butler push build/web '{target}:html5'\n",
        encoding="utf-8",
    )
    steam_manifest = {
        "app_id": "SET_IN_STEAMWORKS",
        "depot_id": "SET_IN_STEAMWORKS",
        "build_output": "release/steam-output",
        "content_root": "build/windows",
        "notes": "Generate the final SteamPipe VDF only after App ID / Depot ID exist. Store review and release remain explicit gates.",
    }
    (out / "steam-manifest.json").write_text(json.dumps(steam_manifest, indent=2), encoding="utf-8")
    (out / "RELEASE-GATES.md").write_text(
        """# Release gates\n\n- [ ] QA score meets internal threshold\n- [ ] Third-party code/assets license audit complete\n- [ ] Store copy reviewed for factual claims\n- [ ] Price and regional pricing approved by account owner\n- [ ] Steam App ID / Depot ID configured when applicable\n- [ ] Platform content survey and age-rating inputs completed by responsible publisher\n- [ ] Store review passed\n- [ ] Final release action performed by authorized account owner\n""",
        encoding="utf-8",
    )
    return out
