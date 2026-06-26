import os
import uuid
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from src.llm_service import generate_text_response

embedding_function=SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

client=chromadb.PersistentClient(path="chroma_db")

def get_collection(collection_name):
    return client.get_or_create_collection(
        name=collection_name,
        embedding_function=embedding_function
    )

def split_text(text,chunk_size=700,overlap=120):
    chunks=[]
    start=0

    while start<len(text):
        end=start+chunk_size
        chunk=text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start=end-overlap

    return chunks

def create_collection_name(file_name):
    clean_name="".join(character.lower() if character.isalnum() else "_" for character in file_name)
    return f"clinical_{clean_name}_{uuid.uuid4().hex[:8]}"

def index_document(pages,file_name):
    collection_name=create_collection_name(file_name)
    collection=get_collection(collection_name)

    ids=[]
    documents=[]
    metadatas=[]

    for page in pages:
        page_number=page["page_number"]
        chunks=split_text(page["text"])

        for chunk_number,chunk in enumerate(chunks,start=1):
            ids.append(f"{file_name}_page_{page_number}_chunk_{chunk_number}_{uuid.uuid4().hex[:6]}")
            documents.append(chunk)
            metadatas.append({
                "file_name":file_name,
                "page_number":page_number,
                "chunk_number":chunk_number
            })

    if documents:
        collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )

    return collection_name

def ask_question(collection_name,question):
    collection=get_collection(collection_name)

    results=collection.query(
        query_texts=[question],
        n_results=4
    )

    documents=results.get("documents",[[]])[0]
    metadatas=results.get("metadatas",[[]])[0]

    if not documents:
        return {
            "answer":"No relevant information was found in the uploaded document.",
            "sources":[]
        }

    context_parts=[]

    for document,metadata in zip(documents,metadatas):
        context_parts.append(
            f"File: {metadata['file_name']}\n"
            f"Page: {metadata['page_number']}\n"
            f"Content: {document}"
        )

    context="\n\n".join(context_parts)

    prompt=f"""
You are a clinical document question-answering assistant.

Answer only from the provided document context.
Do not diagnose, infer, or add information not present in the context.
If the answer is not available, say:
"Not found in the uploaded document."

Document context:
{context}

Question:
{question}
"""

    messages=[
        {
            "role":"system",
            "content":"Answer only from retrieved clinical document context."
        },
        {
            "role":"user",
            "content":prompt
        }
    ]

    answer=generate_text_response(messages)

    sources=[]

    for document,metadata in zip(documents,metadatas):
        sources.append({
            "file_name":metadata["file_name"],
            "page_number":metadata["page_number"],
            "chunk_number":metadata["chunk_number"],
            "text":document
        })

    return {
        "answer":answer,
        "sources":sources
    }