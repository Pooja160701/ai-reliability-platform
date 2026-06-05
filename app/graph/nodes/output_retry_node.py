from app.rag.generator import generate_answer


def output_retry_node(state):

    state["retry_count"] += 1

    corrected_question = f"""
Answer strictly from the provided context.

Question:
{state['question']}
"""

    state["generated_answer"] = generate_answer(
        corrected_question,
        state["retrieved_docs"]
    )

    return state