from pdf_loader import extract_text_from_pdf
from chunker import split_text
from embedder import create_embedding
from vector_store import add_document_chunks
from config import KNOWLEDGE_DIRECTORY


pdf_path = f"{KNOWLEDGE_DIRECTORY}/DSA.pdf"


# Step 1: Extract PDF text
text = extract_text_from_pdf(pdf_path)


# Step 2: Split text into chunks
chunks = split_text(text)


# Step 3: Create embeddings
embeddings = []

for chunk in chunks:

    embedding = create_embedding(chunk)

    embeddings.append(embedding)


# Step 4: Store everything in ChromaDB
add_document_chunks(
    chunks,
    embeddings,
    "DSA.pdf"
)


print("PDF successfully stored in ChromaDB!")
print("Total chunks stored:", len(chunks))