import pytest
from recipes.scrapper.scrapper import SearchResultsScrapper
from recipes.scrapper.url_builder import SearchUrlBuilder


@pytest.mark.parametrize("n_fetched_recipes", [5, 10, 11])
def test_fetch_random_recipes(mocker, n_fetched_recipes):
    url_builder = SearchUrlBuilder()
    scrapper = SearchResultsScrapper(url_builder)

    total_nb_recipes = 10
    nb_recipes_per_page = 3

    mocker.patch.object(scrapper, "_fetch_metadata", return_value={
        "total_nb_recipes": total_nb_recipes, "nb_recipes_per_page": nb_recipes_per_page
    })

    fetch_recipes_by_indices_mock = mocker.patch.object(scrapper, "fetch_recipes_by_indices")

    if n_fetched_recipes <= total_nb_recipes:  # Should work
        scrapper.fetch_random_recipes(n_fetched_recipes)
        fetch_recipes_by_indices_mock.assert_called_once()
    else:  # Should fail
        with pytest.raises(AssertionError, match=f"Cannot fetch {n_fetched_recipes} recipes, only {total_nb_recipes} available"):
            scrapper.fetch_random_recipes(n_fetched_recipes)



def test_fetch_recipes_by_indices(mocker):
    nb_recipes_per_page = 3
    recipes_indices = [0, 4, 2, 9, 1, 8, 6, 3]

    url_builder = SearchUrlBuilder()
    scrapper = SearchResultsScrapper(url_builder)

    def _fetch_recipes_mock(page: int) -> list[dict]:
        return [{"id": (page - 1) * nb_recipes_per_page + i} for i in range(nb_recipes_per_page)]
    mocker.patch.object(scrapper, "_fetch_recipes", _fetch_recipes_mock)

    recipes = scrapper.fetch_recipes_by_indices(recipes_indices, nb_recipes_per_page)
    expected_recipes = [{"id": i} for i in recipes_indices]

    assert {frozenset(r.items()) for r in recipes} == {frozenset(r.items()) for r in expected_recipes}

