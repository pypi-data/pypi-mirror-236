"""`POST`: `/api/v1/trace-list` endpoint configuration."""

import typing as tp

from pydantic import BaseModel

from ._endpoint import Endpoint
from .req_base import ReqBase
from .resp_base import RespBase


class ReqTraceList(ReqBase):
    """`POST`: `/api/v1/trace-list` request model.

    Attributes:
        uids: The subject/activity uids to pull the trace uids for.
    """

    uids: list[str]


class Trace(BaseModel):
    """A lightweight trace object, this doesn't include the data.

    Attributes:
        uid: The unique identifier for the trace.
        name: The trace's name, unique to the parent.
        parser_id: The id of the parser that manages the trace, for manually created, external traces this will always be 2, but e.g. for fit created traces this will be 3. Names can be duplicate across 2 different parsers.
    """

    uid: str
    name: str
    parser_id: int


class TraceWithData(Trace):
    """An extended `Trace` model which includes the data.

    Attributes:
        data: Any json-compatible data.
    """

    data: tp.Any


class RespTraceList(RespBase):
    """`POST`: `/api/v1/trace-list` response model.

    Attributes:
        traces: The traces of each requested parent uid, `dict[parent uid, list[Trace]]`.
    """

    traces: dict[str, list[Trace]]


end_trace_list = Endpoint("POST", "/trace-list", ReqTraceList, RespTraceList)
