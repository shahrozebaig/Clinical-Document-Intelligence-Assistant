# Clinical Document Intelligence Assistant

## Overview

Clinical Document Intelligence Assistant is an AI-powered application that helps users understand healthcare documents more easily. Users can upload a clinical document, ask questions in simple language, and receive answers based only on the uploaded document.

The application supports both digital and scanned documents. If a scanned document is uploaded, OCR is used to extract the text before processing. The extracted information is indexed using Retrieval-Augmented Generation (RAG), allowing the system to retrieve relevant information before generating answers.

This project was developed as a Proof of Concept (POC) for the topic **Clinical Natural Language Technology for Healthcare**.

---

# Features

* Upload PDF documents
* Upload image documents (PNG, JPG, JPEG)
* Upload TXT documents
* OCR support for scanned documents
* AI-powered chatbot
* Retrieval-Augmented Generation (RAG)
* ChromaDB vector database
* Answers generated only from the uploaded document
* Simple and easy-to-use Streamlit interface

---

# How It Works

1. Upload a clinical document.
2. The application reads the uploaded file.
3. If the document is scanned, OCR extracts the text.
4. The document is divided into smaller chunks.
5. Embeddings are created for each chunk.
6. The embeddings are stored in ChromaDB.
7. When the user asks a question, RAG retrieves the most relevant document content.
8. The Groq Large Language Model generates the final answer based only on the uploaded document.

---

# Future Improvements

* Support additional document formats
* Multi-document search
* Document comparison
* User authentication
* Cloud deployment
* Better OCR for low-quality scans