import json
import os
from openai import OpenAI
import chromadb
from dotenv import load_dotenv

load_dotenv()

CHUNKS_FILE = "chunks.json"
DB_FOLDER = "chroma_db"
COLLECTION_NAME = "royalpal_docs"
EMBEDDING_MODEL = "text-embedding-3-small"

client = OpenAI()

def get_embedding(text):
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )
    return response.data[0].embedding

def main():
    with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    print(f"Loaded {len(chunks)} chunks from {CHUNKS_FILE}")

    chroma_client = chromadb.PersistentClient(path=DB_FOLDER)

    try:
        chroma_client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = chroma_client.create_collection(COLLECTION_NAME)

    for i, chunk in enumerate(chunks):
        print(f"Embedding chunk {i + 1}/{len(chunks)} from {chunk['source']}...")
        embedding = get_embedding(chunk["text"])

        collection.add(
            ids=[f"chunk_{i}"],
            embeddings=[embedding],
            documents=[chunk["text"]],
            metadatas=[{"source": chunk["source"]}]
        )

    print(f"\nDone. {len(chunks)} chunks embedded and stored in '{DB_FOLDER}'")

if __name__ == "__main__":
    main()