from urllib.parse import urljoin


NTRS_BASE = "https://ntrs.nasa.gov"


def recursive_find_downloads(obj, found=None):
    """
    Recursively search arbitrary NTRS JSON for objects
    that appear to represent downloadable files.
    """

    if found is None:
        found = []

    if isinstance(obj, dict):

        # Look for common download/file indicators.
        keys = {
            key.lower()
            for key in obj.keys()
        }

        has_file_indicator = any(
            key in keys
            for key in [
                "url",
                "uri",
                "href",
                "downloadurl",
                "download_url",
                "filename",
                "file",
                "path",
                "mimetype",
                "mime_type",
            ]
        )

        if has_file_indicator:
            found.append(obj)

        for value in obj.values():
            recursive_find_downloads(
                value,
                found,
            )

    elif isinstance(obj, list):

        for item in obj:
            recursive_find_downloads(
                item,
                found,
            )

    return found


def normalize_url(value):
    """
    Convert relative NTRS URLs to absolute URLs.
    """

    if not value:
        return None

    if not isinstance(value, str):
        return None

    value = value.strip()

    if not value:
        return None

    if value.startswith("http://"):
        return value

    if value.startswith("https://"):
        return value

    if value.startswith("//"):
        return "https:" + value

    return urljoin(
        NTRS_BASE,
        value,
    )


def extract_url(obj):
    """
    Search an NTRS object for a likely downloadable URL.
    """

    if not isinstance(obj, dict):
        return None

    # Direct URL fields
    fields = [
        "url",
        "uri",
        "href",
        "downloadUrl",
        "download_url",
        "fileUrl",
        "file_url",
        "fulltext",
        "fullText",
        "pdf",
        "pdfUrl",
        "pdf_url",
    ]

    for field in fields:

        value = obj.get(field)

        if isinstance(value, str):

            url = normalize_url(value)

            if url:
                return url

    # Nested links
    for field in [
        "links",
        "link",
        "download",
        "downloads",
        "files",
        "file",
    ]:

        nested = obj.get(field)

        if nested is None:
            continue

        if isinstance(nested, dict):

            url = extract_url(nested)

            if url:
                return url

        elif isinstance(nested, list):

            for item in nested:

                url = extract_url(item)

                if url:
                    return url

    return None


def extract_filename(obj):
    """
    Attempt to find the filename represented by a download object.
    """

    if not isinstance(obj, dict):
        return None

    fields = [
        "name",
        "filename",
        "fileName",
        "file_name",
        "title",
    ]

    for field in fields:

        value = obj.get(field)

        if isinstance(value, str):
            value = value.strip()

            if value:
                return value

    return None


def extract_mimetype(obj):
    if not isinstance(obj, dict):
        return ""

    for field in [
        "mimetype",
        "mimeType",
        "mime_type",
        "contentType",
        "content_type",
        "type",
    ]:

        value = obj.get(field)

        if value:
            return str(value).lower()

    return ""


def is_probable_download(obj):
    """
    Decide whether an NTRS object represents a potentially
    downloadable document.
    """

    url = extract_url(obj)

    if not url:
        return False

    filename = (
        extract_filename(obj)
        or ""
    ).lower()

    mimetype = extract_mimetype(obj)

    # Exact PDF filename
    if filename.endswith(".pdf"):
        return True

    # Explicit PDF MIME type
    if "application/pdf" in mimetype:
        return True

    # Exact URL extension
    url_lower = url.lower().split("?")[0]

    if url_lower.endswith(".pdf"):
        return True

    # Text documents
    if filename.endswith(".txt"):
        return True

    if url_lower.endswith(".txt"):
        return True

    if "text/plain" in mimetype:
        return True

    # Other potentially useful documents
    if filename.endswith(
        (
            ".doc",
            ".docx",
            ".html",
        )
    ):
        return True

    return False


def find_downloads(data):
    """
    Return normalized download candidates from NTRS JSON.
    """

    objects = recursive_find_downloads(data)

    downloads = []

    seen_urls = set()

    for obj in objects:

        if not is_probable_download(obj):
            continue

        url = extract_url(obj)

        if not url:
            continue

        if url in seen_urls:
            continue

        seen_urls.add(url)

        downloads.append({
            "name": extract_filename(obj),
            "url": url,
            "mimetype": extract_mimetype(obj),
            "raw": obj,
        })

    return downloads


def choose_best_download(downloads):
    """
    Select the best available document.

    Preference:
        PDF > TXT > DOC/DOCX/HTML
    """

    candidates = []

    for download in downloads:

        url = download.get("url")

        if not url:
            continue

        name = (
            download.get("name")
            or ""
        ).lower()

        mime = (
            download.get("mimetype")
            or ""
        ).lower()

        url_lower = (
            url.lower()
            .split("?")[0]
        )

        score = 0

        # PDF
        if name.endswith(".pdf"):
            score += 100

        if url_lower.endswith(".pdf"):
            score += 100

        if "application/pdf" in mime:
            score += 100

        # Text
        if name.endswith(".txt"):
            score += 70

        if url_lower.endswith(".txt"):
            score += 70

        if "text/plain" in mime:
            score += 70

        # Other documents
        if name.endswith(".docx"):
            score += 40

        if name.endswith(".doc"):
            score += 30

        if name.endswith(".html"):
            score += 20

        # Full text
        if "fulltext" in name:
            score += 20

        if "full text" in name:
            score += 20

        candidates.append(
            (
                score,
                download,
                url,
            )
        )

    if not candidates:
        return None

    candidates.sort(
        key=lambda item: item[0],
        reverse=True,
    )

    return candidates[0]