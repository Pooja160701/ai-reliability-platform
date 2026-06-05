from app.rag.retriever import retrieve
from app.rag.generator import generate_answer
from app.rag.critic import evaluate_answer


question = (
    "How does AetherAI deploy models?"
)

docs = retrieve(question)

answer = """
AetherAI deploys all models
using Google Vertex AI
across five regions.
"""

decision = evaluate_answer(
    question,
    answer,
    docs
)

print(answer)
print()
print(decision)