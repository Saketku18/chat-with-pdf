from typing import List

from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel

import os
import shutil
import time

from services.ingestion import create_chunks
from services.vectorstore import create_vectorstore

from agents.retriever import retrieve
from agents.reranker import rerank
from agents.planner import plan
from agents.query_writer import rewrite
from agents.generator import generate
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

vectorstore = None


from typing import List

class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    question: str
    history: List[Message] = []


@app.post("/upload")
async def upload_pdfs(
    files: List[UploadFile] = File(...)
):
    global vectorstore

    os.makedirs("uploads", exist_ok=True)

    for filename in os.listdir("uploads"):
        filepath = os.path.join("uploads", filename)
        if os.path.isfile(filepath):
            os.remove(filepath)

    pdf_paths = []

    for file in files:
        if not file.filename.lower().endswith(".pdf"):
            return {"error": f"{file.filename} is not a PDF"}

        filepath = os.path.join("uploads", file.filename)

        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        pdf_paths.append(filepath)

    if len(pdf_paths) == 0:
        return {"error": "No PDF uploaded"}

    start = time.time()
    chunks = create_chunks(pdf_paths)
    print("Chunking Time:", round(time.time() - start, 2), "sec")

    start = time.time()
    vectorstore = create_vectorstore(chunks)
    print("Embedding Time:", round(time.time() - start, 2), "sec")

    return {
        "message": "PDFs uploaded successfully",
        "pdfs": len(pdf_paths),
        "chunks": len(chunks)
    }


@app.post("/chat")
async def chat(request: ChatRequest):
    global vectorstore

    if vectorstore is None:
        return {"error": "Upload a PDF first"}

    question = request.question
    history = request.history

    search_query = rewrite(
        question,
        history
    )

    print("Original Question:", question)
    print("Rewritten Query:", search_query)

    k = 15
    attempts = 0

    while attempts < 3:
        docs = retrieve(
    vectorstore,
    search_query,
    k
)

        summary_keywords = ["summary", "summarize", "topics", "chapters", "contents"]
        rerank_k = 15 if any(word in question.lower() for word in summary_keywords) else 5

        docs = rerank(question, docs, top_k=rerank_k)

        for i, doc in enumerate(docs[:5]):
            print(f"\n----- DOC {i+1} -----")
            print(doc.page_content[:500])

        action = plan(question, docs)
        print(f"Planner: {action}")

        if action == "GENERATE":
            answer = generate(
                question,
                docs,
                history
            )

            return {"answer": answer}

        elif action == "REQUERY":
            question = rewrite(question)

        elif action == "RETRIEVE_MORE":
            k += 10

        else:
            return {"answer": "Answer not found"}

        attempts += 1

    return {"answer": "Answer not found"}