from pdf_loader import extract_text_from_pdf
from chunker import split_text
from embedder import create_embedding
from config import KNOWLEDGE_DIRECTORY


pdf_path = f"{KNOWLEDGE_DIRECTORY}/DSA.pdf"

text = extract_text_from_pdf(pdf_path)

chunks = split_text(text)

embedding = create_embedding(chunks[0])

print("Number of values in embedding:", len(embedding))

print("\nFirst 10 values:")
print(embedding[:10])