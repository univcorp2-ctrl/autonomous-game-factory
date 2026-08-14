from __future__ import annotations

import argparse
import json
import subprocess
import shutil
from pathlib import Path
from .autopilot import run_batch
from .feedback import learn_preferences
from .generator import generate_project
from .ideation import generate_ideas, load_preferences
from .oss import clone_sources
from .qa import quality_score, run_headless, write_qa_report
from .release import make_release_pack
from .spec import load_spec, save_spec


def main() -> None:
    p = argparse.ArgumentParser(prog="game-factory")
    sub = p.add_subparsers(dest="cmd", required=True)

    ideate = sub.add_parser("ideate")
    ideate.add_argument("--count", type=int, default=10)
    ideate.add_argument("--seed", type=int, default=1)
    ideate.add_argument("--preferences")
    ideate.add_argument("--out", default="ideas.json")

    make = sub.add_parser("make")
    make.add_argument("spec")
    make.add_argument("--out", default="generated")

    batch = sub.add_parser("batch")
    batch.add_argument("--count", type=int, default=12)
    batch.add_argument("--keep", type=int, default=3)
    batch.add_argument("--seed", type=int, default=1)
    batch.add_argument("--preferences")
    batch.add_argument("--out", default="generated")

    qa = sub.add_parser("qa")
    qa.add_argument("project")

    run = sub.add_parser("run")
    run.add_argument("project")
    run.add_argument("--godot")

    pack = sub.add_parser("pack")
    pack.add_argument("project")
    pack.add_argument("--itch-target")

    learn = sub.add_parser("learn")
    learn.add_argument("metrics_csv")
    learn.add_argument("--out", default="state/learned_preferences.json")

    vendor = sub.add_parser("vendor")
    vendor.add_argument("names", nargs="*")
    vendor.add_argument("--recommended", action="store_true")
    vendor.add_argument("--dest", default="vendor/oss")

    args = p.parse_args()
    if args.cmd == "ideate":
        weights = load_preferences(args.preferences)
        ideas = generate_ideas(args.count, args.seed, weights)
        Path(args.out).write_text(json.dumps([x.to_dict() for x in ideas], ensure_ascii=False, indent=2), encoding="utf-8")
        print(args.out)
    elif args.cmd == "make":
        print(generate_project(load_spec(args.spec), args.out))
    elif args.cmd == "batch":
        print(json.dumps(run_batch(args.count, args.keep, args.seed, args.out, args.preferences), indent=2))
    elif args.cmd == "qa":
        result = write_qa_report(args.project)
        print(json.dumps(result.to_dict(), indent=2))
        raise SystemExit(0 if result.ok else 2)
    elif args.cmd == "run":
        ok, output = run_headless(args.project, args.godot, frames=120)
        print(output)
        raise SystemExit(0 if ok else 2)
    elif args.cmd == "pack":
        print(make_release_pack(args.project, args.itch_target))
    elif args.cmd == "learn":
        print(json.dumps(learn_preferences(args.metrics_csv, args.out), indent=2))
    elif args.cmd == "vendor":
        print(json.dumps(clone_sources(args.names or None, args.recommended, args.dest), indent=2))


if __name__ == "__main__":
    main()
