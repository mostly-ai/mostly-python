# MOSTLY AI

This repository provides a Python wrapper for the MOSTLY AI platform.

You can...

## Installation
```shell
pip install mostlyai
```

## Basic Usage
```python
from mostlyai import MostlyAI
mostly = MostlyAI(api_key='your_api_key') 
g = mostly.train(path)      # train a generator
sd = mostly.generate(g)     # generate a synthetic dataset
syn = sd.data()             # consume synthetic as pd.DataFrame
```

## Advanced Usage
```python
from mostlyai import MostlyAI
mostly = MostlyAI(api_key='your_api_key') 
```
