# Chat with PDF - Agentic RAG System

An AI-powered PDF Question Answering application built using FastAPI, React, LangChain, FAISS, Hugging Face Embeddings, and Groq Llama 3.1.

The application allows users to upload one or more PDF documents and ask natural language questions. The system uses an Agentic Retrieval-Augmented Generation (RAG) pipeline with query rewriting, retrieval, reranking, planning, and answer generation to provide accurate responses based on the uploaded documents.

---

# Features

* Multi-PDF Upload Support
* Automatic PDF Parsing and Chunking
* Vector Embeddings using BAAI/bge-small-en-v1.5
* FAISS Vector Database
* Query Rewriting Agent
* Retriever Agent
* Reranker Agent
* Planner Agent
* Generator Agent
* Conversation History Support
* Agentic RAG Workflow
* FastAPI Backend
* React Frontend
* Groq Llama 3.1 Integration

---

# Architecture

```text
User Question
      │
      ▼
Query Rewriter Agent
      │
      ▼
Retriever Agent
      │
      ▼
Reranker Agent
      │
      ▼
Planner Agent
      │
      ├── RETRIEVE_MORE
      ├── REQUERY
      └── GENERATE
      │
      ▼
Generator Agent
      │
      ▼
Final Answer
```

---

# Project Structure

```text
chat_with_pdf/
│
├── backend/
│   ├── agents/
│   │   ├── generator.py
│   │   ├── planner.py
│   │   ├── query_writer.py
│   │   ├── reranker.py
│   │   └── retriever.py
│   │
│   ├── services/
│   │   ├── ingestion.py
│   │   └── vectorstore.py
│   │
│   |
│   ├── app.py
│   ├── requirements.txt
│   └── .env
│
├── client/
│   ├── src/
│   │   ├── App.js
│   │   ├── App.css
│   │   └── index.js
│   │
│   ├── package.json
│   └── public/
│
└── README.md
```

---

# Tech Stack

## Frontend

* React
* JavaScript
* CSS
* Fetch API

## Backend

* FastAPI
* Python
* LangChain

## AI & RAG

* Groq Llama 3.1 8B Instant
* Hugging Face Embeddings
* BAAI/bge-small-en-v1.5
* FAISS
* Agentic RAG Pipeline

---

# Agent Workflow

## 1. Query Rewriter

Converts user questions into optimized search queries while preserving intent.

Example:

```text
User:
what is reinforcement learning

Rewritten:
What is reinforcement learning?
```

---

## 2. Retriever

Retrieves relevant chunks from the FAISS vector database.

---

## 3. Reranker

Ranks retrieved chunks according to relevance.

Special handling is applied for:

* summary
* summarize
* topics
* chapters
* contents

---

## 4. Planner

Decides the next action:

```text
GENERATE
RETRIEVE_MORE
REQUERY
```

---

## 5. Generator

Generates the final response using Groq Llama 3.1.

---

# Installation

## Clone Repository

```bash
git clone https://github.com/your-username/chat-with-pdf.git

cd chat-with-pdf
```

---

# Backend Setup

Create Virtual Environment

```bash
python -m venv venv
```

Activate Environment

Windows

```bash
venv\Scripts\activate
```

Linux / Mac

```bash
source venv/bin/activate
```

Install Dependencies

```bash
pip install -r requirements.txt
```

Create .env

```env
GROQ_API_KEY=your_groq_api_key
```

Run Backend

```bash
uvicorn app:app --reload
```

Backend runs on:

```text
http://localhost:8000
```

---

# Frontend Setup

Navigate to Client

```bash
cd client
```

Install Packages

```bash
npm install
```

Start React App

```bash
npm start
```

or

```bash
npm run dev
```

Frontend runs on:

```text
http://localhost:3000
```

or

```text
http://localhost:5173
```

---

# API Endpoints

## Upload PDFs

```http
POST /upload
```

Uploads and indexes PDFs.

Response

```json
{
  "message": "PDFs uploaded successfully",
  "pdfs": 2,
  "chunks": 372
}
```

---

## Chat

```http
POST /chat
```

Request

```json
{
  "question": "What is machine learning?",
  "history": []
}
```

Response

```json
{
  "answer": "Machine learning is a process where a machine improves its performance through experience."
}
```

---

# Example Questions

```text
What is machine learning?

What is reinforcement learning?

Summarize the book.

Explain supervised learning.

List the main topics covered.

Who wrote the book?
```

---

# Future Improvements

* Source Citations
* Streaming Responses
* Hybrid Search (BM25 + FAISS)
* Persistent Chat Memory
* Multi-User Support
* Authentication
* Cloud Deployment
* Agent Monitoring Dashboard

---

# Performance

Example PDF

```text
Chunks Indexed: 372
Chunking Time: 6.5 sec
Embedding Time: 40 sec
```

---

# Author

Saket Kumar

B.Tech CSE
GL Bajaj Institute of Technology and Management

---

# License

This project is for educational and learning purposes.
