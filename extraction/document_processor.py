from extraction.text import (
    extract_pdf_text
)

from extraction.specification_finder import (
    find_relevant_pages
)


def process_pdf(
    pdf_path
):

    print(
        "\nExtracting PDF text..."
    )

    pages = extract_pdf_text(
        pdf_path
    )

    print(
        f"Extracted {len(pages)} pages."
    )

    relevant_pages = find_relevant_pages(
        pages
    )

    print(
        f"Found {len(relevant_pages)} "
        "potentially relevant pages."
    )

    return relevant_pages