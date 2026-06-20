# Chat with PDF - Agentic RAG System

An AI-powered PDF Question Answering application built using FastAPI, React, LangChain, FAISS, Cohere Embeddings, and Groq Llama 3.1.

The application allows users to upload one or more PDF documents and ask natural language questions. The system uses an Agentic Retrieval-Augmented Generation (RAG) pipeline with query rewriting, retrieval, reranking, planning, and streaming answer generation to provide accurate responses based on the uploaded documents.

---

# Live Demo

Frontend: https://chat-with-pdf-sooty-one.vercel.app

Backend: https://chat-with-pdf-backend-1d7e.onrender.com

---

# Features

* Multi-PDF Upload Support
* Automatic PDF Parsing and Chunking
* Vector Embeddings using Cohere API (embed-english-light-v3.0)
* FAISS Vector Database
* Reranking using Cohere API (rerank-english-v3.0)
* Query Rewriting Agent
* Retriever Agent
* Reranker Agent
* Planner Agent
* Generator Agent
* Streaming Responses
* Conversation History Support
* Agentic RAG Workflow
* FastAPI Backend
* React Frontend
* Groq Llama 3.1 Integration
* Deployed on Render (Backend) and Vercel (Frontend)

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
Reranker Agent (Cohere)
      │
      ▼
Planner Agent
      │
      ├── RETRIEVE_MORE
      ├── REQUERY
      └── GENERATE
      │
      ▼
Generator Agent (Groq Llama 3.1)
      │
      ▼
Streaming Answer
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
│   ├── app.py
│   ├── Dockerfile
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
* Deployed on Vercel

## Backend

* FastAPI
* Python
* LangChain
* Docker
* Deployed on Render

## AI & RAG

* Groq Llama 3.1 8B Instant
* Cohere Embeddings (embed-english-light-v3.0)
* Cohere Reranker (rerank-english-v3.0)
* FAISS Vector Database
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

Ranks retrieved chunks using Cohere Reranker API.

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

Generates the final streaming response using Groq Llama 3.1.

---

# Installation

## Clone Repository

```bash
git clone https://github.com/Saketku18/chat-with-pdf.git
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
COHERE_API_KEY=your_cohere_api_key
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

## Health Check

```http
GET /
```

Response

```json
{
  "status": "ok"
}
```

---

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

Response: Streaming text response

---

# Environment Variables

| Variable | Description |
|---|---|
| GROQ_API_KEY | Groq API key for Llama 3.1 |
| COHERE_API_KEY | Cohere API key for embeddings and reranking |

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

# Deployment

## Backend (Render)

* Deployed using Docker container
* Auto-deploys on git push to main branch

## Frontend (Vercel)

* Deployed using Vercel
* Auto-deploys on git push to main branch

---

# Performance

Example PDF

```text
Chunks Indexed: 372
Chunking Time: 6.5 sec
Embedding Time: ~2 sec (Cohere API)
```

---

# Future Improvements

* Source Citations
* Hybrid Search (BM25 + FAISS)
* Persistent Chat Memory
* Multi-User Support
* Authentication
* Agent Monitoring Dashboard

---

# Author

Saket Kumar

B.Tech CSE
GL Bajaj Institute of Technology and Management

---

# License

This project is for educational and learning purposes.
