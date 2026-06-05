from app.rag.retriever import retrieve


results = retrieve(
    "How does AetherAI deploy models?"
)

print()

for result in results:

    print(
        result["source"]
    )

    print(
        result["content"][:300]
    )

    print("-" * 50)