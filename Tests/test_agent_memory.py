from agent import run_agent


conversation = []

questions = [
    "Explain binary search in simple words.",
    "What is its time complexity?",
    "Why is it faster than linear search?"
]


for question in questions:

    print("\nUser:", question)

    answer, tools_used, tool_results, elapsed_time = run_agent(
        question,
        conversation
    )

    print("AI:", answer)

    conversation.append({
        "role": "user",
        "content": question
    })

    conversation.append({
        "role": "assistant",
        "content": answer
    })