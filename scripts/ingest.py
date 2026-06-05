from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
import json
from openai import OpenAI
import faiss
import numpy as np
from app.config import OPENAI_API_KEY

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DOCUMENTS_DIR = PROJECT_ROOT / "data" / "documents"

CHUNK_DIR = PROJECT_ROOT / "data" / "chunks"

VECTOR_DIR = PROJECT_ROOT / "data" / "vectors"

client = OpenAI(
    api_key=OPENAI_API_KEY
)

def load_documents():

    docs = []

    for file in DOCUMENTS_DIR.rglob("*.txt"):

        with open(
            file,
            "r",
            encoding="utf-8"
        ) as f:

            text = f.read()

        docs.append(
            {
                "source": str(file),
                "content": text
            }
        )

    return docs


def chunk_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = []

    for doc in documents:

        split_chunks = splitter.split_text(
            doc["content"]
        )

        for chunk in split_chunks:

            chunks.append(
                {
                    "source": doc["source"],
                    "content": chunk
                }
            )

    return chunks


def save_chunks(chunks):

    CHUNK_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    output_file = CHUNK_DIR / "chunks.json"

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            chunks,
            f,
            indent=2
        )


def get_embedding(text: str):

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )

    return response.data[0].embedding


def create_embeddings(chunks):

    embeddings = []

    for i, chunk in enumerate(chunks):

        print(
            f"Embedding {i+1}/{len(chunks)}"
        )

        vector = get_embedding(
            chunk["content"]
        )

        embeddings.append(vector)

    return embeddings

def build_faiss_index(
    chunks,
    embeddings
):

    VECTOR_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    vectors = np.array(
        embeddings,
        dtype="float32"
    )

    dimension = len(
        embeddings[0]
    )

    index = faiss.IndexFlatL2(
        dimension
    )

    index.add(vectors)

    faiss.write_index(
        index,
        str(
            VECTOR_DIR / "faiss.index"
        )
    )

    print(
        f"Saved FAISS index with {index.ntotal} vectors"
    )


def save_metadata(
    chunks
):

    metadata_file = (
        VECTOR_DIR /
        "metadata.json"
    )

    with open(
        metadata_file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            chunks,
            f,
            indent=2
        )

  
def main():

    docs = load_documents()

    print(
        f"Loaded {len(docs)} documents"
    )

    chunks = chunk_documents(
        docs
    )

    print(
        f"Created {len(chunks)} chunks"
    )

    save_chunks(chunks)

    print(
        "Chunks saved"
    )

    embeddings = create_embeddings(
        chunks
    )

    build_faiss_index(
        chunks,
        embeddings
    )

    save_metadata(
        chunks
    )


if __name__ == "__main__":
    main()