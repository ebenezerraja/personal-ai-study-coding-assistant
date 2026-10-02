import fitz
from config import KNOWLEDGE_DIRECTORY


def extract_text_from_pdf(pdf_path):

    document = fitz.open(pdf_path)

    all_text = ""

    for page in document:

        text = page.get_text()

        all_text += text

        all_text += "\n"

    document.close()

    return all_text