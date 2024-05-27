# External Environment Variables
GH_TOKEN ?= YourSecureToken

# Internal Variables
PUBLIC_OPENAPI_YAML_URL = https://raw.githubusercontent.com/mostly-ai/mostly-app-v2/dev/public-api/public-api.yaml?token=
PUBLIC_API_OUTPUT_PATH = mostlyai/model.py
PUBLIC_API_FULL_URL = $(PUBLIC_OPENAPI_YAML_URL)$(GH_TOKEN)

# Targets
.PHONY: help
help: ## show definition of each function
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-25s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: gen-public-model
gen-public-model: ## build pydantic models for public api
	@echo "Updating custom Jinja2 templates"
	python tools/extend_model.py
	@echo "Generating Pydantic models from $(PUBLIC_API_FULL_URL)"
	datamodel-codegen --url $(PUBLIC_API_FULL_URL) $(COMMON_OPTIONS)
	python tools/postproc_model.py
	black $(PUBLIC_API_OUTPUT_PATH) && isort $(PUBLIC_API_OUTPUT_PATH) && ruff --fix $(PUBLIC_API_OUTPUT_PATH)

# Common options for both targets
COMMON_OPTIONS = \
	--input-file-type openapi \
	--output $(PUBLIC_API_OUTPUT_PATH) \
	--snake-case-field \
	--target-python-version 3.9 \
	--use-schema-description \
	--field-constraints \
	--use-annotated \
	--collapse-root-models \
	--use-one-literal-as-default \
	--enum-field-as-literal one \
	--use-subclass-enum \
	--output-model-type pydantic_v2.BaseModel \
	--base-class mostlyai.base.CustomBaseModel \
	--custom-template-dir tools/custom_template

# Internal Variables for Release Workflow
VERSION := $(shell poetry version -s)
BRANCH := verbump_$(shell echo $(VERSION) | tr '.' '_')
TAG := $(VERSION)

# Targets for Release Workflow/Automation
.PHONY: release bump-version create-branch commit-tag pull-tags changelog push-changes re-tag build clean upload confirm-upload

# Variables
VERSION := $(shell poetry version -s)
BRANCH := verbump_$(shell echo $(VERSION) | tr '.' '_')
TAG := $(VERSION)

.PHONY: release bump-version create-branch commit-tag pull-tags changelog push-changes re-tag build clean upload confirm-upload

release: bump-version create-branch commit-tag pull-tags changelog push-changes re-tag build clean

bump-version: ## bump version (default: patch, options: patch, minor, major)
	@poetry version $(TYPE)
	@echo "Bumped version to $(VERSION)"

create-branch:
	@git checkout -b $(BRANCH)
	@echo "Created branch $(BRANCH)"

commit-tag:
	@git add pyproject.toml
	@git commit -m "Bump version to $(VERSION)"
	@git tag $(TAG)
	@echo "Tag $(TAG) created"

pull-tags:
	@git pull --tags
	@echo "Pulled all tags to ensure they are present locally"

changelog:
	@cz ch --incremental
	@git add CHANGELOG.md
	@git commit -m "Update changelog for version $(VERSION)"
	@echo "Changelog updated"

push-changes:
	@git push origin $(BRANCH)
	@echo "Pushed changes to $(BRANCH) branch"

re-tag:
	@git tag -d $(TAG)
	@git tag $(TAG)
	@git push origin $(TAG)
	@echo "Re-tagged and pushed $(TAG)"

build:
	@poetry build
	@echo "Built the project"

clean:
	@git checkout main
	@git merge $(BRANCH)
	@git push origin main
	@git branch -d $(BRANCH)
	@echo "Merged $(BRANCH) into main and cleaned up"

confirm-upload:
	@echo "Are you sure you want to upload to PyPI? (yes/no)"
	@read ans && [ $${ans:-no} = yes ]

upload: confirm-upload
    # Ensure the token is present in .pypirc file before running upload
	@twine upload dist/* --verbose
	@echo "Uploaded to PyPI"
