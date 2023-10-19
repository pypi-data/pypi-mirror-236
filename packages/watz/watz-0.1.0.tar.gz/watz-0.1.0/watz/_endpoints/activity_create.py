"""`POST`: `/api/v1/activity-create` endpoint configuration."""

import datetime as dt
import typing as tp

from pydantic import BaseModel, Field, field_serializer

from ._endpoint import Endpoint
from .req_base import ReqBase
from .resp_base import RespBase
from .subject_list import Activity


class NewActivity(BaseModel):
    """A creator model for an activity.

    Attributes:
        subject_uid: The uid of the subject to create the activity for.
        fit_files: A list of fit files to upload for the activity. `start_time` and `label` will be extracted from the fit files if possible.
        start_time: The start datetime of the activity, if omitted this will default to the current time. Fit files will override this value.
        label: An optional label for the activity. If omitted, the label will default to "No label". Fit files will override this value.
    """

    subject_uid: str

    # Optional:
    fit_files: list[bytes] = Field(default_factory=list)
    start_time: tp.Optional[dt.datetime] = None
    label: tp.Optional[str] = None

    @field_serializer("fit_files", when_used="json")
    def serialize_fit_files(self, v: tp.Any, _info: tp.Any) -> list[str]:
        """Fit files will be attached as files separately, replace with an empty list as bytes cannot be sent in json."""
        return []


class ReqActivityCreate(ReqBase):
    """`POST`: `/api/v1/activity-create` request model.

    Attributes:
        activities: A list of activities to create.
    """

    activities: list[NewActivity]

    def _extract_files(self) -> dict[str, bytes]:
        files = {}
        for act_index, activity in enumerate(self.activities):
            for fit_index, fit_file in enumerate(activity.fit_files):
                files[f"{act_index}-{fit_index}"] = fit_file
            activity.fit_files = []
        return files

    def _hydrate_files(self, files: dict[str, bytes]):
        act_map: dict[int, list[tuple[int, bytes]]] = {}
        for filename in files:
            act_index, fit_index = map(int, filename.split("-"))

            try:
                act_map[act_index].append((fit_index, files[filename]))
            except KeyError:
                act_map[act_index] = [(fit_index, files[filename])]

        for act_index, activity in enumerate(self.activities):
            activity.fit_files = []
            fit_files = act_map.get(act_index, [])
            for _, fit_file in sorted(fit_files, key=lambda x: x[0]):
                activity.fit_files.append(fit_file)


class RespActivityCreate(RespBase):
    """`POST`: `/api/v1/activity-create` response model.

    Attributes:
        activities: The created activity models, in the same order they were supplied.
    """

    activities: list[Activity]


end_activity_create = Endpoint("POST", "/activity-create", ReqActivityCreate, RespActivityCreate)
