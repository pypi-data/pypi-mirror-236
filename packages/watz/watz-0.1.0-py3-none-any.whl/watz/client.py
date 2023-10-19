"""The central API client."""

import io
import zipfile
from typing import Optional

import orjson
import typing_extensions as tp
from pydantic_core import PydanticSerializationError

from ._client_base import ClientBase
from ._endpoints.activity_create import (
    Activity,
    NewActivity,
    ReqActivityCreate,
    end_activity_create,
)
from ._endpoints.ping import ReqPing, RespPing, end_ping
from ._endpoints.subject_create import (
    NewSubject,
    ReqSubjectCreate,
    end_subject_create,
)
from ._endpoints.subject_list import ReqSubjectList, Subject, end_subject_list
from ._endpoints.trace_create import (
    NewTrace,
    ReqTraceCreate,
    end_trace_create,
)
from ._endpoints.trace_data import ReqTraceData, end_trace_data
from ._endpoints.trace_list import ReqTraceList, Trace, TraceWithData, end_trace_list


class Client(ClientBase):
    """The central API client."""

    def __init__(
        self,
        secret: Optional[tp.Optional[str]] = None,
        base: str = "https://watz.coach",
    ):
        """Instantiates a new client.

        Args:
            secret (tp.Optional[str], optional): The API key. If omitted, will be read from the WATZ_SECRET environment variable.
            base (str, optional): The base URL of the Watz API.
        """
        super().__init__(base=base, secret=secret, version=1)

    def ping(self) -> RespPing:
        """Availability check. Pings the API.

        Returns:
            RespPing
        """
        return end_ping.call(self._session, ReqPing())

    def subject_list(self) -> list[Subject]:
        """Retrieve the caller's subjects.

        Returns:
            list[Subject]
        """
        return end_subject_list.call(self._session, ReqSubjectList()).subjects

    def trace_list(self, uids: list[str]) -> dict[str, list[Trace]]:
        """Retrieves the trace metadata for the requested subjects/activities.

        Args:
            uids (list[str]): The subject/activity uids to retrieve trace metadata for.

        Returns:
            dict[str, list[Trace]]: The parent uid as key and list of their traces as values.
        """
        return end_trace_list.call(
            self._session,
            ReqTraceList(uids=uids),
        ).traces

    def trace_data(self, uids: list[str]) -> list[bytes]:
        """Retrieves the trace data for the request traces.

        Args:
            uids (list[str]): The trace uids to retrieve data for.

        Returns:
            list[bytes]: The encoded trace data objects in the same order they were requested. The data can be decoded with `orjson.loads(data)`.
        """
        src = end_trace_data.call(
            self._session,
            ReqTraceData(uids=uids),
        ).root
        try:
            with zipfile.ZipFile(io.BytesIO(src)) as zip_file:
                return [zip_file.read(uid) for uid in uids]
        except zipfile.BadZipFile as e:
            raise ValueError(
                "Unexpected response from Watz API. Content was not readable as a zipfile. Contents: '{}'".format(
                    src
                )
            ) from e
        except KeyError as e:
            raise ValueError(
                "Unexpected response from Watz API. Missing required data in response."
            ) from e

    @tp.overload
    def trace_hydrate(self, traces: list[Trace]) -> list[TraceWithData]:
        ...

    @tp.overload
    def trace_hydrate(self, traces: dict[str, list[Trace]]) -> dict[str, list[TraceWithData]]:
        ...

    def trace_hydrate(
        self, traces: tp.Union[list[Trace], dict[str, list[Trace]]]
    ) -> tp.Union[list[TraceWithData], dict[str, list[TraceWithData]]]:
        """Hydrates `Trace` objects with their data, internally calls `client.trace_data()`. This method supports a simple list of traces or the direct output from `client.trace_list()` for ease of use.

        Args:
            traces (`list[Trace] | dict[str, list[Trace]]`): The traces to hydrate, either a specific list of traces, or the whole output from `client.trace_list()`.

        Returns:
            `list[TraceWithData] | dict[str, list[TraceWithData]]`: The hydrated traces are returned in the same structure as passed in, where `Trace` objects have been replaced with `TraceData` objects. `TraceData` objects have an extra `data` attribute which contains the trace data.
        """
        # Map needed when passing in as dict rather than list:
        trace_to_parent_map: dict[str, str] = {}
        if isinstance(traces, list):
            in_traces = traces
        else:
            trace_to_parent_map = {}
            in_traces = []
            for parent_uid, trace_group in traces.items():
                for trace in trace_group:
                    trace_to_parent_map[trace.uid] = parent_uid
                    in_traces.append(trace)

        hydrated_traces = [
            TraceWithData(**trace.model_dump(), data=orjson.loads(data))
            for trace, data in zip(in_traces, self.trace_data([trace.uid for trace in in_traces]))
        ]

        if isinstance(traces, list):
            return hydrated_traces

        out_map: dict[str, list[TraceWithData]] = {}
        for trace in hydrated_traces:
            parent_uid = trace_to_parent_map[trace.uid]
            try:
                out_map[parent_uid].append(trace)
            except KeyError:
                out_map[parent_uid] = [trace]

        return out_map

    def subject_create(self, subjects: list[NewSubject]) -> list[Subject]:
        """Create new subjects.

        Args:
            subjects (list[NewSubject]): The subjects to create.

        Returns:
            list[Subject]: The created subject models, in the same order they were supplied.
        """
        return end_subject_create.call(
            self._session,
            ReqSubjectCreate(
                subjects=tp.cast(  # Pydantic can handle the conversion if needed.
                    list[NewSubject], subjects
                )
            ),
        ).subjects

    def activity_create(self, activities: list[NewActivity]) -> list[Activity]:
        """Create new activities.

        Args:
            activities (list[NewActivity]): The activities to create.

        Returns:
            list[Activity]: The created activity models, in the same order they were supplied.
        """
        return end_activity_create.call(
            self._session,
            ReqActivityCreate(activities=activities),
        ).activities

    def trace_create(self, traces: list[NewTrace]) -> list[Trace]:
        """Create new traces.

        Args:
            traces (list[NewTrace]): The traces to create.

        Returns:
            list[Trace]: The created `Trace` objects, in the same order they were supplied.
        """
        try:
            return end_trace_create.call(
                self._session,
                ReqTraceCreate(traces=traces),
            ).traces
        except PydanticSerializationError as e:
            raise TypeError(
                "Serialization failure. Some entered types are not supported: '{}'".format(e)
            ) from e
