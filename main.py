from ollama import chat
from fast_router import try_fast_path
from tools import web_search, pdf_search, memory_search
import time
from config import LLM_MODEL
from memory import (
    create_database,
    save_memory,
    get_memory,
    get_all_memories
)

from memory_extractor import extract_memory

from rag import ask_from_documents
from web_answer import answer_from_web
from memory_answer import answer_from_memory

from agent import run_agent
# Create the database if it doesn't exist
create_database()


# Conversation memory
conversation_history = []
    



print("Personal AI Assistant")
print()
print("Commands:")
print("  remember: key=value  → Save a memory")
print("  recall: key           → Retrieve a memory")
print("  memories              → Show all memories")
print("  pdf: question         → Ask a question about your PDFs")
print("  web: question         → Search the web")
print("  exit                  → Quit")
print("-" * 50)


while True:

    question = input("You: ").strip()


    # Exit
    if question.lower() == "exit":
        print("AI: Goodbye!")
        break

    if question.lower() == "help":
        print()
        print("Available commands:")
        print("  remember: key=value  → Save a memory")
        print("  recall: key           → Retrieve a memory")
        print("  memories              → Show all memories")
        print("  pdf: question         → Search your PDF")
        print("  web: question         → Search the web")
        print("  help                  → Show this help")
        print("  exit                  → Quit")
        print()
        continue
    if question.lower() == "memories":

        memories = get_all_memories()

        if not memories:
            print("AI: I don't have any stored memories.")
        else:
            print("AI: Here is what I remember:")

            for key, value in memories:
                print(f"- {key} = {value}")

        continue


    # Ignore empty input
    if not question:
        continue


    # --------------------------------
    # SAVE MEMORY
    # --------------------------------

    if question.lower().startswith("remember:"):

        memory = question[len("remember:"):].strip()

        if "=" not in memory:
            print("AI: Use this format:")
            print("    remember: key=value")
            continue

        key, value = memory.split("=", 1)

        key = key.strip()
        value = value.strip()

        if not key or not value:
            print("AI: Both key and value are required.")
            continue

        save_memory(key, value)

        print(f"AI: Saved memory → {key} = {value}")

        continue


    # --------------------------------
    # RETRIEVE MEMORY
    # --------------------------------

    if question.lower().startswith("recall:"):

        key = question[len("recall:"):].strip()

        if not key:
            print("AI: Use this format:")
            print("    recall: key")
            continue

        memory = get_memory(key)

        if memory:
            print(f"AI: {key} = {memory}")
        else:
            print(f"AI: I don't have a memory for '{key}'.")

        continue

    # --------------------------------
    # PDF / RAG
    # --------------------------------

    if question.lower().startswith("pdf:"):

        pdf_question = question[len("pdf:"):].strip()

        if not pdf_question:
            print("AI: Use this format:")
            print("    pdf: your question")
            continue

        try:
            answer = ask_from_documents(pdf_question)

            print("AI:", answer)

        except Exception as e:
            print("AI: I couldn't search the documents.")
            print("Error:", e)

        continue

    if question.lower().startswith("web:"):
        web_question = question[len("web:"):].strip()

        if not web_question:
            print("AI: Use this format:")
            print("    web: your question")
            continue

        try:
            answer, sources = answer_from_web(web_question)

            print("AI:", answer)

            print("\nWeb sources:")
            for source in sources:
                print(f"- {source['title']}")
                print(f"  {source['url']}")
        except Exception as e:
            print("AI: I couldn't search the web.")
            print("Error:", e)

        continue

    # --------------------------------
    # AUTOMATIC MEMORY
    # --------------------------------

    memory = extract_memory(question)

    if memory:
        key, value = memory

        save_memory(key, value)

        print(f"AI: I'll remember that → {key} = {value}")

        continue

    fast_result = try_fast_path(question)

    if fast_result is not None:

        fast_tool, result = fast_result

    # -----------------------------------------
    # Calculator Fast Path
    # -----------------------------------------

        if fast_tool == "calculate":

            answer = result

            print("AI:", answer)
            print("Tools used: calculate")
            print("Response time: Fast Path")
            print("\nCalculation source: Calculator tool")
            
            continue

    # -----------------------------------------
    # Web Fast Path
    # -----------------------------------------
        

        elif fast_tool == "web":

            print("Fast Path: web_search")
            web_start = time.time()

            search_results = web_search(result)

            search_time = time.time() - web_start

            print(f"Web search time: {search_time:.2f} seconds")

            # Format search results into clear text for the LLM
            search_context = search_results
            # Send the search results to the LLM
            # for a final natural-language answer.
            llm_start = time.time()
            response = chat(
                model=LLM_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are answering a question using web search results.\n\n"

                            "STRICT RULES:\n"

                            "1. Use the provided search results as the PRIMARY source of truth.\n"

                            "2. Do NOT rely on your training knowledge when answering current, "
                            "recent, latest, or time-sensitive questions.\n"

                            "3. Prefer official or authoritative sources when they are available.\n"

                            "4. If multiple search results provide different information, "
                            "prefer the most authoritative and recent source and mention "
                            "the conflict if necessary.\n"

                            "5. Never invent or assume a fact that is not supported by "
                            "the search results.\n"

                            "6. When the user asks for the 'latest version', interpret "
                            "'latest' as the latest stable officially released version, "
                            "NOT a future development branch, unreleased version, beta, "
                            "alpha, or release candidate, unless the user specifically "
                            "asks for those.\n"

                            "7. Prefer official sources over third-party sources when "
                            "determining releases, versions, dates, or other official facts.\n"

                            "8. For version numbers, dates, prices, statistics, and other "
                            "changing facts, use the value supported by the most reliable "
                            "and relevant search result instead of simply choosing the "
                            "largest number.\n"

                            "9. If the search results contain conflicting information, "
                            "explain the conflict briefly and use the most authoritative source.\n"

                            "10. Keep the answer concise and directly answer the question.\n"

                            "11. Mention the relevant source title when appropriate."
                        )
                        
                    },
                    {
                        "role": "user",
                        "content": f"""
                Question:
                {result}

                Web search results:
                --------------------
                {search_context}
                --------------------

                Answer the question using ONLY the information above.
                """
                    }
                ],
                options={
                    "temperature": 0
                }
            )

            llm_time = time.time() - llm_start

            print(f"Web answer LLM time: {llm_time:.2f} seconds")
    
                
            answer = response.message.content
            total_web_time = time.time() - web_start

            print("AI:", answer)
            print("Tools used: web_search")
            print(f"Response time: {total_web_time:.2f} seconds")

            print("\nWeb search results:")
            print(search_results)

                # -----------------------------------------
        # PDF Fast Path
        # -----------------------------------------

        elif fast_tool == "pdf":

            print("Fast Path: pdf_search")

            pdf_start = time.time()

            search_results = pdf_search(result)

            pdf_search_time = time.time() - pdf_start

            print(
                f"PDF search time: "
                f"{pdf_search_time:.2f} seconds"
            )

            llm_start = time.time()

            response = chat(
                model=LLM_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a study assistant answering "
                            "using the user's PDF.\n\n"
                            "STRICT RULES:\n"
                            "1. Use ONLY information supported by "
                            "the PDF search results.\n"
                            "2. Do NOT add information from your "
                            "own knowledge.\n"
                            "3. Explain the topic clearly and simply.\n"
                            "4. If the PDF does not contain enough "
                            "information, say so.\n"
                            "5. Do not guess."
                        )
                    },
                    {
                        "role": "user",
                        "content": f"""
    Question:
    {result}

    PDF search results:
    --------------------
    {search_results}
    --------------------

    Answer the question using ONLY the PDF information above.
    """
                    }
                ],
                options={
                    "temperature": 0
                }
            )

            llm_time = time.time() - llm_start

            answer = response.message.content

            total_pdf_time = time.time() - pdf_start

            print(
                f"PDF answer LLM time: "
                f"{llm_time:.2f} seconds"
            )

            print("AI:", answer)
            print("Tools used: pdf_search")
            print(
                f"Response time: "
                f"{total_pdf_time:.2f} seconds"
            )

            print("\nPDF source: DSA.pdf")

    # -----------------------------------------
    # Save conversation
    # -----------------------------------------
     # -----------------------------------------
    # Memory Fast Path
    # -----------------------------------------

        elif fast_tool == "memory":

            print("Fast Path: memory_search")

            memory_start = time.time()

            answer = answer_from_memory(result)

            memory_search_time = time.time() - memory_start

            print(
                f"Memory search time: "
                f"{memory_search_time:.2f} seconds"
            )

            if answer is None:
                answer = (
                    "I couldn't find that information "
                    "in your stored memory."
                )

            print("AI:", answer)
            print("Tools used: memory_search")
            print("Response time: Fast Path")
            print("\nMemory source: SQLite")


        # -----------------------------------------
# NORMAL AI AGENT
# -----------------------------------------

    if fast_result is None:

        try:
            answer, tools_used, tool_results, response_time = run_agent(
                question,
                conversation_history
            )

            print()
            print("=" * 60)
            print("AI:")
            print(answer)
            print()

            if tools_used:
                print("Tools:", ", ".join(tools_used))
            else:
                print("Tools: None")

            print(f"Time: {response_time:.2f} seconds")
            print("=" * 60)

            if "web_search" in tool_results:
                print("\nWeb search results:")
                print(tool_results["web_search"])

            if "pdf_search" in tool_results:
                print("\nPDF source: DSA.pdf")

            if "memory_search" in tool_results:
                print("\nMemory source: SQLite")

            if "calculate" in tool_results:
                print("\nCalculation source: Calculator tool")

            conversation_history.append({
                "role": "user",
                "content": question
            })

            conversation_history.append({
                "role": "assistant",
                "content": answer
            })

            conversation_history = conversation_history[-10:]

        except Exception as e:
            print("AI: I couldn't process the question.")
            print("Error:", e)