from recipes.scrapper.url_builder import SearchUrlBuilder
from recipes.scrapper.url_cache import OnDiskUrlCache
from recipes.scrapper.url_fetcher import UrlFetcher

if __name__ == "__main__":
    url_cache = OnDiskUrlCache(".cache")
    url_fetcher = UrlFetcher(url_cache)

    for i in range(1, 11):
        url = SearchUrlBuilder().build(i)
        print(url)
        url_fetcher.fetch(url)