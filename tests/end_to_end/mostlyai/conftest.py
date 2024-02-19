import pytest

from mostlyai import MostlyAI


@pytest.fixture
def mostly():
    return MostlyAI()
