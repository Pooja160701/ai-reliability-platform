from app.rag.retriever import retrieve
from app.graph.nodes.output_retry_node import (
    output_retry_node
)

question = "How does AetherAI deploy models?"

docs = retrieve(question)

state = {
    "question": question,
    "retrieved_docs": docs,
    "generated_answer": "Use Google Vertex AI",
    "retry_count": 0
}

result = output_retry_node(state)

print()
print("Retry Count:", result["retry_count"])
print()
print(result["generated_answer"])