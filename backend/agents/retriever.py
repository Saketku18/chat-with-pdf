def retrieve(
    vectorstore,
    question,
    k
):

    retriever = vectorstore.as_retriever(
         search_type="similarity",
        search_kwargs={"k": k}
    )

    return retriever.invoke(
        question
    )