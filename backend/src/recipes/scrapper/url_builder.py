import urllib.parse


class SearchUrlBuilder:
    base_url = "https://www.marmiton.org/recettes/recherche.aspx"

    def __init__(self):
        self.params = {}

    def build(self, page: int) -> str:
        params = dict(self.params)
        params["page"] = page
        return self.base_url + "?" + urllib.parse.urlencode(params)
