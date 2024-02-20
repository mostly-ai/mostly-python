import numpy as np
import pandas as pd
import pytest

from mostlyai.components import CreateGeneratorRequest
from mostlyai.exceptions import APIStatusError
from mostlyai.model import Generator


@pytest.fixture
def create_generator_config():
    return CreateGeneratorRequest(name="Test Generator")


@pytest.fixture
def sample_data():
    np.random.seed(0)  # For reproducible results
    df = pd.DataFrame(np.random.rand(5, 3), columns=['A', 'B', 'C'])
    return df



class TestGenerators:
    def test_list(self, mostly):
        for generator in mostly.generators.list():
            assert isinstance(generator, Generator)

    def test_create_get_update_delete(self, mostly, create_generator_config):
        generator = mostly.generators.create(create_generator_config)
        assert isinstance(generator, Generator)

        generator_id = str(generator.id)
        generator = mostly.generators.get(generator_id)
        assert str(generator.id) == generator_id

        updated_params = {"name": "Updated Test Generator"}
        updated_generator = generator.update(updated_params)
        assert updated_generator.name == "Updated Test Generator"

        generator.delete()

    def test_create_and_delete(self, mostly, sample_data):
        generator = mostly.generators.create(
            {"tables": [{"data": sample_data, "name": "sample"}]}
        )
        assert generator.name == "sample"  # defaulted after the single table name
        assert [c.name for c in generator.tables[0].columns] == ["A", "B", "C"]
        generator_id = generator.id
        generator.delete()
        with pytest.raises(APIStatusError) as err:
            mostly.generators.get(generator_id)
        assert "not found" in err.value.message
