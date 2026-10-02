from ollama import embed
from config import EMBEDDING_MODEL


def create_embedding(text):

    response = embed(
        model=EMBEDDING_MODEL,
        input=text
    )

    return response.embeddings[0]