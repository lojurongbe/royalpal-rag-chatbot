import os
from openai import OpenAI
import chromadb
from dotenv import load_dotenv

load_dotenv()

DB_FOLDER = "chroma_db"
COLLECTION_NAME = "royalpal_docs"
EMBEDDING_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4o-mini"
TOP_K = 3

# Maps raw filenames to clean, client-facing labels.
# Add a new line here any time you add a new source document.
FRIENDLY_SOURCE_NAMES = {
    "RoyalPal_Procedures_Guidelines.docx": "Service Procedures & Guidelines",
    "RoyalPal_Tax_Deadlines_QuickReference.docx": "Tax Deadlines Reference",
    "RoyalPal_New_Business_Registration_Checklist.docx": "Business Registration Guide",
}

def friendly_source_name(filename):
    """Look up a clean display name; fall back to a cleaned-up version of the filename
    if it's a new document that hasn't been added to the mapping yet."""
    if filename in FRIENDLY_SOURCE_NAMES:
        return FRIENDLY_SOURCE_NAMES[filename]
    name = filename.replace(".docx", "").replace("RoyalPal_", "")
    name = name.replace("_", " ").strip()
    return name.title()

client = OpenAI()
chroma_client = chromadb.PersistentClient(path=DB_FOLDER)
collection = chroma_client.get_collection(COLLECTION_NAME)

def get_embedding(text):
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )
    return response.data[0].embedding

def retrieve_chunks(question, top_k=TOP_K):
    question_embedding = get_embedding(question)
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=top_k
    )
    documents = results["documents"][0]
    sources = [friendly_source_name(meta["source"]) for meta in results["metadatas"][0]]
    return documents, sources

def build_prompt(question, chunks):
    context = "\n\n---\n\n".join(chunks)
    prompt = f"""You are a helpful assistant answering questions about Royal Pal Professional Services based only on the context provided below.

If the answer isn't in the context, say you don't have that information rather than guessing.

Context:
{context}

Question: {question}

Answer:"""
    return prompt

def ask(question):
    chunks, sources = retrieve_chunks(question)
    prompt = build_prompt(question, chunks)

    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    answer = response.choices[0].message.content
    return answer, sources

def main():
    print("Royal Pal Assistant — type 'quit' to exit\n")
    while True:
        question = input("Ask a question: ").strip()
        if question.lower() in ("quit", "exit"):
            break
        if not question:
            continue

        answer, sources = ask(question)
        print(f"\nAnswer: {answer}")
        print(f"\n(Based on: {', '.join(set(sources))})\n")

if __name__ == "__main__":
    main()
