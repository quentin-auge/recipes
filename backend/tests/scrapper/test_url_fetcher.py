from tempfile import TemporaryDirectory

import pytest
from recipes.scrapper.url_cache import NoOpUrlCache, OnDiskUrlCache
from recipes.scrapper.url_fetcher import UrlFetcher

test_url, test_content = ("https://www.example1.com", "<example>content1</example>")


@pytest.fixture
def fetch_mock(mocker):
    return mocker.patch.object(UrlFetcher, "_fetch", return_value=test_content)


def test_uncached_fetcher(fetch_mock):
    url_fetcher = UrlFetcher(cache=None)

    url_cache = url_fetcher.url_cache
    assert url_cache.__class__ is NoOpUrlCache

    assert url_fetcher.fetch(test_url) == test_content
    fetch_mock.assert_called_once_with(test_url)  # Cache miss

    fetch_mock.reset_mock()

    assert url_fetcher.fetch(test_url) == test_content
    fetch_mock.assert_called_once_with(test_url)  # Cache miss, again


def test_cached_fetcher(fetch_mock):
    with TemporaryDirectory() as cache_dir:
        url_cache = OnDiskUrlCache(cache_dir)
        url_fetcher = UrlFetcher(url_cache)

        assert url_fetcher.fetch(test_url) == test_content
        fetch_mock.assert_called_once_with(test_url)  # Cache miss

        fetch_mock.reset_mock()

        url_fetcher.fetch(test_url) == test_content
        fetch_mock.assert_not_called()  # Cache hit
