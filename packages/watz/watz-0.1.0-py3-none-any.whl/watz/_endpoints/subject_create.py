"""`POST`: `/api/v1/subject-create` endpoint configuration."""

from pydantic import BaseModel

from ._endpoint import Endpoint
from .req_base import ReqBase
from .resp_base import RespBase
from .subject_list import Subject


class NewSubject(BaseModel):
    """A creator model for a subject.

    Attributes:
        email: The subject's email address. Currently, this will be used as the uid.
    """

    email: str


class ReqSubjectCreate(ReqBase):
    """`POST`: `/api/v1/subject-create` request model.

    Attributes:
        subjects: A list of subjects to create.
    """

    subjects: list[NewSubject]


class RespSubjectCreate(RespBase):
    """`POST`: `/api/v1/subject-create` response model.

    Attributes:
        subjects: The created subject models, in the same order they were supplied.
    """

    subjects: list[Subject]


end_subject_create = Endpoint("POST", "/subject-create", ReqSubjectCreate, RespSubjectCreate)
