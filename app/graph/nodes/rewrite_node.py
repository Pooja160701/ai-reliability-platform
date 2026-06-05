from app.rag.query_rewriter import rewrite_query


def rewrite_node(state):

    rewritten = rewrite_query(
        state["question"],
        state["critic_reason"]
    )

    state["rewritten_query"] = rewritten

    state["retry_count"] += 1

    return state