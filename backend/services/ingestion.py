from langchain_community.document_loaders import (
    PyPDFLoader
)

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)


def create_chunks(pdf_paths):

    documents = []

    for pdf in pdf_paths:

        loader = PyPDFLoader(pdf)

        docs = loader.load()

        documents.extend(docs)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=200
    )

    chunks = text_splitter.split_documents(
        documents
    )

    clean_chunks = []

    for chunk in chunks:

        text = chunk.page_content.strip()

        # Skip very small chunks
        if len(text) < 100:
            continue

        clean_chunks.append(chunk)

    print(
        f"Total Chunks: {len(clean_chunks)}"
    )

    return clean_chunks