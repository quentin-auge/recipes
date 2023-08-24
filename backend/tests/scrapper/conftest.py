from pathlib import Path
import pytest

@pytest.fixture(scope="session")
def data_folder() -> Path:
    return Path(__file__).parent / "data"

@pytest.fixture(scope="session", autouse=True)
def forbid_http_requests(session_mocker):
    def urlopen_mock(self, method, url, **kwargs):
        raise RuntimeError(f"Unexpected HTTP call: {method} {url}")

    session_mocker.patch("urllib3.connectionpool.HTTPConnectionPool.urlopen", urlopen_mock)