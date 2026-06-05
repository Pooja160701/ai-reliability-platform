from openai import OpenAI

from app.config import (
    OPENAI_API_KEY,
    MODEL_NAME
)

client = OpenAI(
    api_key=OPENAI_API_KEY
)


def rewrite_query(
    original_question: str,
    critic_reason: str
):

    prompt = f"""
You are a retrieval optimization agent.

Original Question:
{original_question}

Critic Feedback:
{critic_reason}

Rewrite the question so that a vector search
system can retrieve better supporting documents.

Return only the rewritten query.
"""

    response = client.responses.create(
        model=MODEL_NAME,
        input=prompt
    )

    return response.output_text.strip()