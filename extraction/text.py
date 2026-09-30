from pypdf import PdfReader


def extract_pdf_text(
    pdf_path: str
):

    reader = PdfReader(
        pdf_path
    )

    pages = []

    for page_number, page in enumerate(
        reader.pages
    ):

        try:

            text = page.extract_text()

        except Exception:

            text = None

        if text:

            pages.append({
                "page": page_number + 1,
                "text": text
            })

    return pages