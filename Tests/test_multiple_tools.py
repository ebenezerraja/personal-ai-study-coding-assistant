from ollama import chat
from config import LLM_MODEL
from tools import calculate, web_search
from tool_manager import execute_tool


questions = [
    "Calculate 125 * 48",
    "What is the latest Java version?"
]


for question in questions:

    print("\nUser:", question)

    messages = [
        {
            "role": "user",
            "content": question
        }
    ]

    response = chat(
        model=LLM_MODEL,
        messages=messages,
        tools=[calculate, web_search]
    )

    messages.append(response.message)

    if response.message.tool_calls:

        for call in response.message.tool_calls:

            tool_name = call.function.name
            arguments = call.function.arguments

            print("Tool selected:", tool_name)
            print("Arguments:", arguments)

            result = execute_tool(
                tool_name,
                arguments
            )

            messages.append({
                "role": "tool",
                "tool_name": tool_name,
                "content": result
            })

        final_response = chat(
            model=LLM_MODEL,
            messages=messages,
            tools=[calculate, web_search]
        )

        print("AI:", final_response.message.content)

    else:
        print("AI:", response.message.content)