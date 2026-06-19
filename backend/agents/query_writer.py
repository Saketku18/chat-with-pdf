from langchain_core.prompts import (
ChatPromptTemplate
)

from langchain_core.output_parsers import (
StrOutputParser
)

from agents.llm import llm

prompt = ChatPromptTemplate.from_template("""
You are a query rewriting assistant.

Conversation History:
{history}

Current Question:
{question}

Rewrite the question into a standalone query that contains all necessary context.
Rules:
1. Preserve the user's intent exactly.
2. Fix spelling mistakes only when obvious.
3. Resolve references using conversation history.
4. Do not introduce new requirements, comparisons, analyses, or time references.
5. If the question is already standalone, return it unchanged.
6. For short or ambiguous questions (e.g. "why?", "how?", "what to do?", "explain"), do not expand them unless conversation history clearly identifies the subject.
7. Never add words such as "today", "best", "compare", "analyze", "advantages", etc. unless explicitly present in the user's request.
Return only the rewritten query.
""")

chain = (
prompt
| llm
| StrOutputParser()
)

def rewrite(question, history):

    history_text = "\n".join(
        f"{msg.role}: {msg.content}"
        for msg in history
    ) if history else ""

    return chain.invoke(
        {
            "question": question,
            "history": history_text
        }
    )