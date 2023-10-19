import io
import re
import typing as tp
import zipfile

from polyfactory.factories.pydantic_factory import ModelFactory
from pydantic import BaseModel
from pytest_httpx import HTTPXMock

import watz
from tests import _utils as ut
from watz._endpoints._endpoint import Endpoint, Method_T, Req_T, Resp_T
from watz._endpoints.resp_base import RespBase, RespBytes

T = tp.TypeVar("T", bound=BaseModel)


def gen_mock_model(model: type[T], **overrides: tp.Any) -> T:
    """Create mock data for a model.

    Args:
        model: The model to create mock data for.
        **overrides: Specific fields of the model to concretely set.

    Returns:
        The model instanstiated with mock data.
    """

    class Factory(ModelFactory):
        __model__ = model

    return tp.cast(T, Factory.build(factory_use_construct=False, **overrides))


def fake_client() -> watz.Client:
    return watz.Client(secret="foo")  # nosec


def mock_endpoint(
    httpx_mock: HTTPXMock,
    end: Endpoint[Method_T, Req_T, Resp_T],
    resp: tp.Optional[Resp_T] = None,
):
    if resp is None:
        if issubclass(end.resp_model, RespBytes):
            resp = tp.cast(Resp_T, RespBytes(root=generate_zip({"foo": b"bar"}).getvalue()))
        else:
            resp = tp.cast(Resp_T, tp.cast(RespBase, ut.gen_mock_model(end.resp_model)))

    httpx_mock.add_response(
        method=end.method,
        url=re.compile(r"https://watz.coach/api/v1/" + re.escape(end.path.strip("/")) + r"/?\??"),
        headers={
            "Content-Type": "application/json"
            if not isinstance(resp, RespBytes)
            else "application/zip"
        },
        content=resp.model_dump_json().encode() if not isinstance(resp, RespBytes) else resp.root,
    )


def generate_zip(data: dict[str, bytes]) -> io.BytesIO:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zip_file:
        for name, content in data.items():
            zip_file.writestr(name, content)
    return buf


def end_example(
    end: Endpoint[Method_T, Req_T, Resp_T],
) -> tp.Union[RespBytes, RespBase]:
    if issubclass(end.resp_model, RespBytes):
        return tp.cast(Resp_T, RespBytes(root=generate_zip({"foo": b"bar"}).getvalue()))
    return tp.cast(Resp_T, tp.cast(RespBase, ut.gen_mock_model(end.resp_model)))
