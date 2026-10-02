from fast_router import try_fast_path


tests = [
    "Calculate 125 * 48",
    "125 * 48",
    "What is the latest Python version?",
    "What is Python?",
    "Explain binary search from my PDF",
    "Search my PDF for binary search",
    "According to my PDF, what is binary search?",
    "What does my document say about arrays?",
    "Explain binary search",
    "What is my goal?",
    "What am I learning?",
    "What programming language am I learning?",
    "What tool do I use?",
    "How should I achieve my goal?",
    ]


for question in tests:

    result = try_fast_path(question)

    print()
    print("Question:", question)
    print("Result:", result)