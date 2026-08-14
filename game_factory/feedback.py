from __future__ import annotations

import csv
import json
import math
from collections import defaultdict
from pathlib import Path


def _row_score(row: dict[str, str]) -> float:
    wishlists = float(row.get("wishlists", 0) or 0)
    conversion = float(row.get("conversion_rate", 0) or 0)
    positive = float(row.get("positive_review_rate", 0) or 0)
    playtime = float(row.get("median_playtime_minutes", 0) or 0)
    refunds = float(row.get("refund_rate", 0) or 0)
    return (
        math.log1p(wishlists) * 0.25
        + conversion * 4.0
        + positive * 2.5
        + min(playtime, 180.0) / 180.0
        - refunds * 3.0
    )


def learn_preferences(metrics_csv: str | Path, out_path: str | Path) -> dict:
    totals: dict[str, list[float]] = defaultdict(list)
    with Path(metrics_csv).open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            mode = row.get("mode", "").strip()
            if mode:
                totals[mode].append(_row_score(row))
    averages = {mode: sum(vals) / len(vals) for mode, vals in totals.items() if vals}
    floor = min(averages.values(), default=0.0)
    weights = {mode: max(0.2, score - floor + 0.5) for mode, score in averages.items()}
    for mode in ["survivor", "dodger", "collector"]:
        weights.setdefault(mode, 1.0)
    result = {"schema": 1, "mode_weights": weights, "raw_mode_scores": averages}
    p = Path(out_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result
