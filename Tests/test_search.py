from embedder import create_embedding
from vector_store import search_documents


question = "What is the time complexity of binary search?"


# Convert question into an embedding
query_embedding = create_embedding(question)


# Search ChromaDB
results = search_documents(
    query_embedding,
    number_of_results=3
)


documents = results["documents"][0]


print("Search results:")
print("=" * 50)


for i, document in enumerate(documents):

    print(f"\nRESULT {i + 1}")
    print("-" * 50)
    print(document)