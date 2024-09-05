# MOSTLY AI - GenAI for Tabular Data

A Python wrapper for the MOSTLY AI platform (https://app.mostly.ai/).

| Intent                                          | Primitive                        |
|-------------------------------------------------|----------------------------------|
| Train a Generative AI on tabular data           | `g = mostly.train(data)`         |
| Empower your team with safe synthetic data      | `mostly.share(g, email)`         |
| Generate any number of synthetic data records   | `mostly.generate(g, size)`       |
| Prompt the generator for the data that you need | `mostly.generate(g, seed)`       |
| Live probe the generator on demand              | `mostly.probe(g, size \| seed)`  |
| Connect to any data source within your org      | `mostly.connect(config)`         |
| List the available models                       | `mostly.models(model_type)`      |
| List the available computes                     | `mostly.computes()`              |
| Info about the current user                     | `mostly.me()`                    |
| Info about the platform                         | `mostly.about()`                 |



## Installation

```shell
pip install -U mostlyai
```

## Basic Usage
```python
from mostlyai import MostlyAI
mostly = MostlyAI(api_key='your_api_key')
g = mostly.train(data)      # train a generator on your data
mostly.share(g, email)      # share the generator with your team
sd = mostly.generate(g)     # use the generator to create a synthetic dataset
syn = sd.data()             # consume the synthetic data as pandas DataFrame(s)
mostly.probe(g, size=100)   # generate few samples on demand
```

## Supported Methods

### Connectors

```python
c = mostly.connect(config)

c = mostly.connectors.create(config)
c = mostly.connectors.get(id)
it = mostly.connectors.list()
c = c.update(config)
ls = c.locations(prefix)
config = c.config()
c.open()
c.reload()
c.delete()
```

### Generators

```python
g = mostly.train(data, config, name, start=True, wait=True)

g = mostly.generators.create(config)
g = mostly.generators.get(id)
it = mostly.generators.list()
g = g.update(config)
config = g.config()
g.open()
g.reload()
g.delete()

# training
g.training.start()
g.training.progress()
g.training.cancel()
g.training.wait()

# import / export
g.export_to_file(file_path)
mostly.generators.import_from_file(file_path)
```

### Synthetic Datasets

```python
sd = mostly.generate(g, seed=seed)
sd = mostly.generate(g, size=size)
sd = mostly.generate(g, config=config)

sd = mostly.synthetic_datasets.create(g, config)
sd = mostly.synthetic_datasets.get(id)
it = mostly.synthetic_datasets.list()
config = sd.config()
sd.open()
sd.reload()
sd.delete()


sd.generation.start()
sd.generation.progress()
sd.generation.cancel()
sd.generation.wait()

sd.data()
sd.download(file, format)
```

### Synthetic Probes
```python
sp = mostly.probe(g, seed=seed)
sp = mostly.probe(g, size=size)
sp = mostly.probe(g, config=config)
```

### Sharing

```python
mostly.share(g | sd | c, email)
mostly.unshare(g | sd | c, email)

g.shares()
sd.shares()
c.shares()
```

### Job Configuration Info
```python
mostly.models(model_type)
mostly.computes()
```

### User Info

```python
mostly.me()
mostly.about()

```
