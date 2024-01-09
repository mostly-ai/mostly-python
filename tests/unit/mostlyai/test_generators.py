import pandas as pd
import pytest

from mostlyai.exceptions import APIStatusError
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
        self, mostly_client, new_generator_params, local_connector
    ):
        generator = mostly_client.generators.create(**new_generator_params)
        df = pd.DataFrame({'id': [1, 2], 'num': [3, 4]})
        new_table = generator.add_table_from_df_by_upload(df=df, name="simple")
        assert [c.name for c in new_table.columns] == ["id", "num"]
        table = generator.get_table(table_id=new_table.id)
        assert table.name == "simple"
        updated_table = generator.update_table(
            table_id=str(table.id), name="new"
        )
        assert updated_table.name == "new"
        generator.delete_table(table_id=str(table.id))

        with pytest.raises(APIStatusError) as err:
            generator.get_table(table_id=new_table.id)

        assert "not found" in err.value.message
