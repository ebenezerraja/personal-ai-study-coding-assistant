from ollama import chat
from config import LLM_MODEL

from embedder import create_embedding
from vector_store import search_documents


def ask_from_documents(question):

    # --------------------------------
    # 1. Create embedding for question
    # --------------------------------

    query_embedding = create_embedding(question)


    # --------------------------------
    # 2. Search relevant document chunks
    # --------------------------------

    results = search_documents(
        query_embedding,
        number_of_results=3
    )


    # --------------------------------
    # 3. Get the retrieved text
    # --------------------------------

    documents = results["documents"][0]


    # --------------------------------
    # 4. Combine the chunks
    # --------------------------------

    context = "\n\n".join(documents)


    # --------------------------------
    # 5. Create prompt for Qwen
    # --------------------------------

    prompt = f"""
You are answering a question using the user's documents.

Use the provided document context to answer the question.

If the answer is not present in the document context, say:
"I couldn't find that information in the document."

Do not make up information.

Document context:
-----------------
{context}
-----------------

Question:
{question}
"""


    # --------------------------------
    # 6. Ask Qwen
    # --------------------------------

    response = chat(
        model=LLM_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )


    return response.message.content