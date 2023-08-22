import urllib.parse

from recipes.scrapper.constants import MARMITON_ROOT_URL


class SearchUrlBuilder:
    base_url = MARMITON_ROOT_URL + "/recettes/recherche.aspx"

    def __init__(self):
        self.params = {}

    def build(self, page: int) -> str:
        params = dict(self.params)
        params["page"] = page
        return self.base_url + "?" + urllib.parse.urlencode(params)
