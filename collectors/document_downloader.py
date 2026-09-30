import requests
from pathlib import Path


class DocumentDownloader:

    def __init__(self):

        self.session = requests.Session()

        self.session.headers.update({
            "User-Agent":
                "SpaceCrafted NASA Data Collector/1.0"
        })

    def download(
        self,
        url: str,
        output_path: str
    ):

        print(
            f"Downloading:\n{url}"
        )

        response = self.session.get(
            url,
            timeout=120,
            stream=True
        )

        response.raise_for_status()

        path = Path(output_path)

        path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            path,
            "wb"
        ) as file:

            for chunk in response.iter_content(
                chunk_size=1024 * 1024
            ):

                if chunk:
                    file.write(chunk)

        print(
            f"Saved: {path}"
        )

        return str(path)