"""`POST`: `/api/v1/subject-list` endpoint configuration."""

import datetime as dt

from pydantic import BaseModel

from ._endpoint import Endpoint
from .req_base import ReqBase
from .resp_base import RespBase


class ReqSubjectList(ReqBase):
    """`POST`: `/api/v1/subject-list` request model.

    No specific attributes.
    """

    pass


class Activity(BaseModel):
    """An activity of a subject.

    Attributes:
        uid: The activity's unique id.
        start_time: The start time of the activity.
        label: The activity's label.
    """

    uid: str
    start_time: dt.datetime
    label: str


class Subject(BaseModel):
    """A subject of a researcher.

    Attributes:
        uid: The subject's unique id. Currently, this is always the subject's email address.
        email: The subject's email address.
        activities: The subject's activities.
    """

    uid: str
    email: str
    activities: list[Activity]


class RespSubjectList(RespBase):
    """`POST`: `/api/v1/subject-list` response model.

    Attributes:
        subjects: The subjects of the researcher.
    """

    subjects: list[Subject]


end_subject_list = Endpoint("POST", "/subject-list", ReqSubjectList, RespSubjectList)
