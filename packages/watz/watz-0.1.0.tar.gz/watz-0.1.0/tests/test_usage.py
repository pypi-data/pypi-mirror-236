import datetime as dt

import orjson
from pytest_httpx import HTTPXMock

import watz
from watz._endpoints.activity_create import end_activity_create
from watz._endpoints.ping import end_ping
from watz._endpoints.subject_create import end_subject_create
from watz._endpoints.subject_list import end_subject_list
from watz._endpoints.trace_create import end_trace_create
from watz._endpoints.trace_data import end_trace_data
from watz._endpoints.trace_list import end_trace_list
from watz.helpers import _all_supported_types_example, dump, serialize

from . import _utils as ut


def test_usage(httpx_mock: HTTPXMock):
    """A full run through of client usage. This is what the usage doc is based upon, if this needs to be changed, so does the usage doc."""
    client = watz.Client(secret="my secret")  # nosec

    # Ping the API to check availability:
    ut.mock_endpoint(
        httpx_mock, end_ping, resp=end_ping.resp_model(status="OK", whoami="foo@bar.com")
    )
    assert (
        client.ping().model_dump()
        == watz.models.Ping(status="OK", whoami="foo@bar.com").model_dump()
    )

    # Create some subjects:
    mocked_subject_create = end_subject_create.resp_model(
        subjects=[
            watz.models.Subject(
                uid="bar@bar.com",
                email="bar@bar.com",
                activities=[],
            ),
            watz.models.Subject(
                uid="foo@foo.com",
                email="foo@foo.com",
                activities=[],
            ),
        ]
    )
    ut.mock_endpoint(httpx_mock, end_subject_create, resp=mocked_subject_create)
    assert dump(
        client.subject_create(
            [
                watz.models.NewSubject(email="bar@bar.com"),
                watz.models.NewSubject(email="foo@foo.com"),
            ]
        )
    ) == dump(mocked_subject_create.subjects)

    # Create some activities, optionally add a fit file directly to an activity:
    act_2_time = dt.datetime(2021, 10, 1)
    now = dt.datetime.now()
    bar_act = watz.models.Activity(uid="1_act_uid", label="No Label", start_time=now)
    foo_act = watz.models.Activity(uid="2_act_uid", label="foo", start_time=act_2_time)
    mocked_activity_create = end_activity_create.resp_model(
        activities=[
            bar_act,
            foo_act,
        ]
    )
    ut.mock_endpoint(httpx_mock, end_activity_create, resp=mocked_activity_create)
    assert dump(
        client.activity_create(
            [
                watz.models.NewActivity(subject_uid="bar@bar.com"),
                watz.models.NewActivity(
                    subject_uid="foo@foo.com",
                    label="foo",
                    start_time=act_2_time,
                    # Adding a fit file will automatically create applicable traces from said file.
                    fit_files=[b"valid_fit_file_contents"],
                ),
            ]
        )
    ) == dump(mocked_activity_create.activities)

    # List the existing subjects and activities:
    mocked_subject_list = end_subject_list.resp_model(
        subjects=[
            watz.models.Subject(
                uid="bar@bar.com",
                email="bar@bar.com",
                activities=[bar_act],
            ),
            watz.models.Subject(
                uid="foo@foo.com",
                email="foo@foo.com",
                activities=[foo_act],
            ),
        ]
    )
    ut.mock_endpoint(httpx_mock, end_subject_list, resp=mocked_subject_list)
    assert dump(client.subject_list()) == dump(mocked_subject_list.subjects)

    # Create some traces for the users and their activities:
    mocked_trace_create = end_trace_create.resp_model(
        traces=[
            watz.models.Trace(uid="123", name="measurements", parser_id=2),
            watz.models.Trace(uid="456", name="measurements", parser_id=2),
            watz.models.Trace(uid="789", name="activity_misc", parser_id=2),
        ]
    )
    ut.mock_endpoint(httpx_mock, end_trace_create, resp=mocked_trace_create)
    supported_types, supported_types_serialized = _all_supported_types_example()
    assert dump(
        client.trace_create(
            [
                # Duplicate naming is not a problem when the parent_uid is different.
                watz.models.NewTrace(
                    parent_uid="bar@bar.com",
                    name="measurements",
                    data={
                        "height": 180,
                        "weight": 80,
                    },
                ),
                watz.models.NewTrace(
                    parent_uid="foo@foo.com",
                    name="measurements",
                    data={
                        "height": 170,
                        "weight": 70,
                    },
                ),
                watz.models.NewTrace(
                    parent_uid="1_act_uid",
                    name="activity_misc",
                    data=supported_types,
                ),
            ]
        )
    ) == dump(mocked_trace_create.traces)

    # Now list the available traces for specific parents:
    mocked_trace_list = end_trace_list.resp_model(
        traces={
            "bar@bar.com": [watz.models.Trace(uid="123", name="measurements", parser_id=2)],
            "foo@foo.com": [watz.models.Trace(uid="456", name="measurements", parser_id=2)],
            "1_act_uid": [watz.models.Trace(uid="789", name="activity_misc", parser_id=2)],
        }
    )
    ut.mock_endpoint(httpx_mock, end_trace_list, resp=mocked_trace_list)
    assert dump(client.trace_list(["bar@bar.com", "foo@foo.com", "1_act_uid"])) == dump(
        mocked_trace_list.traces
    )

    # And finally retrieve the data for the traces.
    mocked_trace_data = end_trace_data.resp_model(
        root=ut.generate_zip(
            {
                "123": serialize({"height": 180, "weight": 80}),
                "456": serialize({"height": 170, "weight": 70}),
                "789": supported_types_serialized,
            }
        ).getvalue()
    )
    ut.mock_endpoint(httpx_mock, end_trace_data, resp=mocked_trace_data)

    # This can be done on the dict outputted directly from trace_list, or on individual lists of traces:
    traces = client.trace_list(["bar@bar.com", "foo@foo.com", "1_act_uid"])
    assert dump(client.trace_hydrate(traces)) == dump(
        {
            "bar@bar.com": [
                watz.models.TraceWithData(
                    uid="123", name="measurements", parser_id=2, data={"height": 180, "weight": 80}
                )
            ],
            "foo@foo.com": [
                watz.models.TraceWithData(
                    uid="456", name="measurements", parser_id=2, data={"height": 170, "weight": 70}
                )
            ],
            "1_act_uid": [
                watz.models.TraceWithData(
                    uid="789",
                    name="activity_misc",
                    parser_id=2,
                    # Won't be the same as original due to some times being downcast to json compatible versions
                    data=orjson.loads(supported_types_serialized),
                )
            ],
        }
    )

    # It can also be done on a specific list of traces, outputting a list to match:
    assert dump(client.trace_hydrate(traces["bar@bar.com"])) == dump(
        [
            watz.models.TraceWithData(
                uid="123", name="measurements", parser_id=2, data={"height": 180, "weight": 80}
            ),
        ]
    )
