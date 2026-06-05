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

Return ONLY valid JSON:

{{
    "decision": "approve" or "reject",
    "reason": "short explanation"
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

    return response.output_text