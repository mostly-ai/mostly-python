# Copyright 2024 MOSTLY AI
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from unittest import skip

from mostlyai import MostlyAI
from mostlyai.client.domain import GeneratorConfig, SyntheticDatasetConfig
import pandas as pd


@skip("End-to-end tests require API access")
def test_end_to_end(tmp_path):
    # create some mock data
    df = pd.DataFrame(
        {
            "a": ["a1", "a2"] * 100,
            "b": [1, 2] * 100,
        }
    )

    # initialize client
    mostly = MostlyAI()

    ## GENERATOR

    # config via sugar
    g = mostly.train(data=df, name="Test 1", start=False)
    assert g.name == "Test 1"
    g.delete()

    # config via dict
    config = {
        "name": "Test 1",
        "tables": [
            {"name": "data", "data": df, "model_configuration": {"max_epochs": 1}}
        ],
    }
    g = mostly.train(config=config, start=False)
    assert g.name == "Test 1"
    g.delete()

    # config via class
    g = mostly.train(config=GeneratorConfig(**config), start=False)
    assert g.name == "Test 1"

    # update
    g.update(name="Test 2")
    assert g.name == "Test 2"
    g = mostly.generators.get(g.id)
    assert g.name == "Test 2"
    g_config = g.config()
    assert isinstance(g_config, GeneratorConfig)
    assert g_config.name == "Test 2"
    assert g_config.tables[0].model_configuration.max_epochs == 1

    # train
    g.training.start()
    g.training.wait()
    assert g.training_status.value == "DONE"  # .value shouldn't be needed

    ## SYNTHETIC DATASET

    # config via sugar
    sd = mostly.generate(g, size=100, start=False)
    assert sd.tables[0].configuration.sample_size == 100
    sd.delete()

    # config via dict
    config = {"tables": [{"name": "data", "configuration": {"sample_size": 100}}]}
    sd = mostly.generate(g, config=config, start=False)
    assert sd.name == "Test 2"
    sd_config = sd.config()
    assert isinstance(sd_config, SyntheticDatasetConfig)
    assert sd_config.tables[0].configuration.sample_size == 100
    sd.delete()

    # config via class
    config = {"tables": [{"name": "data", "configuration": {"sample_size": 100}}]}
    config = SyntheticDatasetConfig(**config)
    sd = mostly.generate(g, config=config, start=False)

    # update
    sd.update(name="Test 2")
    assert sd.name == "Test 2"
    sd = mostly.synthetic_datasets.get(sd.id)
    assert sd.name == "Test 2"
    sd_config = sd.config()
    assert isinstance(sd_config, SyntheticDatasetConfig)
    assert sd_config.name == "Test 2"
    assert sd_config.tables[0].configuration.sample_size == 100

    # generate
    sd.generation.start()
    sd.generation.wait()
    assert sd.generation_status.value == "DONE"  # .value shouldn't be needed
    syn = sd.data()
    assert len(syn) == 100

    # clean up
    g.delete()
    sd.delete()

    ## CONNECTOR

    c = mostly.connect(
        config={
            "name": "Test 1",
            "type": "S3_STORAGE",
            "access_type": "SOURCE",
            "config": {
                "access_key": "xxx",
            },
            "secrets": {
                "secret_key": "xxx",
            },
            # "test_connection": False,
        }
    )
    assert c.name == "Test 1"
    c.update(name="Test 2")
    assert c.name == "Test 2"

    c.delete()
