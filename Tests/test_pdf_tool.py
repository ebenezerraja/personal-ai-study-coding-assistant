from tools import pdf_search


query = "What is the time complexity of binary search?"

result = pdf_search(query)

print("\nPDF Search Result:")
print("=" * 60)
print(result)