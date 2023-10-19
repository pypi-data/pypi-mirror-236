"""`POST`: `/api/v1/ping` endpoint configuration."""

import typing_extensions as tp

from ._endpoint import Endpoint
from .req_base import ReqBase
from .resp_base import RespBase


class ReqPing(ReqBase):
    """`POST`: `/api/v1/ping` request model.

    No specific attributes.
    """

    pass


class RespPing(RespBase):
    """`POST`: `/api/v1/ping` response model.

    Attributes:
        status: Always `"OK"`.
        whoami: The researcher's email address attached to the token.
    """

    status: tp.Literal["OK"]
    whoami: str


end_ping = Endpoint("POST", "/ping", ReqPing, RespPing)
