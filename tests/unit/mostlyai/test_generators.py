import pytest

from mostlyai.exceptions import APIStatusError
from mostlyai.model import Generator, SourceTable


@pytest.fixture
def new_generator_params():
    return {
        "name": "Test Generator",
    }


class TestGenerators:
    def test_list(self, mostly_client):
        for generator in mostly_client.generators.list():
            assert isinstance(generator, Generator)

    def test_create_get_update_delete(self, mostly_client, new_generator_params):
        generator = mostly_client.generators.create(**new_generator_params)
        assert isinstance(generator, Generator)

        generator_id = str(generator.id)
        generator = mostly_client.generators.get(generator_id)
        assert str(generator.id) == generator_id

        updated_params = {"name": "Updated Test Generator"}
        updated_generator = mostly_client.generators.update(
            generator_id, **updated_params
        )
        assert updated_generator.name == "Updated Test Generator"

        mostly_client.generators.delete(generator_id)
