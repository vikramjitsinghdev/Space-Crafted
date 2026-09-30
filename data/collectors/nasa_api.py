import requests

from config import NASA_IMAGES_API


class NASAClient:

    def __init__(self):
        self.session = requests.Session()

    def search_images(
        self,
        query: str,
        page_size: int = 10
    ):

        url = f"{NASA_IMAGES_API}/search"

        params = {
            "q": query,
            "media_type": "image",
            "page_size": page_size
        }

        response = self.session.get(
            url,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        return response.json()

    def search_all_media(
        self,
        query: str,
        page_size: int = 10
    ):

        url = f"{NASA_IMAGES_API}/search"

        params = {
            "q": query,
            "page_size": page_size
        }

        response = self.session.get(
            url,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        return response.json()