from agent import run_agent


questions = [
    "What programming language am I learning?",
    "What is the time complexity of binary search according to my PDF?",
    "Calculate 125 * 48",
    "What is the latest Java version?"
]


for question in questions:

    print("\nUser:", question)

    answer = run_agent(question)

    print("AI:", answer)