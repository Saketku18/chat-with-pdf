from langchain_community.cross_encoders import (
HuggingFaceCrossEncoder
)

reranker = HuggingFaceCrossEncoder(
    model_name="cross-encoder/ms-marco-MiniLM-L-6-v2"
)

def rerank(
    question,
    docs,
    top_k=5
):
    pairs = [
        (question, doc.page_content)
        for doc in docs
    ]

    scores = reranker.score(
        pairs
    )

    ranked = sorted(
        zip(scores, docs),
        reverse=True,
        key=lambda x: x[0]
    )

    return [
        doc
        for _, doc in ranked[:top_k]
    ]
