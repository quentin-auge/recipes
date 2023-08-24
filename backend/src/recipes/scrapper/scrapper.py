from collections import defaultdict
import random
from recipes.scrapper.constants import MAX_SEARCH_RESULTS
from recipes.scrapper.search_results_parser import SearchResultsParser
from recipes.scrapper.url_builder import SearchUrlBuilder
from recipes.scrapper.url_cache import UrlCache
from recipes.scrapper.url_fetcher import UrlFetcher
from traitlets import Any


class SearchResultsScrapper:
    def __init__(self, url_builder: SearchUrlBuilder, url_cache: UrlCache | None = None):
        self.url_builder = url_builder
        self.url_fetcher = UrlFetcher(url_cache)

    def fetch_random_recipes(self, n: int, seed: int | None = None) -> list[dict]:
        metadata = self._fetch_metadata()

        total_nb_recipes, nb_recipes_per_page = metadata["total_nb_recipes"], metadata["nb_recipes_per_page"]
        assert n <= total_nb_recipes, f"Cannot fetch {n} recipes, only {total_nb_recipes} available"

        indices = random.Random(seed).sample(range(total_nb_recipes), n)

        return self.fetch_recipes_by_indices(indices, nb_recipes_per_page)

    def fetch_recipes_by_indices(self, indices: list[int], nb_recipes_per_page: int) -> list[dict]:
        recipes = []

        page_to_indices = self._paginate_indices(indices, nb_recipes_per_page)

        for page, indices in page_to_indices.items():
            page_recipes = self._fetch_recipes(page)
            recipes += [page_recipes[index] for index in indices]

        return recipes

    def _fetch_metadata(self) -> dict[str, Any]:
        url = self.url_builder.build(page=1)
        html = self.url_fetcher.fetch(url)
        metadata = SearchResultsParser(html).parse_metadata()
        return {
            "total_nb_recipes": min(metadata["nb_hits"], MAX_SEARCH_RESULTS),
            "nb_recipes_per_page": metadata["nb_hits_per_page"],
        }

    def _fetch_recipes(self, page: int) -> list[dict]:
        url = self.url_builder.build(page)
        html = self.url_fetcher.fetch(url)
        return SearchResultsParser(html).parse_recipes()

    def _paginate_indices(self, indices: list[int], nb_recipes_per_page: int) -> dict[int, list[int]]:
        paginated_indictes = defaultdict(list)

        for index in indices:
            page = index // nb_recipes_per_page + 1
            paginated_indictes[page].append(index % nb_recipes_per_page)

        return paginated_indictes