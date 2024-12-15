---
hide:
  - navigation
---

# Usage Examples

## Single-table tabular data

```python
# load original data
repo_url = 'https://github.com/mostly-ai/public-demo-data'
df_original = pd.read_csv(f'{repo_url}/raw/dev/census/census.csv.gz')

# train a generator
g = mostly.train(config={
        'name': 'US Census Income',       # name of the generator
        'tables': [{                      # provide list of table(s)
            'name': 'census',             # name of the table
            'data': df_original,          # the original data as pd.DataFrame
            'model_configuration': {      # tabular model configuration (optional)
                'max_training_time': 2,   # - limit training time (in minutes)
                # model, max_epochs,,..   # further model configurations (optional)
            },
            # columns, keys, compute,..   # further table configurations (optional)  
        }]
    }, 
    start=True,                           # start training immediately (default: True)
    wait=True,                            # wait for completion (default: True)
)

# probe for new samples a synthetic dataset
df_samples = mostly.probe(g, size=100)

# conditionally generate a hybrid synthetic dataset
df_seed = pd.DataFrame({
    'age': [28] * 10_000, 
    'native_country': ['Mexico', 'Cuba'] * 5_000
})
sd = mostly.generate(g, seed=df_seed)
df_synthetic = sd.data()
```

## Multi-table tabular data

```python
# load original data
repo_url = 'https://github.com/mostly-ai/public-demo-data'
df_original_players = pd.read_csv(f'{repo_url}/raw/dev/baseball/players.csv.gz')
df_original_players = df_original_players[['id', 'country', 'weight', 'height']]
df_original_seasons = pd.read_csv(f'{repo_url}/raw/dev/baseball/batting.csv.gz')
df_original_seasons = df_original_seasons[['players_id', 'year', 'team', 'G', 'AB', 'HR']]

# train a generator
g = mostly.train(config={
    'name': 'Baseball',                   # name of the generator
    'tables': [{                          # provide list of table(s)
        'name': 'players',                # name of the table
        'data': df_original_players,      # the original data as pd.DataFrame
        'primary_key': 'id', 
    }, {
        'name': 'seasons',                # name of the table
        'data': df_original_seasons,      # the original data as pd.DataFrame
        'foreign_keys': [                 # foreign key configurations
            {'column': 'players_id', 'referenced_table': 'players', 'is_context': True},
        ],
    }],
}, start=True, wait=True)

# generate a new dataset of synthetic players and their synthetic season stats 
sd = mostly.generate(g, size=10_000)
df_synthetic_players = sd.data()['players']
df_synthetic_seasons = sd.data()['seasons']
```

## Single-table tabular and textual data

```python
# load original data with news headlines
repo_url = 'https://github.com/mostly-ai/public-demo-data'
original_df = pd.read_parquet(f'{repo_url}/raw/refs/heads/dev/headlines/headlines.parquet')

# print out available LANGUAGE models
print(mostly.models("LANGUAGE"))

# train a generator; increase max_training_time to improve quality
g = mostly.train(config={
    'name': 'Headlines',                   # name of the generator
    'tables': [{                           # provide list of table(s)
        'name': 'headlines',               # name of the table
        'data': original_df,               # the original data as pd.DataFrame
        'columns': [                       # configure TABULAR + LANGUAGE cols
            {'name': 'category', 'model_encoding_type': 'TABULAR_CATEGORICAL'},
            {'name': 'date', 'model_encoding_type': 'TABULAR_DATETIME'},
            {'name': 'headline', 'model_encoding_type': 'LANGUAGE_TEXT'},
        ],
        'model_configuration': {           # tabular model configuration (optional)
            'max_training_time': 5,        # - limit training time (in minutes)
        },
        'language_model_configuration': {  # language model configuration (optional)
            'max_training_time': 5,        # - limit training time (in minutes)
            'model': 'microsoft/phi-1_5',  # - select an available language model
        }
    }],
}, start=True, wait=True)

# conditionally generate 100 new headlines for the WELLNESS category
df_seed = pd.DataFrame({'category': ['WELLNESS'] * 100})
sd = mostly.generate(g, seed=df_seed)
df_synthetic = sd.data()
```
