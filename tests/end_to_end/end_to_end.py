from mostlyai import MostlyAI
from mostlyai.client.model import *
import pandas as pd
mostly = MostlyAI()

df = pd.read_csv('https://github.com/mostly-ai/public-demo-data/raw/refs/heads/dev/census/census.csv.gz').head(200)

## GENERATOR

# config via sugar
g = mostly.train(data=df, name='Test 1')
assert g.name == 'Test 1'
g.delete()

# config via dict
config = {'name': 'Test 1', 'tables': [{'name': 'data', 'data': df, 'model_configuration': {'max_epochs': 1}}]}
g = mostly.train(config=config, start=False)
assert g.name == 'Test 1'
g.delete()

# config via class
g = mostly.train(config=GeneratorConfig(**config), start=False)
assert g.name == 'Test 1'

# update
g = g.update(name='Test 2')
assert g.name == 'Test 2'
g = mostly.generators.get(g.id)
assert g.name == 'Test 2'
g_config = g.config()
assert isinstance(g_config, GeneratorConfig)
assert g_config.name == 'Test 2'
assert g_config.tables[0].model_configuration.max_epochs == 1

# train
g.training.start()
g = g.training.wait()
assert g.training_status == 'DONE'

# SYNTHETIC DATASET

# config via sugar
sd = mostly.generate(g, size=100, start=False)
assert sd.tables[0].configuration.sample_size == 100
sd.delete()

# config via dict
config = {'tables': [{'name': 'data', 'configuration': {'sample_size': 100}}]}
sd = mostly.generate(g, config=config, start=False)
assert sd.name == 'Test 2'
sd_config = sd.config()
assert isinstance(sd_config, SyntheticDatasetConfig)
assert sd_config.tables[0].configuration.sample_size == 100
sd.delete()

# config via class
config = {'tables': [{'name': 'data', 'configuration': {'sample_size': 100}}]}
config = SyntheticDatasetConfig(**config)
sd = mostly.generate(g, config=config, start=False)

# generate
sd.generation.start()
sd = sd.generation.wait()
assert sd.generation_status == 'DONE'
syn = sd.data()
assert len(syn) == 100

# clean up
g.delete()
sd.delete()
