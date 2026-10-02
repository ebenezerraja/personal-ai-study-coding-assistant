from router import route_question


questions = [
    "What is the latest Java version?",
    "What happened in AI news today?",
    "What is the current Python version?",
    "According to the PDF, what is binary search?",
    "Explain binary search.",
    "Explain Java inheritance.",
    "What is a search algorithm?"
]


for question in questions:

    route = route_question(question)

    print(f"Question: {question}")
    print(f"Route: {route}")
    print("-" * 60)