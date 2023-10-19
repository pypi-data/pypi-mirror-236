"""Data models returned from the client and those needed to pass into client methods."""

from ._endpoints.activity_create import NewActivity
from ._endpoints.ping import RespPing
from ._endpoints.subject_create import NewSubject
from ._endpoints.subject_list import Activity, Subject
from ._endpoints.trace_create import NewTrace
from ._endpoints.trace_list import Trace, TraceWithData

Ping = RespPing

__all__ = [
    "Activity",
    "Subject",
    "Trace",
    "Ping",
    "NewSubject",
    "NewActivity",
    "NewTrace",
    "TraceWithData",
]
