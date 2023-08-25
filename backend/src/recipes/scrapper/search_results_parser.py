from functools import lru_cache
import json
from bs4 import BeautifulSoup
from recipes.scrapper.constants import MARMITON_ROOT_URL


def cached_property(f):
    return property(lru_cache(maxsize=1)(f))


class SearchResultsParser:
    def __init__(self, html: str):
        self._html = html

    @cached_property
    def _next_data(self) -> dict:
        soup = BeautifulSoup(self._html, "html.parser")
        next_data_tag = soup.find("script", id="__NEXT_DATA__", type="application/json")
        if next_data_tag:
            return json.loads(next_data_tag.text)
        else:
            return {}

    @cached_property
    def _search_results(self) -> dict:
        return self._next_data["props"]["pageProps"]["searchResults"]

    def parse_metadata(self) -> dict[str, int]:
        return {
            "nb_hits": self._search_results["nbHits"],
            "nb_hits_per_page": self._search_results["hitsPerPage"],
            "nb_pages": self._search_results["nbPages"],
        }

    def parse_recipes(self) -> list[dict]:
        recipes = []
        for hit in self._search_results["hits"]:
            title = hit["title"]
            url = MARMITON_ROOT_URL + hit["url"]
            image_urls = hit["image"]["pictureUrls"] if hit["image"] else {}
            image_url = image_urls.get("originNoCrop")
            thumbnail_url = image_urls.get("thumb")

            recipes.append(
                {
                    "title": title,
                    "url": url,
                    "image_url": image_url,
                    "thumbnail_url": thumbnail_url,
                }
            )

        return recipes
