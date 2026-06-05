from app.graph.workflow import graph


state = {
    "question":
        "How does AetherAI deploy models?",

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


result = graph.invoke(
    state
)

print()

print(
    result["final_response"]
)

print()

print(
    "Decision:",
    result["critic_decision"]
)

print()

print(
    "Retries:",
    result["retry_count"]
)