import pytest
from pytest_httpx import HTTPXMock

import watz
from tests import _utils as ut
from watz._client_base import AUTH_HEADER, ENV_SECRET_NAME


def test_secret_arg(httpx_mock: HTTPXMock):
    client = ut.fake_client()
    assert client._session.headers[AUTH_HEADER] == "foo"


def test_secret_env(httpx_mock: HTTPXMock, monkeypatch: pytest.MonkeyPatch):
    with monkeypatch.context() as m:
        m.setenv(ENV_SECRET_NAME, "bar")
        client = watz.Client()
        assert client._session.headers[AUTH_HEADER] == "bar"


def test_secret_missing(httpx_mock: HTTPXMock):
    with pytest.raises(ValueError, match="No secret/api-key provided."):
        watz.Client()
