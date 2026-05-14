# rag/loader/pdf_loader.py

import PyPDF2

def load_pdf(path: str) -> str:
    """
    Extract raw text from a PDF file.

    Parameters
    ----------
    path : str
        Path to the PDF file.

    Returns
    -------
    str
        The full extracted text from the PDF.
    """

    # Open the PDF in binary read mode.
    with open(path, "rb") as f:
        reader = PyPDF2.PdfReader(f)

        # Collect text from all pages.
        pages_text = []
        for page in reader.pages:
            # Extract text from each page.
            text = page.extract_text()
            if text:
                pages_text.append(text)

    # Join all pages into one big string.
    return "\n".join(pages_text)
