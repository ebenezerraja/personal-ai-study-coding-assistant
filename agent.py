from ollama import chat
import time
from config import LLM_MODEL

from tools import (
    calculate,
    web_search,
    pdf_search,
    memory_search
)

from tool_manager import execute_tool


SYSTEM_PROMPT = """
You are a personal AI study and coding assistant.

You have access to four tools.

1. memory_search
Use this when the user asks about their personal information,
preferences, goals, programming language, tools, or anything
that may be stored in their memory.

2. pdf_search
Use this when the user asks about information in their PDF.

When pdf_search is used:
- Use the PDF search result as the primary source.
- Do not make up information that is not present in the PDF.
- If the answer is not found in the PDF result, clearly say that it was not found.

3. web_search

Use web_search ONLY when the user explicitly asks for:
- current information
- latest information
- today's information
- recent news or events
- live information
- information that must be checked online
- information that may have changed recently

Do NOT use web_search for general knowledge questions,
programming concepts, definitions, explanations, or
questions that can be answered from your existing knowledge.

When web_search is used:
- Use the search results as the primary source for current information.
- Do not rely on your training knowledge when it conflicts with the search results.
- Do not invent facts that are not supported by the search results.
- When appropriate, mention the source title or URL.

4. calculate

Use calculate for mathematical calculations.

Pass ONLY the mathematical expression to the calculator.

Do NOT add:
- /think
- explanations
- words
- Markdown
- extra instructions

Example:

User: Calculate 125 * 48

Correct tool argument:
125 * 48

Incorrect:
125 * 48 /think
Calculate 125 * 48
The answer to 125 * 48

Important rules:

Important rules:

- Use a tool only when the question requires it.
- Answer directly when no tool is necessary.
- Use the selected tool's result as the primary source for the answer.
- Do not guess information that should come from memory, the PDF,
  web search, or the calculator.
- If the answer is already present in the conversation history, use the conversation history first and do not call a tool unnecessarily.
- If the question asks about a personal fact, preference, goal, learning topic, or other information about the user that is not present in the conversation history, MUST use memory_search.
- Do not guess or claim that you do not know a personal fact when memory_search can retrieve it.

Response style:

- Give concise answers by default.
- Answer the user's exact question directly.
- Do not add unnecessary background information.
- For simple questions, keep the answer short.
- For simple calculations, give the result briefly.
- Give detailed explanations only when the user asks for them.
- For coding and DSA questions, provide step-by-step explanations when requested.
"""


def run_agent(question, conversation_history=None):

    start_time = time.time()

    tools_used = []
    tool_results = {}

    if conversation_history is None:
        conversation_history = []

    # Force memory search for personal questions
    personal_words = [
        "my ", "i am", "i'm", "am i", "do i", "what do i",
        "what am i", "what is my", "what's my"
    ]

    if any(word in question.lower() for word in personal_words):

        history_text = " ".join(
            message.get("content", "").lower()
            for message in conversation_history
        )

        if question.lower() not in history_text:

            memory_result = execute_tool(
                "memory_search",
                {"query": question}
            )

            if memory_result and "No relevant memories" not in memory_result:
                tools_used.append("memory_search")
                tool_results["memory_search"] = memory_result

                messages = [
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
                    }
                ]

                messages.extend(conversation_history)

                messages.append({
                    "role": "user",
                    "content": (
                        f"{question}\n\n"
                        f"Use this memory information to answer:\n"
                        f"{memory_result}"
                    )
                })

                response = chat(
                    model=LLM_MODEL,
                    messages=messages,
                    options={
                        "temperature": 0,
                        "num_predict": 800
                    }
                )

                elapsed_time = time.time() - start_time

                return (
                    response.message.content,
                    tools_used,
                    tool_results,
                    elapsed_time
                )



    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    messages.extend(conversation_history)

    messages.append({
        "role": "user",
        "content": question
    })

    tools = [
        calculate,
        web_search,
        pdf_search,
        memory_search
    ]

    # Allow the agent to perform multiple tool steps
    for step in range(5):
        llm_start = time.time()

        response = chat(
            model=LLM_MODEL,
            messages=messages,
            tools=tools,
            options={
                "temperature": 0,
                "num_predict": 800
            }
        )
        llm_time = time.time() - llm_start

        print(f"LLM response time: {llm_time:.2f} seconds")
        messages.append(response.message)

        if not response.message.tool_calls:

            elapsed_time = time.time() - start_time

            return (
                response.message.content,
                tools_used,
                tool_results,
                elapsed_time
            )

        # Execute requested tools
        for call in response.message.tool_calls:

            tool_name = call.function.name
            arguments = call.function.arguments

            if tool_name not in tools_used:
                tools_used.append(tool_name)

            print("Tool selected:", tool_name)
            print("Arguments:", arguments)

            try:
                tool_start = time.time()

                result = execute_tool(
                    tool_name,
                    arguments
                )

                tool_time = time.time() - tool_start

                print(f"Tool execution time: {tool_time:.2f} seconds")

            except Exception as e:

                print("Tool error:", e)

                result = (
                    f"The {tool_name} tool is currently unavailable. "
                    "Please try again."
                )

            tool_results[tool_name] = result

            print("Tool result:", result)

            messages.append({
                "role": "tool",
                "tool_name": tool_name,
                "content": result
            })

    elapsed_time = time.time() - start_time

    return (
        "I couldn't complete the request within the allowed tool steps.",
        tools_used,
        tool_results,
        elapsed_time
    )