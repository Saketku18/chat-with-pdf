import json
import re

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from agents.llm import llm


prompt = ChatPromptTemplate.from_template(
"""
You are a planning agent.

Question:
{question}

Retrieved Context:
{context}

Choose ONE action.

GENERATE
- Context contains relevant information.
- Partial information is enough.
- Summaries are allowed.
- Explanations are allowed.
- Synthesis is allowed.

REQUERY
- Context is mostly unrelated.
- Better wording may help retrieval.

RETRIEVE_MORE
- Context is relevant.
- More chunks may improve answer quality.

NOT_FOUND
- Retrieved context is completely unrelated.

Return ONLY valid JSON. No explanation. No extra text.

Examples:

{{"action":"GENERATE"}}

{{"action":"REQUERY"}}

{{"action":"RETRIEVE_MORE"}}

{{"action":"NOT_FOUND"}}
"""
)

chain = (
    prompt
    | llm
    | StrOutputParser()
)

VALID_ACTIONS = {"GENERATE", "REQUERY", "RETRIEVE_MORE", "NOT_FOUND"}


def plan(question, docs):

    if len(docs) == 0:
        return "NOT_FOUND"

    context = "\n\n".join(doc.page_content for doc in docs)

    response = chain.invoke({"question": question, "context": context})

    print("\nPlanner Response:")
    print(response)

    # Extract JSON using regex to handle extra text from LLM
    match = re.search(r'\{.*?"action"\s*:\s*"(\w+)".*?\}', response, re.DOTALL)

    if match:
        action = match.group(1)
        if action in VALID_ACTIONS:
            return action

    print("\nPlanner Parse Error: Could not extract valid action")
    print("\nRaw Response:", response)
    return "GENERATE"