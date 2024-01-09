import pytest

from mostlyai.model import Generator


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

    def test_add_get_update_delete_table(
        self, mostly_client, new_generator_params, local_connector, postgres_connector
    ):
        generator = mostly_client.generators.create(**new_generator_params)

        new_table = generator.add_table(
            sourceConnectorId=str(postgres_connector.id), location="public.Customer"
        )
        table = generator.get_table(table_id=new_table.id)
        # TODO ensure update table works
        modelConfiguration = {
            "modelSize": "M",
            "enableFlexibleGeneration": True,
            "valueProtection": True,
            "rareCategoryReplacementMethod": "CONSTANT",
        }
        generator.update_table(
            table_id=str(table.id), modelConfiguration=modelConfiguration
        )
        generator.delete_table(table_id=str(table.id))

