# MOSTLY AI - Python Client 🚀

[![Documentation](https://img.shields.io/badge/docs-latest-green)](https://mostly-ai.github.io/mostlyai-client/) [![stats](https://pepy.tech/badge/mostlyai)](https://pypi.org/project/mostlyai/) ![license](https://img.shields.io/github/license/mostly-ai/mostlyai-client) ![GitHub Release](https://img.shields.io/github/v/release/mostly-ai/mostlyai-client) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mostlyai)

The official Python client for [MOSTLY AI](https://app.mostly.ai/), the #1 platform for high-fidelity, privacy-safe **Synthetic Data**. 

The client allows you to programmatically create, browse and manage the 3 key resources of the MOSTLY AI platform: 

1. **Generators** - Train a synthetic data generator on your existing tabular or language data assets
2. **Synthetic Datasets** - Use a generator to create any number of synthetic samples to your needs
3. **Connectors** - Connect to any data source within your organization, for reading and writing data


| Intent                                        | Primitive                         |
|-----------------------------------------------|-----------------------------------|
| Train a Generator on tabular or language data | `g = mostly.train(config)`        |
| Generate any number of synthetic data records | `sd = mostly.generate(g, config)` |
| Live probe the generator on demand            | `df = mostly.probe(g, config)`    |
| Connect to any data source within your org    | `c = mostly.connect(config)`      |

See also our [Platform Documentation](https://mostly.ai/docs) for detailed feature descriptions and further Python examples.

## Installation

The latest release of `mostlyai` can be installed via pip:

```shell
pip install -U mostlyai
```

## Quick Start

Please obtain your personal API key from your [account settings page](https://app.mostly.ai/settings/api-keys), and adjust the following code snippet, before running it.

```python
import pandas as pd
from mostlyai import MostlyAI

# initialize client
mostly = MostlyAI(
    api_key='INSERT_YOUR_API_KEY',   # or set env var `MOSTLYAI_API_KEY` 
    base_url='https://app.mostly.ai' # or set env var `MOSTLYAI_BASE_URL`
)

# train a generator on original data
df_original = pd.read_csv('https://github.com/mostly-ai/public-demo-data/raw/dev/census/census.csv.gz')
g = mostly.train(name='census', data=df_original)  # shorthand syntax for 1-table config

# live probe the generator for synthetic samples
df_samples = mostly.probe(g, size=10)

# generate a synthetic dataset
sd = mostly.generate(g, size=10_000)

# download the synthetic dataset
df_synthetic = sd.data()
```

## Further Links

* [MOSTLY AI Website](https://mostly.ai/)
* [MOSTLY AI Blog](https://mostly.ai/blog) 
* [Platform Documentation](https://mostly.ai/docs)
* [OpenAPI Documentation](https://api-docs.mostly.ai/)
* [MOSTLY AI @ GitHub](https://github.com/mostly-ai/)
* [Synthetic Data - Quality Assurance](https://github.com/mostly-ai/mostlyai-qa/) `mostlyai-qa`
