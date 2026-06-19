from langchain_huggingface import (
    HuggingFaceEmbeddings
)

from langchain_community.vectorstores import (
    FAISS
)

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)

def create_vectorstore(chunks):

    return FAISS.from_documents(
        chunks,
        embeddings
    )