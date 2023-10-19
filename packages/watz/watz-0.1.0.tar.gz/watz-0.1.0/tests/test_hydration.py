import watz
from watz._endpoints.activity_create import end_activity_create
from watz._endpoints.ping import end_ping


def test_hydration():
    """Confirm extraction of files and then re-hydration results in an identical model for those that use it."""
    # Currently only used by activity create:
    example = end_activity_create.req_model(
        activities=[
            watz.models.NewActivity(
                subject_uid="foo",
                fit_files=[b"valid_fit_file_contents", b"secondary"],
            ),
            watz.models.NewActivity(
                subject_uid="bar",
                fit_files=[b"other"],
            ),
        ]
    )
    orig_dump = example.model_dump()
    files = example._extract_files()
    example._hydrate_files(files)
    assert orig_dump == example.model_dump()

    # Confirm running on something that doesn't use it is fine:
    example = end_ping.req_model()
    orig_dump = example.model_dump()
    files = example._extract_files()
    example._hydrate_files({})
    assert orig_dump == example.model_dump()
