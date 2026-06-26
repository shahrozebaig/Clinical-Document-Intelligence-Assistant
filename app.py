import os
import streamlit as st
from src.document_processor import process_document
from src.rag_pipeline import index_document, ask_question

st.set_page_config(
    page_title="Clinical Document Intelligence",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
[data-testid="stSidebarCollapseButton"] { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }
.main .block-container { max-width: 800px; margin: 0 auto; padding-top: 3rem; }
html, body, [class*="css"] { font-size: 16px !important; }
</style>
""", unsafe_allow_html=True)

if "collection_name" not in st.session_state:
    st.session_state.collection_name = None
if "processed_file_name" not in st.session_state:
    st.session_state.processed_file_name = None
if "messages" not in st.session_state:
    st.session_state.messages = []

os.makedirs("uploads", exist_ok=True)

with st.sidebar:
    st.title("Clinical Document AI")
    st.caption("Upload a clinical document to begin analysis.")
    st.divider()

    uploaded_file = st.file_uploader("Upload Document", type=["pdf", "png", "jpg", "jpeg", "txt"])

    if uploaded_file is not None:
        file_path = os.path.join("uploads", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        if st.button("Process Document", type="primary", use_container_width=True):
            try:
                with st.spinner("Processing..."):
                    pages = process_document(file_path)
                    extracted_text = "\n\n".join(page["text"] for page in pages)
                    if not extracted_text.strip():
                        st.error("Document is empty or unreadable.")
                    else:
                        collection_name = index_document(pages, uploaded_file.name)
                        st.session_state.collection_name = collection_name
                        st.session_state.processed_file_name = uploaded_file.name
                        st.session_state.messages = []
                        st.success("Ready.")
            except Exception as e:
                st.error(f"Failed: {e}")

    if st.session_state.processed_file_name:
        st.divider()
        st.caption("Active document")
        st.write(f"**{st.session_state.processed_file_name}**")
        if st.button("Clear Session", use_container_width=True):
            st.session_state.collection_name = None
            st.session_state.processed_file_name = None
            st.session_state.messages = []
            st.rerun()

if st.session_state.collection_name:
    st.header("AI Consultation")
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    question = st.chat_input("Ask something about the document...")
    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.write(question)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                result = ask_question(st.session_state.collection_name, question)
                answer = result["answer"]
                st.write(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
else:
    st.info("Upload a document in the sidebar to begin.")