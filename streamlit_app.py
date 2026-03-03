import os
from typing import List, TypedDict

import requests
import streamlit as st


class Msg(TypedDict):
    role: str
    content: str


API_BASE = os.getenv("THESISFLOW_API_BASE_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="ThesisFlow", page_icon="📚", layout="wide")

if "messages" not in st.session_state:
    st.session_state.messages: List[Msg] = []

st.markdown(
    """
    <style>
      .stApp {
        background: #000000;
        color: #f5f5f5;
      }
      .block-container {
        max-width: 900px;
        padding-top: 2rem;
        padding-bottom: 1.5rem;
      }
      .stMarkdown, .stMarkdown p, .stMarkdown span, .stMarkdown li, .stMarkdown div {
        color: #f5f5f5 !important;
      }
      [data-testid="stChatMessageContent"], [data-testid="stChatMessageContent"] * {
        color: #f5f5f5 !important;
      }
      .tf-title {
        font-size: 2.3rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 0;
      }
      .tf-subtitle {
        font-size: 0.92rem;
        color: #b7b7c0;
        margin-top: 0.2rem;
        margin-bottom: 1rem;
      }
      .tf-chat-wrap {
        background: #0d0d0f;
        border: 1px solid #24242b;
        border-radius: 16px;
        padding: 0.75rem 0.75rem 0.25rem 0.75rem;
        box-shadow: 0 10px 28px rgba(0, 0, 0, 0.55);
      }
      .tf-composer {
        margin-top: 0.7rem;
        border-top: 1px solid #24242b;
        padding-top: 0.7rem;
      }
      [data-testid="stChatMessage"] {
        background: #141419;
        border: 1px solid #23232b;
        border-radius: 12px;
        padding: 0.4rem 0.55rem;
      }
      [data-testid="stChatInput"] textarea, [data-testid="stChatInput"] input {
        background: #121217 !important;
        color: #f5f5f5 !important;
        border: 1px solid #2a2a34 !important;
      }
      [data-testid="stFileUploader"] section {
        background: #121217 !important;
        border: 1px dashed #2a2a34 !important;
      }
      .stButton>button {
        border-radius: 10px !important;
        border: 1px solid #2a2a34 !important;
        background: #1f6feb !important;
        color: #ffffff !important;
        font-weight: 600 !important;
      }
      .stAlert {
        background: #0f0f14 !important;
        color: #f5f5f5 !important;
        border: 1px solid #2a2a34 !important;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="tf-title">ThesisFlow</div>', unsafe_allow_html=True)
st.markdown('<div class="tf-subtitle">Memory-Augmented Research Agent</div>', unsafe_allow_html=True)

header_left, header_right = st.columns([4, 1])
with header_right:
    if st.button("Clear Memory", use_container_width=True):
        try:
            r = requests.delete(f"{API_BASE}/memory", timeout=10)
            r.raise_for_status()
            st.success(f"Deleted {r.json().get('deleted', 0)} memories")
        except Exception as exc:
            st.error(f"Could not clear memory: {exc}")

st.markdown('<div class="tf-chat-wrap">', unsafe_allow_html=True)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

st.markdown('<div class="tf-composer">', unsafe_allow_html=True)
u_col, b_col = st.columns([5, 1])
with u_col:
    pdf_file = st.file_uploader(
        "Attach PDF",
        type=["pdf"],
        label_visibility="collapsed",
        key="composer_pdf",
    )
with b_col:
    upload_clicked = st.button("Upload", use_container_width=True)

if upload_clicked:
    if pdf_file is None:
        st.warning("Select a PDF first.")
    else:
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

prompt = st.chat_input("Message ThesisFlow...")
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

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
