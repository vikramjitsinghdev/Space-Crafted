import requests
from pathlib import Path
from urllib.parse import unquote


class DocumentDownloader:

    def __init__(self):

        self.session = requests.Session()

        self.session.headers.update({
            "User-Agent":
                "SpaceCrafted NASA Data Collector/1.0"
        })

    def detect_file_type(
        self,
        content: bytes,
        content_type: str,
        url: str,
    ):
        """
        Detect the actual file type using both
        magic bytes and HTTP metadata.
        """

        content_type = (
            content_type
            or ""
        ).lower()

        url_lower = (
            url.lower()
            .split("?")[0]
        )

        # PDF magic signature
        if content.startswith(
            b"%PDF"
        ):
            return "pdf"

        # HTML
        stripped = (
            content[:500]
            .lstrip()
            .lower()
        )

        if (
            stripped.startswith(b"<!doctype html")
            or stripped.startswith(b"<html")
        ):
            return "html"

        # HTTP MIME
        if "application/pdf" in content_type:
            return "pdf"

        if "text/plain" in content_type:
            return "txt"

        if "text/html" in content_type:
            return "html"

        # URL fallback
        if url_lower.endswith(".pdf"):
            return "pdf"

        if url_lower.endswith(".txt"):
            return "txt"

        if url_lower.endswith(".html"):
            return "html"

        return "unknown"

    def download(
        self,
        url: str,
        output_path: str,
    ):

        print(
            "\nDownloading document:"
        )

        print(url)

        response = self.session.get(
            url,
            timeout=120,
        )

        response.raise_for_status()

        content = response.content

        actual_type = self.detect_file_type(
            content,
            response.headers.get(
                "Content-Type",
                "",
            ),
            url,
        )

        print(
            "Detected file type:",
            actual_type,
        )

        # Determine a safe extension
        extensions = {
            "pdf": ".pdf",
            "txt": ".txt",
            "html": ".html",
            "unknown": ".bin",
        }

        extension = extensions[
            actual_type
        ]

        path = Path(output_path)

        # Remove whatever extension the caller supplied.
        path = path.with_suffix(
            extension
        )

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(
            path,
            "wb",
        ) as file:

            file.write(content)

        print(
            f"Saved: {path}"
        )

        return {
            "path": str(path),
            "file_type": actual_type,
            "content_type": response.headers.get(
                "Content-Type",
                "",
            ),
            "size_bytes": len(content),
            "url": url,
        }