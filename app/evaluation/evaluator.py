# app/evaluation/evaluator.py

import json
from pathlib import Path
from datetime import datetime

from app.evaluation.metrics import (
    calculate_accuracy,
    calculate_groundedness,
    calculate_approval_rate,
    calculate_failure_rate,
    calculate_average_retries
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

RESULTS_FILE = (
    PROJECT_ROOT
    / "data"
    / "evaluation"
    / "benchmark_results.json"
)

REPORT_FILE = (
    PROJECT_ROOT
    / "data"
    / "evaluation"
    / "evaluation_report.json"
)

def load_results():

    with open(
        RESULTS_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)

def build_report(results):

    accuracy = calculate_accuracy(results)

    report = {

        "run_timestamp":
            datetime.utcnow().isoformat(),

        "samples":
            len(results),

        "accuracy":
            accuracy,

        "groundedness":
            calculate_groundedness(results),

        "approval_rate":
            calculate_approval_rate(results),

        "failure_rate":
            calculate_failure_rate(results),

        "average_retries":
            calculate_average_retries(results),

        "status":
            "PASS"
            if accuracy >= 0.80
            else "FAIL"
    }

    return report

def save_report(report):

    REPORT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        REPORT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            report,
            file,
            indent=2
        )

def main():

    results = load_results()

    report = build_report(
        results
    )

    save_report(
        report
    )

    print()

    print(
        json.dumps(
            report,
            indent=2
        )
    )


if __name__ == "__main__":
    main()