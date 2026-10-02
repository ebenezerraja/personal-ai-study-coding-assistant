from rag import ask_from_documents


question = "What is the time complexity of binary search?"


answer = ask_from_documents(question)


print("\nAI:")
print(answer)