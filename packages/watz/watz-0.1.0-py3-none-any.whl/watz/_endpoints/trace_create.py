"""`POST`: `/api/v1/trace-create` endpoint configuration."""

import typing as tp

from pydantic import BaseModel, field_serializer

from watz.helpers import serialize

from ._endpoint import Endpoint
from .req_base import ReqBase
from .resp_base import RespBase
from .trace_list import Trace


class NewTrace(BaseModel):
    """A creator model for a trace.

    Attributes:
        parent_uid: The subject/activity uid to create the trace for.
        name: The trace's identifier, this must be unique to the subject/activity.
        data: Any json-compatible data to store.
    """

    parent_uid: str
    name: str
    data: tp.Any

    @field_serializer("data", when_used="json")
    def serialize_data_json(self, v: tp.Any, _info: tp.Any) -> str:
        """Custom types such as numpy arrays, datetimes, dataclasses etc are handled by orjson, so serialize with that."""
        # Must be stringified to send inside json (orjson returns bytes by default)
        return serialize(v).decode()


class ReqTraceCreate(ReqBase):
    """`POST`: `/api/v1/trace-create` request model.

    Attributes:
        traces: A list of traces to create.
    """

    traces: list[NewTrace]


class RespTraceCreate(RespBase):
    """`POST`: `/api/v1/trace-create` response model.

    Attributes:
        traces: The created `Trace` objects, in the same order they were supplied.
    """

    traces: list[Trace]


end_trace_create = Endpoint("POST", "/trace-create", ReqTraceCreate, RespTraceCreate)
