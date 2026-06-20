from langchain_cohere import CohereEmbeddings

from langchain_community.vectorstores import (
    FAISS
)
import os
embeddings = CohereEmbeddings(
    model="embed-english-light-v3.0",
    cohere_api_key=os.getenv("COHERE_API_KEY")
)

def create_vectorstore(chunks):

    return FAISS.from_documents(
        chunks,
        embeddings
    )