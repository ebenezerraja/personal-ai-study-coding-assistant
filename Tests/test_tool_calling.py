from ollama import chat
from tools import calculate
from config import LLM_MODEL

question = "What is 25 * 16?"

messages = [
    {
        "role": "user",
        "content": question
    }
]

response = chat(
    model=LLM_MODEL,
    messages=messages,
    tools=[calculate]
)

# Add Qwen's response to the conversation
messages.append(response.message)

# Check whether Qwen requested a tool
if response.message.tool_calls:

    for call in response.message.tool_calls:

        if call.function.name == "calculate":

            result = calculate(**call.function.arguments)

            print("Tool called:", call.function.name)
            print("Arguments:", call.function.arguments)
            print("Tool result:", result)

            # Give the tool result back to Qwen
            messages.append({
                "role": "tool",
                "tool_name": call.function.name,
                "content": str(result)
            })

    # Ask Qwen for the final answer
    final_response = chat(
        model=LLM_MODEL,
        messages=messages,
        tools=[calculate]
    )

    print("\nAI:", final_response.message.content)

else:
    print("\nAI:", response.message.content)