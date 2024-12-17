---
hide:
  - navigation
---

# Syntax Overview

## Generators

```python
# shorthand syntax to train a new single-table generator
g = mostly.train(name: str, data: pd.DataFrame)

# train a new generator
g = mostly.train(config: dict | GeneratorConfig, start: bool, wait: bool)

# configure a new generator and launch separately
g = mostly.generators.create(config: dict | GeneratorConfig)
g.training.start()
g.training.wait()

# iterate over all your available generators
for g in mostly.generators.list():
    print(g.id, g.name)

# fetch a generator by id
g = mostly.generators.get(id: str)

# fetch a generator's configuration
config = g.config()

# open a generator in a new browser tab
g.open()

# update a generator
g.update(name: str, ...)

# delete a generator
g.delete()

# clone a generator
# 1. re-use configs, and start training from scratch
g1 = g.clone(training_status="NEW")       
# 2. or re-use configs, and weights to continue training 
g2 = g.clone(training_status="CONTINUE")
```

## Synthetic Datasets

```python
# shorthand syntax for generating a new synthetic dataset
sd = mostly.generate(g, size: int)

# shorthand syntax for conditionally generating a new synthetic dataset
sd = mostly.generate(g, seed: pd.DataFrame)

# generate a new synthetic dataset
sd = mostly.generate(g, config: dict | SyntheticDatasetConfig, start: bool, wait: bool)

# configure a new synthetic dataset and launch separately
sd = mostly.synthetic_datasets.create(config: dict | SyntheticDatasetConfig)
sd.generation.start()
sd.generation.wait()

# iterate over all your available synthetic datasets
for sd in mostly.synthetic_datasets.list():
    print(sd.id, sd.name)

# fetch a synthetic dataset by id
sd = mostly.synthetic_datasets.get(id: str)

# fetch a synthetic dataset's configuration
config = sd.config()

# open a synthetic dataset in a new browser tab
sd.open()

# download a synthetic dataset
sd.download(file: str, format: str)

# fetch the synthetic dataset's data
df = sd.data()

# update a synthetic dataset
sd.update(name: str, ...)

# delete a synthetic dataset
sd.delete()
```

Synthetic probes allow to instantly generate synthetic samples on demand, without storing these on the platform. This feature depends on the availability of **Live Probing** on the platform. The syntax is similar to generating a synthetic dataset, with the notable difference that its return value is already the synthetic data as pandas DataFrame(s).
```python
# shorthand syntax for probing for synthetic samples
df = mostly.probe(g, size: int)

# shorthand syntax for conditionally probing for synthetic samples
df = mostly.probe(g, seed: pd.DataFrame)

# probe for synthetic samples
df = mostly.probe(g, config: dict | SyntheticDatasetConfig)
```

## Connectors

Connectors can be used both as a source of original data for training a generator, as well as a destination for delivering the generated synthetic data samples to. Please see our [Platform Documentation](https://mostly.ai/docs), respectively our [Open API specificiations](https://github.com/mostly-ai/mostly-openapi/blob/main/public-api.yaml) for the full list of available connectors, and their corresponding configuration parameters.  

```python
# create a new connector
c = mostly.connect(config: dict | ConnectorConfig)

# fetch a connector by id
c = mostly.connectors.get(id: str)

# list all locations of a connector
ls = c.locations(prefix: str)

# iterate over all your available connectors
for c in mostly.connectors.list():
    print(c.id, c.name)

# update a connector
c.update(name: str, ...)

# fetch a connector's configuration
config = c.config()

# open a connector in a new browser tab
c.open()

# delete a connector
c.delete()
```

In order to use a connector as a source, pass its ID as a parameter to the `SourceTableConfig`:
```python
c = mostly.connect(config={
    "name": "My S3 Source Storage",
    "type": "S3_STORAGE",
    "access_type": "SOURCE",
    "config": {
        "access_key": "INSERT_YOUR_ACCESS_KEY",
    },
    "secrets": {
        "secret_key": "INSERT_YOUR_SECRET_KEY",
    }
})
g = mostly.train(config={
    "name": "US Census Income",
    "tables": [{
        "name": "census",
        "source_connector_id": c.id,
        "location": "s3://bucket/path_to_original"
    }]
})
```

In order to use a connector as a destination, pass its ID as a parameter to the `SourceTableConfig`:
```python
c = mostly.connect(config={
    "name": "My S3 Destination Storage",
    "type": "S3_STORAGE",
    "access_type": "DESTINATION",
    "config": {
        "access_key": "INSERT_YOUR_ACCESS_KEY",
    },
    "secrets": {
        "secret_key": "INSERT_YOUR_SECRET_KEY",
    }
})
sd = mostly.generate(g, config={
    "name": "US Census Income",
    "delivery": {
        "destination_connector_id": c.id,
        "location": "s3://bucket/path_to_synthetic"
    }
})
```

## Miscellaneous

```python
# fetch info on your user account
mostly.me()

# fetch info about the platform
mostly.about()

# list all available TABULAR models
mostly.models(model_type='TABULAR')

# list all available LANGUAGE models
mostly.models(model_type='LANGUAGE')

# list all available computes
mostly.computes()
```
