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
- Currently, it's fixed to fetch `public-api.yaml` from `dev`
- The relevant code sections from `tools/model.py` are stitched into the resulted `mostlyai/model.py`
- Make sure to set `GH_TOKEN` env var to be able to fetch the raw data for `public-api.yaml` from the associated GitHub repo

# Commitizen, Conventional Commits, Tags, and Releases on GitHub

[Commitizen](https://commitizen-tools.github.io/commitizen/) is included in the `dev` dependencies. Its purpose is to help us stick to [conventional commits](https://www.conventionalcommits.org/),
and by that make it easy to maintain versioning - bumps, tags, releases and a changelog.

The important part is to keep the commit messages (on the public repo) follow the above mentioned standard. There are several ways to ensure that:
- `cz commit` is one option, to help composing such a commit in CLI.
- There is a pre-commit hook, that could be used (for that, run locally: `pre-commit install --hook-type commit-msg --hook-type pre-push`)
- Otherwise, if comfortable, follow the commits guidelines independent of the helpers above

With that, changelog update is as easy as running `cz ch`. Bumping based on git log is done with `cz bump`. And so on.

# Publishing to PyPI

The setup is done via `pyproject.toml`, which contains the metadata, dependencies and other configurations.
In this project `poetry` is being used, and many of the sections being handled by it (those starting with `[tool.poetry]`).

It is important to stick to conventional [versioning](https://py-pkgs.org/07-releasing-versioning.html).
The most common one is being [semantic versioning](https://semver.org/).

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
