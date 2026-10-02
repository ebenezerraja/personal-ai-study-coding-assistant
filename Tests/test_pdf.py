from pdf_loader import extract_text_from_pdf
from chunker import split_text
from config import KNOWLEDGE_DIRECTORY


pdf_path = f"{KNOWLEDGE_DIRECTORY}/DSA.pdf"

text = extract_text_from_pdf(pdf_path)

chunks = split_text(text)


print("Total chunks:", len(chunks))

for i, chunk in enumerate(chunks):

    print("\n" + "=" * 50)
    print(f"CHUNK {i + 1}")
    print("=" * 50)

    print(chunk)