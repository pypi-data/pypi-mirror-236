import httpx
import pytest
from pytest_httpx import HTTPXMock

import watz
import watz._endpoints._endpoint
from tests import _utils as ut


def test_err_unexpected_response(httpx_mock: HTTPXMock):
    httpx_mock.add_response(method="POST", json="Invalid")
    client = ut.fake_client()

    # Wrong response:
    with pytest.raises(ValueError, match="Unexpected data structure from Watz API.\nInvalid"):
        client.ping()

    # Wrong response but not even valid json
    httpx_mock.add_response(method="POST", html="Invalid")
    with pytest.raises(
        ValueError,
        match="Unexpected data structure from Watz API.\nb'Invalid'",
    ):
        client.ping()

    # Wrong status code:
    httpx_mock.add_response(method="POST", status_code=500, json="Something went wrong")
    with pytest.raises(
        httpx.HTTPStatusError,
        match='Unexpected status code from Watz API: 500\n"Something went wrong"',
    ):
        client.ping()


def test_err_api_unavail(httpx_mock: HTTPXMock):
    before_val = watz._endpoints._endpoint.CONN_WAIT_SECS
    try:
        watz._endpoints._endpoint.CONN_WAIT_SECS = 0
        client = ut.fake_client()
        httpx_mock.add_exception(httpx.ConnectError("No connect"))
        with pytest.raises(
            httpx.ConnectError, match="Failed to connect to Watz API after 5 attempts."
        ):
            client.ping()
    finally:
        watz._endpoints._endpoint.CONN_WAIT_SECS = before_val


def test_err_unserializable_input_data():
    client = ut.fake_client()
    with pytest.raises(
        TypeError, match="Serialization failure. Some entered types are not supported:"
    ):

        class ArbCls:
            pass

        client.trace_create(
            [
                watz.models.NewTrace(
                    parent_uid="foo",
                    name="foo",
                    data=ArbCls,
                )
            ]
        )


def test_err_dodgy_data_response(httpx_mock: HTTPXMock):
    client = ut.fake_client()

    # Invalid zip returned:
    httpx_mock.add_response(method="POST", content=b"Invalid")
    with pytest.raises(ValueError, match="Content was not readable as a zipfile."):
        client.trace_data(["foo"])

    # Valid zip but missing keys:
    httpx_mock.add_response(method="POST", content=ut.generate_zip({}).getvalue())
    with pytest.raises(ValueError, match="Missing required data in response."):
        client.trace_data(["foo"])
