\# Royal Pal Assistant — RAG Chatbot



A Retrieval-Augmented Generation (RAG) chatbot that answers questions about Royal Pal Professional Services (a chartered accounting and tax consultancy) using only its own service documents as source material.



\## What it does

Answers questions about services, tax deadlines, and business registration procedures by retrieving relevant passages from internal documents and using an LLM to generate grounded, accurate answers — rather than relying on general knowledge, which reduces hallucination risk.



\## Architecture

1\. Source documents (.docx) are read and split into overlapping text chunks

2\. Each chunk is converted into a vector embedding (OpenAI `text-embedding-3-small`) and stored in a local ChromaDB vector database

3\. At query time, the user's question is embedded and compared against stored chunks to retrieve the most relevant ones

4\. Retrieved chunks are passed as context to an LLM (`gpt-4o-mini`), which generates an answer grounded only in that context

5\. A Streamlit interface wraps the pipeline in a simple chat UI



\## Tech stack

Python · OpenAI API (embeddings + chat) · ChromaDB · Streamlit · python-docx



\## Running it locally

git clone https://github.com/lojurongbe/royalpal-rag-chatbot.git
cd royalpal-rag-chatbot
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

Add your OpenAI API key to a `.env` file:

OPENAI_API_KEY=your-key-here


Then build the vector store and launch the app:

python chunk_documents.py
python build_vectorstore.py
streamlit run app.py


## A real limitation I hit
"Short, vague questions sometimes retrieve the wrong document because chunk size (400 words) is too coarse for very specific queries. Tuning chunk size to 200-250 words improved precision but slightly increased the number of API calls."

## Why RAG instead of fine-tuning
RAG was the right fit here because the source documents change over time (fees, deadlines, procedures) — fine-tuning would require retraining every time content changes, while RAG just needs the new document re-embedded.



