import pdfplumber

def extract_text_from_pdf(path: str) -> str:
    text = ""

    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"

    return text
