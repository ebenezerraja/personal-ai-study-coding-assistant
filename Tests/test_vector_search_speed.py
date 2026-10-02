import time

from embedder import create_embedding
from vector_store import search_documents


query = "Explain binary search"


# Measure embedding
embedding_start = time.time()

query_embedding = create_embedding(query)

embedding_time = time.time() - embedding_start


# Measure ChromaDB search
search_start = time.time()

results = search_documents(
    query_embedding,
    number_of_results=3
)

search_time = time.time() - search_start


print(f"Embedding time: {embedding_time:.2f} seconds")
print(f"ChromaDB search time: {search_time:.2f} seconds")

print(
    "Documents returned:",
    len(results["documents"][0])
)