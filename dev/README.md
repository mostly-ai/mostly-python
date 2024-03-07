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

# Publishing to PyPI

The setup is done via `pyproject.toml`, which contains the metadata, dependencies and other configurations.
In this project `poetry` is being used, and many of the sections being handled by it (those starting with `[tool.poetry]`).

It is important to stick to conventional [versioning](https://py-pkgs.org/07-releasing-versioning.html).
The most common one is being [semantic versioning](https://semver.org/).

## Copy public files to mostly-python repository

This repository could be seen as the python client itself *with* a scaffold (tools, internal documentation, etc.).
For the public repository, only a subset of the files contained here are needed. That is what `.public` file denotes.
`MOSTLY_PYTHON_REPO_PATH` env var must be set to the directory where `mostly-python` repository is located.
Then, running `make copy_public_files` will copy all the public files to the destination.

NOTE: It's important to keep both repositories in sync to avoid unaccounted changes or conflicts in the release process.

## Build

Run `poetry build`, which will create `sdist` and `wheel` files in `dist` directory.

## Test and Publish

For testing purposes, we could use [TestPyPi](https://test.pypi.org/).
Run `twine upload --repository testpypi dist/*`. Unless the credentials are saved in env vars or in `$HOME/.pypirc`, those will be promted.
For credentials use `__token__` as the `username` and the token itself as the `password`. To avoid entering them each time, add the following to `$HOME/.pypirc`:

```
[testpypi]
username = __token__
password = <TestPyPI token>
```

NOTE: Once a version was uploaded, it cannot be altered anymore!

Finally, uploading to [PyPI](https://pypi.org/) is done very similarly.

Run `twine upload dist/*`.
Have a similar `[pypi]` section in `$HOME/.pypirc` for convenience.

# Notes

- Make sure to set `MOSTLY_AI_PASSWORD` env var to be able to authenticate using the default values.
