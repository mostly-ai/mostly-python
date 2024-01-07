# python-client

This repository provides a Python wrapper for the Public API.
At its very initial stage it provides functionality for the `connector` section.

# Installation

Use your favourite environment manager (e.g. `conda`, `virtualenv`, etc.) to create one 
to be used for this repo.

Clone the repo:

```bash
git clone https://github.com/mostly-ai/python-client/
cd python-client
```

## Poetry

### Poetry Installation
```bash
curl -sSL https://install.python-poetry.org | python -
```

### Install dependencies via poetry
```bash
poetry install
```

# Notes

- Make sure to set `MOSTLY_PASSWORD` env var to be able to authenticate using the default values.
