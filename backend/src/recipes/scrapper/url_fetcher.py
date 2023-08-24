from recipes.scrapper.url_cache import NoOpUrlCache, UrlCache

import requests


class UrlFetcher:
    def __init__(self, cache: UrlCache | None = None):
        self.url_cache = cache or NoOpUrlCache()

    def fetch(self, url: str) -> str:
        content = self.url_cache.read(url)
        if not content:
            content = self._fetch(url)
            self.url_cache.write(url, content)
        return content

    def _fetch(self, url: str) -> str:
        response = requests.get(url)
        response.raise_for_status()
        return response.text