import urllib.parse

from recipes.scrapper.url_builder import SearchUrlBuilder


def test_build_url():
    page = 31
    url = SearchUrlBuilder().build(page)
    assert f"page={page}" in url
