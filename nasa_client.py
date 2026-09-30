import requests  # type: ignore[import-not-found]

from config import NASA_BASE_URL, NASA_API_KEY


class NASAClient:

    def __init__(self):
        self.api_key = NASA_API_KEY

    def search_images(self, query, page_size=10):

        url = "https://images-api.nasa.gov/search"

        params = {
            "q": query,
            "media_type": "image",
            "page_size": page_size
        }

        response = requests.get(
            url,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        return response.json()

    def get_asset_manifest(self, nasa_id):

        url = f"https://images-api.nasa.gov/asset/{nasa_id}"

        response = requests.get(
            url,
            timeout=30
        )

        response.raise_for_status()

        return response.json()