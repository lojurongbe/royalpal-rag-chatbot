import os
import sys
import streamlit as st

st.set_page_config(page_title="Royal Pal Assistant", page_icon="💼")

if "OPENAI_API_KEY" in st.secrets:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

if not os.path.exists("chroma_db"):
    with st.spinner("Setting up knowledge base for the first time — this takes about a minute..."):
        import subprocess
        subprocess.run([sys.executable, "chunk_documents.py"], check=True)
        subprocess.run([sys.executable, "build_vectorstore.py"], check=True)

from ask import ask

st.title("Royal Pal Professional Services — Assistant")
st.caption("Ask a question about services, tax deadlines, or registration procedures.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input("Ask a question...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer, sources = ask(question)
            full_response = f"{answer}\n\n*Sources: {', '.join(set(sources))}*"
            st.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
