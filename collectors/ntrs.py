import requests

from config import NTRS_API


class NTRSClient:

    def __init__(self):

        self.session = requests.Session()

        self.session.headers.update({
            "User-Agent":
                "SpaceCrafted NASA Data Collector/1.0"
        })

    def search(
        self,
        query: str,
        page: int = 1,
        size: int = 10,
    ):

        url = (
            f"{NTRS_API}"
            "/citations/search"
        )

        params = {
            "q": query,
            "page": page,
            "size": size,
        }

        response = self.session.get(
            url,
            params=params,
            timeout=30,
        )

        response.raise_for_status()

        return response.json()

    def get_citation(
        self,
        citation_id: str,
    ):

        url = (
            f"{NTRS_API}"
            f"/citations/{citation_id}"
        )

        response = self.session.get(
            url,
            timeout=30,
        )

        response.raise_for_status()

        return response.json()

    def get_downloads(
        self,
        citation_id: str,
    ):

        url = (
            f"{NTRS_API}"
            f"/citations/{citation_id}"
            "/downloads"
        )

        response = self.session.get(
            url,
            timeout=30,
        )

        response.raise_for_status()

        return response.json()