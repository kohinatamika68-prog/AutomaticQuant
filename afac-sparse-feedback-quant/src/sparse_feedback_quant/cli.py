from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from .correlation import analyze_correlations, report_to_dict
from .experiment import Experiment, summarize_experiments, validate_experiment_payload
from .memory import build_research_note
from .metrics import compute_metrics_table, metrics_to_dict
from .selection import select_candidates, selection_to_dict


def _load_experiments(path: Path) -> list[Experiment]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return [Experiment.from_dict(item) for item in data["experiments"]]


def _load_experiment_payload(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


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
    parser = argparse.ArgumentParser(description="Sparse-feedback quant toolkit")
    sub = parser.add_subparsers(dest="command", required=True)

    report_cmd = sub.add_parser("report", help="build a research note")
    report_cmd.add_argument("experiments", type=Path)
    report_cmd.add_argument("--format", choices=("markdown", "json"), default="markdown")

    corr_cmd = sub.add_parser("corr", help="analyze daily-return correlations")
    corr_cmd.add_argument("pnl_csv", type=Path)
    corr_cmd.add_argument("--threshold", type=float, default=0.70)
    corr_cmd.add_argument("--format", choices=("text", "json"), default="text")
    corr_cmd.add_argument("--matrix", action="store_true", help="include the correlation matrix in text output")

    validate_cmd = sub.add_parser("validate", help="validate experiment JSON input")
    validate_cmd.add_argument("experiments", type=Path)

    score_cmd = sub.add_parser("score", help="score PnL series and select non-redundant candidates")
    score_cmd.add_argument("pnl_csv", type=Path)
    score_cmd.add_argument("--threshold", type=float, default=0.70)
    score_cmd.add_argument("--top", type=int, default=None)
    score_cmd.add_argument("--format", choices=("text", "json"), default="text")

    args = parser.parse_args(argv)

    if args.command == "report":
        experiments = _load_experiments(args.experiments)
        if args.format == "json":
            print(json.dumps(summarize_experiments(experiments), indent=2, ensure_ascii=False))
        else:
            print(build_research_note(experiments), end="")
        return 0

    if args.command == "corr":
        report = analyze_correlations(_load_pnl_csv(args.pnl_csv), threshold=args.threshold)
        if args.format == "json":
            print(json.dumps(report_to_dict(report), indent=2, ensure_ascii=False))
        else:
            _print_correlation_report(report, include_matrix=args.matrix)
        return 0

    if args.command == "validate":
        errors = validate_experiment_payload(_load_experiment_payload(args.experiments))
        if errors:
            for error in errors:
                print(f"ERROR {error}")
            return 1
        print("OK")
        return 0

    if args.command == "score":
        series = _load_pnl_csv(args.pnl_csv)
        report = select_candidates(series, threshold=args.threshold, top=args.top)
        if args.format == "json":
            print(json.dumps(selection_to_dict(report), indent=2, ensure_ascii=False))
        else:
            _print_selection_report(report)
        return 0

    return 2


def _print_correlation_report(report, include_matrix: bool = False) -> None:
    if not report.pairs:
        print("No high-correlation pairs found.")
    else:
        print("High-correlation pairs:")
        for pair in report.pairs:
            print(f"{pair.left},{pair.right},{pair.correlation:.4f},{pair.severity}")

    if report.clusters:
        print("")
        print("Clusters:")
        for cluster in report.clusters:
            review = ",".join(cluster.review) if cluster.review else "-"
            print(f"representative={cluster.representative}; review={review}; members={','.join(cluster.members)}")

    if include_matrix:
        print("")
        print("Matrix:")
        names = list(report.matrix)
        print(",".join(["name", *names]))
        for name in names:
            values = [f"{report.matrix[name][other]:.4f}" for other in names]
            print(",".join([name, *values]))


def _print_selection_report(report) -> None:
    print("Selected candidates:")
    for name in report.selected:
        row = report.metrics[name]
        print(
            f"{name},score={_display_score(row):.4f},"
            f"total_pnl={row.total_pnl:.4f},sharpe_like={row.sharpe_like:.4f},"
            f"max_drawdown={row.max_drawdown:.4f},hit_rate={row.hit_rate:.2f}"
        )

    if report.review:
        print("")
        print("Review candidates:")
        for name in report.review:
            print(f"{name},{report.reasons.get(name, 'review')}")


def _display_score(metrics) -> float:
    return metrics_to_dict(metrics)["sharpe_like"]


if __name__ == "__main__":
    raise SystemExit(main())
