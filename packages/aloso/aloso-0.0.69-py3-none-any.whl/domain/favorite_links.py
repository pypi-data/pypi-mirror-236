from dataclasses import dataclass


@dataclass
class FavoriteLinks:
    id: int
    name: str
    url: str

    def url_to_http(self, url):
        if not(url.startswith("http")):
            self.url = "http://" + url

