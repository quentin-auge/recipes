from tempfile import TemporaryDirectory

from recipes.scrapper.url_cache import OnDiskUrlCache

url1, content1 = ("https://www.example1.com", "<example>content1</example>")
url2, content2 = ("https://www.example2.com", "<example>content2</example>")

def test_on_disk_cache():
    with TemporaryDirectory() as cache_dir:
        url_cache = OnDiskUrlCache(cache_dir)

        assert url_cache.read(url1) is None  # Cache miss
        assert url_cache.read(url2) is None  # Cache miss

        url_cache.write(url1, content1)
        assert url_cache.read(url1) == content1  # Cache hit
        assert url_cache.read(url2) is None  # Cache miss

        url_cache.write(url2, content2)
        assert url_cache.read(url1) == content1  # Cache hit
        assert url_cache.read(url2) == content2  # Cache hit