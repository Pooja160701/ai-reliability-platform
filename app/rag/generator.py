from openai import OpenAI

from app.config import (
    OPENAI_API_KEY,
    MODEL_NAME
)

client = OpenAI(
    api_key=OPENAI_API_KEY
)

def generate_answer(
    question: str,
    retrieved_docs: list
):

    context = "\n\n".join(
        [
            doc["content"]
            for doc in retrieved_docs
        ]
    )

    prompt = f"""
Answer the question using ONLY
the provided context.

If the answer is not present
in the context, say:

'I do not have enough information.'

Context:

{context}

Question:

{question}
"""

    response = client.responses.create(
        model=MODEL_NAME,
        input=prompt
    )

    return response.output_text