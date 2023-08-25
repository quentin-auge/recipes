import pytest
from recipes.scrapper.search_results_parser import SearchResultsParser


@pytest.fixture(scope="module")
def html(data_folder):
    with open(data_folder / "recherche.aspx?aqt=tatin-endive&page=2") as f:
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

    assert recipes[2] == {
        "title": "Tatin d'endives caramélisées orange-miel",
        "url": "https://www.marmiton.org/recettes/recette_tatin-d-endives-caramelisees-orange-miel_214980.aspx",
        "image_url": "https://assets.afcdn.com/recipe/20201119/115747_origin.jpeg",
        "thumbnail_url": "https://assets.afcdn.com/recipe/20201119/115747_s96cx1024cy768.jpeg",
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
