from pathlib import Path
import json

MIN_ACCURACY = 0.80
MIN_GROUNDEDNESS = 0.80
MAX_FAILURE_RATE = 0.20

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

REPORT_FILE = (
    PROJECT_ROOT
    / "data"
    / "evaluation"
    / "evaluation_report.json"
)

def main():

    with open(
        REPORT_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        report = json.load(file)

    accuracy = report["accuracy"]
    groundedness = report["groundedness"]
    failure_rate = report["failure_rate"]

    result = {
        "status": "PASS",
        "merge_allowed": True
    }

    if accuracy < MIN_ACCURACY:

        result = {
            "status": "FAIL",
            "merge_allowed": False,
            "reason": "Accuracy below threshold"
        }

    elif groundedness < MIN_GROUNDEDNESS:

        result = {
            "status": "FAIL",
            "merge_allowed": False,
            "reason": "Groundedness below threshold"
        }

    elif failure_rate > MAX_FAILURE_RATE:

        result = {
            "status": "FAIL",
            "merge_allowed": False,
            "reason": "Failure rate above threshold"
        }

    print(
        json.dumps(
            result,
            indent=2
        )
    )

    if not result["merge_allowed"]:
        raise SystemExit(1)

if __name__ == "__main__":
    main()