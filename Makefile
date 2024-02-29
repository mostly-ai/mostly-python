# External Environment Variables
GH_TOKEN ?= YourSecureToken
PUBLIC_OPENAPI_FILE ?= /path/to/metadata/openapi.yaml
MOSTLY_PYTHON_REPO_PATH ?= /path/to/mostly-python

# Internal Variables
PUBLIC_OPENAPI_YAML_URL = https://raw.githubusercontent.com/mostly-ai/mostly-app-v2/dev/public-api/public-api.yaml?token=
PUBLIC_API_OUTPUT_PATH = mostlyai/model.py
PUBLIC_API_FULL_URL = $(PUBLIC_OPENAPI_YAML_URL)$(GH_TOKEN)

# .public file location
PUBLIC_FILE := .public

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
	--custom-template-dir custom_template

.PHONY: copy_public_files
copy_public_files:
	@# Check if MOSTLY_PYTHON_REPO_PATH is set
	@if [ -z "$(MOSTLY_PYTHON_REPO_PATH)" ]; then \
		echo "MOSTLY_PYTHON_REPO_PATH is not set. Set the environment variable to the destination path."; \
		exit 1; \
	fi

	@# Check if .public file exists
	@if [ ! -f "$(PUBLIC_FILE)" ]; then \
		echo "The .public file does not exist."; \
		exit 1; \
	fi

	# Read each line from .public file and copy the files/directories
	@while IFS= read -r line || [[ -n "$$line" ]]; do \
		[[ $$line = \#* ]] || [[ -z $$line ]] && continue; \
		if [ -d "$$line" ]; then \
			mkdir -p "$(MOSTLY_PYTHON_REPO_PATH)/$$line"; \
			cp -r "$$line/." "$(MOSTLY_PYTHON_REPO_PATH)/$$line"; \
		else \
			cp "$$line" "$(MOSTLY_PYTHON_REPO_PATH)/$$line"; \
		fi; \
	done < "$(PUBLIC_FILE)"

	@echo "Files copied successfully to $(MOSTLY_PYTHON_REPO_PATH)"
