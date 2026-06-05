from app.rag.retriever import retrieve
from app.rag.generator import generate_answer


question = (
    "How does AetherAI deploy models?"
)

docs = retrieve(
    question
)

answer = generate_answer(
    question,
    docs
)

print(answer)