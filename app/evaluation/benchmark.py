from pathlib import Path
import json
import time

from app.graph.workflow import graph

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

DATASET_FILE = (
    PROJECT_ROOT
    / "data"
    / "golden_dataset"
    / "golden_dataset.json"
)

RESULTS_FILE = (
    PROJECT_ROOT
    / "data"
    / "evaluation"
    / "benchmark_results.json"
)

def load_dataset():

    with open(
        DATASET_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)
    
def run_question(example):

    start = time.time()

    result = graph.invoke(
        {
            "question":
                example["question"],

            "retrieved_docs": [],

            "generated_answer": "",

            "critic_decision": "",

            "critic_reason": "",

            "rewritten_query": "",

            "retry_count": 0,

            "final_response": "",

            "input_validation_passed": True,

            "output_validation_passed": True
        }
    )

    latency = (
        time.time() - start
    )

    return {
        "id":
            example["id"],

        "question":
            example["question"],

        "expected_answer":
            example["expected_answer"],

        "generated_answer":
            result["final_response"],

        "latency":
            latency
    }

def main():

    dataset = load_dataset()

    dataset = dataset[:5]
    
    results = []

    total = len(dataset)

    print(
        f"Running {total} evaluations"
    )

    for index, example in enumerate(
        dataset,
        start=1
    ):

        print(
            f"{index}/{total}"
        )

        results.append(
            run_question(example)
        )

    RESULTS_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        RESULTS_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            results,
            file,
            indent=2
        )

    print()

    print(
        f"Saved {len(results)} results"
    )

if __name__ == "__main__":
    main()