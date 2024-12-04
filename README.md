# MOSTLY AI - Python Client 🚀

[![Documentation](https://img.shields.io/badge/docs-latest-green)](https://mostly-ai.github.io/mostly-python/) [![stats](https://pepy.tech/badge/mostlyai)](https://pypi.org/project/mostlyai/) ![license](https://img.shields.io/github/license/mostly-ai/mostly-python) ![GitHub Release](https://img.shields.io/github/v/release/mostly-ai/mostly-python) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mostlyai)

The official Python client for the [MOSTLY AI platform](https://app.mostly.ai/). See the [Platform Documentation](https://mostly.ai/docs) for detailed feature descriptions and Python examples. Check out our [Synthetic Data Tutorials](#synthetic-data-tutorials) for further end-to-end usage demonstrations.

## Overview

| Intent                                          | Primitive                                |
|-------------------------------------------------|------------------------------------------|
| Train a Generative AI on tabular data           | `g = mostly.train(data)`                 |
| Generate any number of synthetic data records   | `mostly.generate(g, size)`               |
| Prompt the generator for the data that you need | `mostly.generate(g, seed)`               |
| Live probe the generator on demand              | `mostly.probe(g, size \| seed)`          |
| Connect to any data source within your org      | `mostly.connect(config)`                 |
| List the available models                       | `mostly.models('LANGUAGE' \| 'TABULAR')` |
| List the available computes                     | `mostly.computes()`                      |
| Info about the current user                     | `mostly.me()`                            |
| Info about the platform                         | `mostly.about()`                         |

## Installation

The latest release of `mostlyai` can be installed via pip:

```shell
pip install -U mostlyai
```

## Quick Start

Please obtain your personal API key from your [settings page](https://app.mostly.ai/settings/api-keys). 

```python
import pandas as pd
from mostlyai import MostlyAI

# initialize client
mostly = MostlyAI(
    api_key='INSERT_YOUR_API_KEY',   # or set env var `MOSTLYAI_API_KEY` 
    base_url='https://app.mostly.ai' # or set env var `MOSTLYAI_BASE_URL`
)

# train a generator
df = pd.read_csv('https://github.com/mostly-ai/public-demo-data/raw/dev/census/census.csv.gz')
g = mostly.train(data=df)

# probe for some samples
syn = mostly.probe(g, size=10)

# generate a synthetic dataset
sd = mostly.generate(g, size=2_000)

# start using it
sd.data()
```

## Basic Usage

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

# clone
cloned_g = g.clone(training_status="NEW")       # clone the generator for new training
cloned_g = g.clone(training_status="CONTINUE")  # clone the generator and reuse its weights for continued training
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
mostly.models(model_type='TABULAR')
mostly.models(model_type='LANGUAGE')
mostly.computes()
```

### User Info

```python
mostly.me()
mostly.about()

```

## Synthetic Data Tutorials

* Validate synthetic data via **Train-Synthetic-Test-Real** [[run on Colab](https://colab.research.google.com/github/mostly-ai/mostly-tutorials/blob/dev/train-synthetic-test-real/TSTR.ipynb)]
* Explore the **size vs. accuracy trade-off** for synthetic data [[run on Colab](https://colab.research.google.com/github/mostly-ai/mostly-tutorials/blob/dev/size-vs-accuracy/size-vs-accuracy.ipynb)]
* **Rebalance** synthetic datasets for data augmentation [[run on Colab](https://colab.research.google.com/github/mostly-ai/mostly-tutorials/blob/dev/rebalancing/rebalancing.ipynb)]
* **Conditionally generate** synthetic (geo) data [[run on Colab](https://colab.research.google.com/github/mostly-ai/mostly-tutorials/blob/dev/conditional-generation/conditional-generation.ipynb)]
* **Explain AI**  with synthetic data [[run on Colab](https://colab.research.google.com/github/mostly-ai/mostly-tutorials/blob/dev/explainable-ai/explainable-ai.ipynb)]
* Generate **synthetic text** [[run on Colab](https://colab.research.google.com/github/mostly-ai/mostly-tutorials/blob/dev/synthetic-text/synthetic-text.ipynb)]
* Perform **multi-table synthesis** [[run on Colab](https://colab.research.google.com/github/mostly-ai/mostly-tutorials/blob/dev/multi-table/multi-table.ipynb)]
* Develop a **fake or real discriminator** with Synthetic Data [[run on Colab](https://colab.research.google.com/github/mostly-ai/mostly-tutorials/blob/dev/fake-or-real/fake-or-real.ipynb)]
* Close gaps in your data with **Smart Imputation** [[run on Colab](https://colab.research.google.com/github/mostly-ai/mostly-tutorials/blob/dev/smart-imputation/smart-imputation.ipynb)]
* Calculate accuracy and privacy metrics for **Quality Assurance** [[run on Colab](https://colab.research.google.com/github/mostly-ai/mostly-tutorials/blob/dev/quality-assurance/quality-assurance.ipynb)]

## Further Links

* [MOSTLY AI Website](https://mostly.ai/)
* [MOSTLY AI Blog](https://mostly.ai/blog) 
* [Platform Documentation](https://mostly.ai/docs)
* [OpenAPI Documentation](https://api-docs.mostly.ai/)
* [MOSTLY AI @ GitHub](https://github.com/mostly-ai/)
* [Synthetic Data - Quality Assurance](https://github.com/mostly-ai/mostlyai-qa/) `mostlyai-qa`
