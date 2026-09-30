import requests # type: ignore[import-not-found]

from config import NTRS_BASE_URL


class NTRSClient:

    def search(self, query, page=1):

        url = f"{NTRS_BASE_URL}/citations/search"

        params = {
            "q": query,
            "page": page
        }

        response = requests.get(
            url,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        return response.json()

    def get_document(self, citation_id):

        url = f"{NTRS_BASE_URL}/citations/{citation_id}"

        response = requests.get(
            url,
            timeout=30
        )

        response.raise_for_status()

        return response.json()