from pathlib import Path
from pypdf import PdfReader


def clean_text(text: str) -> str:
    if not text:
        return ""

    # Normalize whitespace
    lines = []

    for line in text.splitlines():
        line = " ".join(line.split())

        if line:
            lines.append(line)

    return "\n".join(lines)


def extract_pages(pdf_path: str):
    pdf_path = Path(pdf_path)

    reader = PdfReader(str(pdf_path))

    pages = []

    print(f"\nReading PDF: {pdf_path}")
    print(f"Total pages: {len(reader.pages)}")

    for page_number, page in enumerate(reader.pages, start=1):

        try:
            raw_text = page.extract_text() or ""
        except Exception as exc:
            print(
                f"Page {page_number} extraction failed: {exc}"
            )
            raw_text = ""

        text = clean_text(raw_text)

        pages.append({
            "page": page_number,
            "text": text,
            "character_count": len(text),
        })

    return pages


def extract_full_text(pdf_path: str) -> str:
    pages = extract_pages(pdf_path)

    return "\n\n".join(
        f"[PAGE {page['page']}]\n{page['text']}"
        for page in pages
        if page["text"]
    )