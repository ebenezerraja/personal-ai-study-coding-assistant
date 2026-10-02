from ollama import chat
from web_search import search_web
from config import LLM_MODEL


def answer_from_web(question):

    # Step 1: Search the web
    results = search_web(question, max_results=5)

    if not results:
        return "I couldn't find any web results."

    # Step 2: Build context from search results
    context = ""

    for i, result in enumerate(results, start=1):
        context += f"""
Result {i}:
Title: {result["title"]}
URL: {result["url"]}
Description: {result["description"]}
"""

    # Step 3: Give the search results to Qwen
    prompt = f"""
You are a personal AI study and coding assistant.

Answer the user's question using the web search results below.

Rules:
1. Use the web search results as the primary source of information.
2. Do not rely on your older training knowledge when answering current or recent questions.
3. Pay attention to dates in the search results.
4. Prefer newer information over older information when answering time-sensitive questions.
5. Do not make up information.
6. If the search results do not contain enough information, say so.
7. Give a clear and simple answer.
8. Do not create your own Sources section.
9. Do not invent URLs.

Web search results:
-------------------
{context}
-------------------

User question:
{question}
"""

    # Step 4: Ask Qwen
    response = chat(
        model=LLM_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    answer = response.message.content

    return answer, results