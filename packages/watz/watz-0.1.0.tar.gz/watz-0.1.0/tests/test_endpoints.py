import orjson
import typing_extensions as tp
from pydantic import BaseModel
from pytest_httpx import HTTPXMock

from tests import _utils as ut
from watz._endpoints._endpoint import Endpoint
from watz._endpoints.activity_create import NewActivity, end_activity_create
from watz._endpoints.ping import end_ping
from watz._endpoints.resp_base import RespBytes
from watz._endpoints.subject_create import NewSubject, end_subject_create
from watz._endpoints.subject_list import end_subject_list
from watz._endpoints.trace_create import NewTrace, end_trace_create
from watz._endpoints.trace_data import end_trace_data
from watz._endpoints.trace_list import end_trace_list

T = tp.TypeVar("T", bound=BaseModel)


def test_endpoints(httpx_mock: HTTPXMock):
    """A simple run of the mill call of each endpoint, to make sure no errors."""
    config: list[tuple[Endpoint, tp.Optional[tp.Any]]] = [
        (end_ping, None),
        (end_subject_list, None),
        (
            end_trace_data,
            RespBytes(
                root=ut.generate_zip(
                    {"sd": orjson.dumps([1, 2, 3]), "df": orjson.dumps("bar")}
                ).getvalue()
            ),
        ),
        (end_trace_list, None),
        (end_subject_create, None),
        (end_activity_create, None),
        (end_trace_create, None),
    ]
    for end, resp_override in config:
        ut.mock_endpoint(httpx_mock, end, resp=resp_override)

    client = ut.fake_client()

    client.ping()
    client.subject_list()
    client.trace_data(["sd", "df"])
    client.trace_list(["1", "a"])
    client.subject_create([NewSubject(email="foo@foo.com"), NewSubject(email="bar@bar.com")])
    client.activity_create(
        [
            NewActivity(subject_uid="foo@foo.com", label="foo"),
            NewActivity(subject_uid="bar@bar.com"),
        ]
    )
    client.trace_create(
        [
            NewTrace(
                parent_uid="foo@foo.com",
                name="foo",
                data=[{"x": 1, "y": 2}, 1, 2, 3, True, False],
            )
        ]
    )
