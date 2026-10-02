import chromadb
from config import VECTOR_DATABASE


client = chromadb.PersistentClient(
    path=VECTOR_DATABASE
)


# Create or open our document collection
collection = client.get_or_create_collection(
    name="documents"
)


def add_document_chunks(chunks, embeddings, source):

    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):

        collection.upsert(
            ids=[f"{source}_{i}"],
            documents=[chunk],
            embeddings=[embedding],
            metadatas=[
                {
                    "source": source,
                    "chunk": i
                }
            ]
        )


def get_collection():

    return collection

def search_documents(query_embedding, number_of_results=3):

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=number_of_results
    )

    return results