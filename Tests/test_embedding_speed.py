import time

from embedder import create_embedding


query = "Explain binary search"


start = time.time()

embedding = create_embedding(query)

elapsed = time.time() - start


print("Embedding dimensions:", len(embedding))
print(f"Embedding time: {elapsed:.2f} seconds")