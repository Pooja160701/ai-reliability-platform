from app.rag.critic import evaluate_answer


def critic_node(state):

    result = evaluate_answer(
        state["question"],
        state["generated_answer"],
        state["retrieved_docs"]
    )

    state["critic_decision"] = (
        result["decision"]
    )

    state["critic_reason"] = (
        result["reason"]
    )

    return state