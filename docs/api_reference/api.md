::: mostlyai.client.api

# MostlyAI.connectors

## Examples

Here are some examples of how to use the `connectors` methods.

```python
from mostlyai import MostlyAI

# Firstly, make sure your MostlyAI client has been initialized
mostly = MostlyAI(api_key="YOUR_API_KEY")

# List and print all the connectors available
for connector in mostly.connectors.list():
    print(connector)

# Fetch a connector
connector_id = "some-connector-id"
connector = mostly.connectors.get(connector_id)

# Create a new connector
config = {
    "name": "New Connector",
    "type": "POSTGRES",
    # Other configuration parameters...
}
new_connector = mostly.connectors.create(config=config)
```

Methods available in `MostlyAI.connectors`.

::: mostlyai.client.connectors._MostlyConnectorsClient

# MostlyAI.generators

## Examples

Here are some examples of how to use the `generators` methods.

```python
from mostlyai import MostlyAI

# Firstly, make sure your MostlyAI client has been initialized
mostly = MostlyAI(api_key="YOUR_API_KEY")

# List and print all the generators available
for generator in mostly.generators.list():
    print(generator)

# Fetch a generator
generator_id = "some-generator-id"
generator = mostly.generator.get(generator_id)

# Create a new generator
# NOTE: this will not train the generator, but only create one
census_url = "https://github.com/mostly-ai/public-demo-data/raw/dev/census/census.csv.gz"
new_generator = mostly.generator.create(data=census_url)
```

Methods available in `MostlyAI.generators`.

::: mostlyai.client.generators._MostlyGeneratorsClient

# MostlyAI.synthetic_datasets

## Examples

Here are some examples of how to use the `synthetic_datasets` methods.

```python
from mostlyai import MostlyAI

# Firstly, make sure your MostlyAI client has been initialized
mostly = MostlyAI(api_key="YOUR_API_KEY")

# List and print all the synthetic datasets available
for synthetic_dataset in mostly.synthetic_datasets.list():
    print(synthetic_dataset)

# Fetch a synthetic dataset
synthetic_dataset_id = "some-synthetic-dataset_id-id"
synthetic_dataset = mostly.synthetic_datasets.get(synthetic_dataset_id)

# Create a new synthetic dataset
# NOTE: this will not generate the synthetic dataset, but will only create the corresponding job for it
generator_id = "your-trained-generator-id"
new_synthetic_dataset = mostly.synthetic_datasets.create({"generatorId": generator_id})
```

Methods available in `MostlyAI.synthetic_datasets`.

::: mostlyai.client.synthetic_datasets._MostlySyntheticDatasetsClient
