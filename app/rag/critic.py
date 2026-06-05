import json

from openai import OpenAI

from app.config import (
    OPENAI_API_KEY,
    MODEL_NAME
)

client = OpenAI(
    api_key=OPENAI_API_KEY
)


def evaluate_answer(
    question: str,
    answer: str,
    retrieved_docs: list
):

    context = "\n\n".join(
        [
            doc["content"]
            for doc in retrieved_docs
        ]
    )

    prompt = f"""
You are a strict RAG evaluator.

Your job is to determine whether
the answer is grounded in the context.

Question:
{question}

Retrieved Context:
{context}

Generated Answer:
{answer}

Return ONLY valid JSON.

Example:

{{
    "decision": "approve",
    "reason": "Answer is supported by context"
}}

Rules:

Approve only if the answer is
supported by the retrieved context.

Reject if:
- information is invented
- unsupported claims exist
- answer goes beyond context
"""

    response = client.responses.create(
        model=MODEL_NAME,
        input=prompt
    )

    raw = response.output_text.strip()

    raw = raw.replace(
        "```json",
        ""
    )

    raw = raw.replace(
        "```",
        ""
    )

    raw = raw.strip()

    try:
        return json.loads(raw)

    except Exception:

        print("\nCRITIC RAW RESPONSE:")
        print(raw)

        return {
            "decision": "reject",
            "reason": "Critic returned invalid JSON"
        }