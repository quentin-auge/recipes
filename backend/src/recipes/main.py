import json
from recipes.scrapper.scrapper import SearchResultsScrapper
from recipes.scrapper.url_builder import SearchUrlBuilder
from recipes.scrapper.url_cache import OnDiskUrlCache

if __name__ == "__main__":
    url_builder = SearchUrlBuilder()
    scrapper = SearchResultsScrapper(url_builder, url_cache = OnDiskUrlCache(".cache"))
    random_recipes = scrapper.fetch_random_recipes(10)
    print(json.dumps(random_recipes, indent=2))
