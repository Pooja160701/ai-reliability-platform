from app.rag.generator import generate_answer


def generate_node(state):

    answer = generate_answer(
        state["question"],
        state["retrieved_docs"]
    )

    state["generated_answer"] = answer

    return state