"""`POST`: `/api/v1/trace-data` endpoint configuration."""

from ._endpoint import Endpoint
from .req_base import ReqBase
from .resp_base import RespBytes


class ReqTraceData(ReqBase):
    """`POST`: `/api/v1/trace-data` request model.

    Attributes:
        uids: The trace uids to pull data for.
    """

    uids: list[str]


end_trace_data = Endpoint("POST", "/trace-data", ReqTraceData, RespBytes)
