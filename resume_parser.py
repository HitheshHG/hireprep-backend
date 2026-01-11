import pdfplumber

def extract_text(file):
    text_chunks = []

    with pdfplumber.open(file.file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_chunks.append(page_text)

    return " ".join(text_chunks)
