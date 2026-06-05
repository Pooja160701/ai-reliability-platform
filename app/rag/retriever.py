from pathlib import Path
import json
import faiss
import numpy as np
from openai import OpenAI
from app.config import OPENAI_API_KEY

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

VECTOR_DIR = PROJECT_ROOT / "data" / "vectors"

client = OpenAI(
    api_key=OPENAI_API_KEY
)

index = faiss.read_index(
    str(
        VECTOR_DIR / "faiss.index"
    )
)

with open(
    VECTOR_DIR / "metadata.json",
    "r",
    encoding="utf-8"
) as f:

    metadata = json.load(f)

def embed_query(
    query: str
):

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    )

    return response.data[0].embedding

def retrieve(
    query: str,
    k: int = 5
):

    query_vector = np.array(
        [embed_query(query)],
        dtype="float32"
    )

    distances, indices = index.search(
        query_vector,
        k
    )

    results = []

    for idx in indices[0]:

        results.append(
            metadata[idx]
        )

    return results