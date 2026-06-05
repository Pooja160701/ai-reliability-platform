from pathlib import Path
import json

from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential

from app.config import OPENAI_API_KEY, MODEL_NAME


client = OpenAI(
    api_key=OPENAI_API_KEY
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DOCUMENTS_DIR = PROJECT_ROOT / "data" / "documents"

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "golden_dataset"
    / "golden_dataset.json"
)


SYSTEM_PROMPT = """
You are an enterprise QA engineer.

Generate evaluation examples from internal company documents.

For each document create exactly 2 question-answer pairs.

Requirements:

- Questions must be realistic.
- Answers must be grounded in the document.
- Questions should test retrieval quality.
- Include at least one edge-case question when possible.
- Return valid JSON only.

Format:

[
  {
    "question": "...",
    "expected_answer": "..."
  }
]
"""


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=2)
)
def generate_qa_pairs(content: str):

    response = client.responses.create(
        model=MODEL_NAME,
        input=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": content[:12000]
            }
        ]
    )

    return response.output_text


def main():

    dataset = []

    current_id = 1

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    files = list(
        DOCUMENTS_DIR.rglob("*.txt")
    )

    total_files = len(files)

    print(
        f"Found {total_files} documents"
    )

    for file in files:

        print(
            f"Processing {file.name}"
        )

        content = file.read_text(
            encoding="utf-8"
        )

        try:

            output = generate_qa_pairs(
                content
            )

            qa_pairs = json.loads(
                output
            )

            for qa in qa_pairs:

                dataset.append(
                    {
                        "id": current_id,
                        "question":
                            qa["question"],
                        "expected_answer":
                            qa["expected_answer"],
                        "source_document":
                            file.stem
                    }
                )

                current_id += 1

        except Exception as error:

            print(
                f"Failed: {file.name}"
            )

            print(error)


    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            dataset,
            file,
            indent=2
        )

    print()

    print(
        f"Generated {len(dataset)} QA pairs"
    )


if __name__ == "__main__":
    main()