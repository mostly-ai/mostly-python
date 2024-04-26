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
