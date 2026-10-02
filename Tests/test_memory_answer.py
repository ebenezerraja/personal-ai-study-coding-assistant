from memory_answer import answer_from_memory

tests = [
    "What is my goal?",
    "What programming language am I learning?",
    "What tool do I use?",
]

for question in tests:
    print()
    print("Question:", question)
    print("Answer:", answer_from_memory(question))