import abc
import hashlib
import os
from pathlib import Path

class UrlCache(abc.ABC):
    @abc.abstractmethod
    def read(self, url: str) -> str | None:
        raise NotImplementedError

    @abc.abstractmethod
    def write(self, url: str, content: str):
        raise NotImplementedError


class NoOpUrlCache(UrlCache):
    def read(self, url: str) -> str | None:
        return None

    def write(self, url: str, content: str):
        pass


class InMemoryUrlCache(UrlCache):
    def __init__(self):
        self._cache = {}

    def read(self, url: str) -> str | None:
        return self._cache[url]

    def write(self, url: str, content: str):
        self._cache[url] = content


class OnDiskUrlCache(UrlCache):
    def __init__(self, cache_dir: str):
        self.cache_dir = Path(cache_dir)

    def read(self, url: str) -> str:
        filepath = self._get_filepath(url)

        try:
            with open(filepath) as f:
                return f.read()
        except FileNotFoundError:
            return None
        except Exception as e:
            raise e

    def write(self, url: str, content: str) -> bool:
        os.makedirs(self.cache_dir, exist_ok=True)
        filepath = self._get_filepath(url)
        with open(filepath, "w") as f:
            f.write(content)

    def _get_filepath(self, url: str) -> Path:
        md5_url = hashlib.md5(url.encode("utf-8")).hexdigest()
        filename = f"{md5_url}.html"
        return self.cache_dir / filename