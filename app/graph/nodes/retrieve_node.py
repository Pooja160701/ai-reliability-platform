from app.rag.retriever import retrieve


def retrieve_node(state):

    query = (
        state["rewritten_query"]
        if state["rewritten_query"]
        else state["question"]
    )

    docs = retrieve(query)

    state["retrieved_docs"] = docs

    return state