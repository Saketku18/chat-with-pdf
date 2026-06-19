from langchain_core.prompts import (
ChatPromptTemplate
)

from langchain_core.output_parsers import (
StrOutputParser
)

from agents.llm import llm

prompt = ChatPromptTemplate.from_template(
"""
You are a document question-answering assistant.

Use ONLY the provided context.

Rules:
- Answer in your own words.
- Do NOT copy large portions of the context.
- Keep answers concise (2-5 sentences).
- For definitions, provide a clear explanation.
- For lists, use bullet points.
- If the answer is not present in the context, say:
  "I could not find this information in the uploaded PDFs."

Conversation History:
{history}

Context:
{context}

Question:
{question}

Answer:
"""
)

chain = (
prompt
| llm
| StrOutputParser()
)

def generate(
    question,
    docs,
    history
):
    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )
    history_text = "\n".join(
    f"{msg.role}: {msg.content}"
    for msg in history
)

    result= chain.invoke(
        {
            "question": question,
            "context": context,
            "history": history_text
        }
    )
    print("\n===== GENERATED ANSWER =====")
    print(result)

    return result
