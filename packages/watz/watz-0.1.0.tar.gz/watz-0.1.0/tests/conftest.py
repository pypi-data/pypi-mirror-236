import pytest


@pytest.fixture
def assert_all_responses_were_requested() -> bool:
    """Disable the httpx mock check that all responses were requested."""
    return False
