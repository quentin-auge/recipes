from pathlib import Path

import pytest
from recipes.scrapper.search_results_parser import SearchResultsParser


@pytest.fixture(scope="module")
def html(data_folder) -> dict[int, str]:
    with open(data_folder / f"tatin_endives_search_results_page_2.html") as f:
        return f.read()

def test_parse_metadata(html):
    parser = SearchResultsParser(html)
    assert parser.parse_metadata() == {
        "nb_hits": 27,
        "nb_hits_per_page": 12,
        "nb_pages": 3,
    }

def test_parse_recipe_with_image(html):
    parser = SearchResultsParser(html)
    recipes = parser.parse_recipes()

    assert recipes[3] == {
        "title": "Tarte tatin d'endives facile",
        "url": "https://www.marmiton.org/recettes/recette_tarte-tatin-d-endives-facile_49138.aspx",
        "image_url": "https://assets.afcdn.com/recipe/20110430/56659_origin.jpg",
        "thumbnail_url": "https://assets.afcdn.com/recipe/20110430/56659_s96cx256cy192.jpg",
    }

def test_parse_recipe_without_image(html):
    parser = SearchResultsParser(html)
    recipes = parser.parse_recipes()

    assert recipes[1] == {
        "title": "Tatin d'endives aux lardons",
        "url": "https://www.marmiton.org/recettes/recette_tatin-d-endives-aux-lardons_85628.aspx",
        "image_url": None,
        "thumbnail_url": None,
    }