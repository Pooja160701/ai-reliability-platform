from app.rag.query_rewriter import rewrite_query

question = (
    "How does AetherAI deploy models?"
)

reason = (
    "Retrieved context does not contain enough deployment details."
)

query = rewrite_query(
    question,
    reason
)

print(query)