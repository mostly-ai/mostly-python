# Internal Variables
PUBLIC_API_FULL_URL = https://raw.githubusercontent.com/mostly-ai/mostly-openapi/refs/heads/main/public-api.yaml
PUBLIC_API_OUTPUT_PATH = mostlyai/model.py

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

.PHONY: clean
clean: ## Remove .gitignore files
	git clean -fdX

# Internal Variables for Release Workflow
BUMP_TYPE ?= patch

# Targets for Release Workflow/Automation
.PHONY: release-pypi bump-version clean-dist build confirm-upload upload-pypi docs

release-pypi: clean-dist build upload docs

bump-version: ## Bump version (default: patch, options: patch, minor, major)
	@poetry version $(BUMP_TYPE)
	@echo "Bumped version"

clean-dist: ## Remove "volatile" directory dist
	@rm -rf dist
	@echo "Cleaned up dist directory"

build: ## Build the project and create the dist directory if it doesn't exist
	@mkdir -p dist
	@poetry build
	@echo "Built the project"

confirm-upload: ## Confirm before the irreversible zone
	@echo "Are you sure you want to upload to PyPI? (yes/no)"
	@read ans && [ $${ans:-no} = yes ]

upload-pypi: confirm-upload ## Upload to PyPI (ensure the token is present in .pypirc file before running upload)
	@twine upload dist/*$(VERSION)* --verbose
	@echo "Uploaded version $(VERSION) to PyPI"
	
docs: ## Update docs site
	@mkdocs gh-deploy
	@echo "Deployed docs"
