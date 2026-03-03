import os
from typing import List, TypedDict

import requests
import streamlit as st


class Msg(TypedDict):
    role: str
    content: str


API_BASE = os.getenv("THESISFLOW_API_BASE_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="ThesisFlow MARA", page_icon="📚", layout="wide")

if "messages" not in st.session_state:
    st.session_state.messages: List[Msg] = []

st.title("ThesisFlow MARA")
st.caption("Memory-Augmented Research Agent")

with st.sidebar:
    st.subheader("Backend")
    st.code(API_BASE)
    if st.button("Check Health", use_container_width=True):
        try:
            r = requests.get(f"{API_BASE}/health", timeout=8)
            r.raise_for_status()
            st.success("Backend reachable")
            st.json(r.json())
        except Exception as exc:
            st.error(f"Health check failed: {exc}")

    st.divider()
    st.subheader("Paper Ingestion")
    pdf_file = st.file_uploader("Upload PDF", type=["pdf"])
    if st.button("Upload and Index", use_container_width=True, disabled=pdf_file is None):
        if pdf_file is not None:
            files = {"file": (pdf_file.name, pdf_file.getvalue(), "application/pdf")}
            try:
                with st.spinner("Uploading and indexing..."):
                    r = requests.post(f"{API_BASE}/upload-pdf", files=files, timeout=120)
                if r.ok:
                    data = r.json()
                    st.success(f"Indexed {data.get('chunks_stored', 0)} chunks")
                else:
                    detail = r.text
                    try:
                        detail = r.json().get("detail", detail)
                    except Exception:
                        pass
                    st.error(f"Upload failed: {detail}")
            except Exception as exc:
                st.error(f"Upload failed: {exc}")

    st.divider()
    if st.button("Clear Memory", use_container_width=True):
        try:
            r = requests.delete(f"{API_BASE}/memory", timeout=10)
            r.raise_for_status()
            st.success(f"Deleted {r.json().get('deleted', 0)} memories")
        except Exception as exc:
            st.error(f"Could not clear memory: {exc}")

st.subheader("Chat")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ask about findings, methods, or evidence gaps...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_text = ""
        try:
            payload = {"message": prompt, "use_memory": True, "use_rag": True}
            with requests.post(
                f"{API_BASE}/chat-stream",
                json=payload,
                stream=True,
                timeout=180,
            ) as r:
                if not r.ok:
                    detail = r.text
                    try:
                        detail = r.json().get("detail", detail)
                    except Exception:
                        pass
                    raise RuntimeError(detail)

                for chunk in r.iter_content(chunk_size=None):
                    if not chunk:
                        continue
                    full_text += chunk.decode("utf-8", errors="ignore")
                    placeholder.markdown(full_text)

            st.session_state.messages.append({"role": "assistant", "content": full_text})
        except Exception as exc:
            err = f"Request failed: {exc}"
            placeholder.error(err)
            st.session_state.messages.append({"role": "assistant", "content": err})
