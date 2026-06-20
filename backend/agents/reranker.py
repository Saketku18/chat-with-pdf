import cohere
import os

co = cohere.Client(os.getenv("COHERE_API_KEY"))


def rerank(question, docs, top_k=5):
    texts = [doc.page_content for doc in docs]

    results = co.rerank(
        query=question,
        documents=texts,
        top_n=top_k,
        model="rerank-english-v3.0"
    )

    return [docs[r.index] for r in results.results]