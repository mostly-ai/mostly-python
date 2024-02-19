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

# Tools

## model extension

While `datamodel-codegen` is a very handy tool for converting OpenAPI definitions into
pydantic objects (see `mostlyai/model.py`), it lacks the direct ability of adding extra functionality (e.g. methods)
to the classes it creates. For example, having `Generator.add_table(...)` is out of its scope, but
there's a trick being used here:
- `datamodel-codegen` works with `Jinja2` templates, and custom templates can be specified
- That specific template is located in `custom_template/pydantic_v2/BaseModel.jinja2`
- That template is created based on `tools/model.py`, which contains the functionality to add to existing classes
- Running `extend_model.py` updates the template based on `tools/model.py`

tl;dr the content of `tools/model.py` is being stitched to what `datamodel-codegen` generates natively.
Moreover, all of that happens by simply running `make gen-public-model`

# Common procedures

## Updating public model (based on `public-api.yaml`)

`make gen-public-model` does all the required actions to rewrite and format `mostlyai/model.py`.
Be mindful of the following:
- Currently, it's fixed to fetch `public-api.yaml` from `llb2/mstar`
- The relevant code sections from `tools/model.py` are stitched into the resulted `mostlyai/model.py`
- Make sure to set `GH_TOKEN` env var to be able to fetch the raw data for `public-api.yaml` from the associated GitHub repo

# Notes

- Make sure to set `MOSTLY_PASSWORD` env var to be able to authenticate using the default values.
