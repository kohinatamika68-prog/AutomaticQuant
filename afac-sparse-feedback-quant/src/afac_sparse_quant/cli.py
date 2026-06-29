from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from .correlation import high_correlation_pairs
from .experiment import Experiment
from .memory import build_research_note


def _load_experiments(path: Path) -> list[Experiment]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return [Experiment.from_dict(item) for item in data["experiments"]]


def _load_pnl_csv(path: Path) -> dict[str, list[float]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames or len(reader.fieldnames) < 2:
            raise ValueError("PnL CSV must contain a date column and at least one strategy column")
        strategy_names = reader.fieldnames[1:]
        series = {name: [] for name in strategy_names}
        for row in reader:
            for name in strategy_names:
                series[name].append(float(row[name]))
    return series


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="AFAC sparse-feedback quant toolkit")
    sub = parser.add_subparsers(dest="command", required=True)

    report_cmd = sub.add_parser("report", help="build a sanitized research note")
    report_cmd.add_argument("experiments", type=Path)

    corr_cmd = sub.add_parser("corr", help="find high daily-return correlations")
    corr_cmd.add_argument("pnl_csv", type=Path)
    corr_cmd.add_argument("--threshold", type=float, default=0.70)

    args = parser.parse_args(argv)

    if args.command == "report":
        print(build_research_note(_load_experiments(args.experiments)), end="")
        return 0

    if args.command == "corr":
        pairs = high_correlation_pairs(_load_pnl_csv(args.pnl_csv), threshold=args.threshold)
        if not pairs:
            print("No high-correlation pairs found.")
            return 0
        for pair in pairs:
            print(f"{pair.left},{pair.right},{pair.correlation:.4f}")
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
