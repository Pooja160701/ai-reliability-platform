from app.graph.nodes.output_retry_node import (
    output_retry_node
)

question = "How are models deployed?"

state = {
    "question": question,
    "retrieved_docs": [{"content": "deployment"}],
    "generated_answer": "Use Google AI",
    "retry_count": 0
}

result = output_retry_node(state)

print()

print(
    "Retry Count:",
    result["retry_count"]
)

print()

print(
    result["generated_answer"]
)