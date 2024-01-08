import pytest

from mostlyai import MostlyAI


@pytest.fixture
def mostly_client():
    return MostlyAI()
