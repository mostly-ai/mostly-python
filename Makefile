# Internal Variables
PUBLIC_API_FULL_URL = https://raw.githubusercontent.com/mostly-ai/mostly-openapi/refs/heads/main/public-api.yaml
PUBLIC_API_OUTPUT_PATH = mostlyai/client/model.py

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

# Default files to update
PYPROJECT_TOML = pyproject.toml
INIT_FILE = mostlyai/__init__.py

# Internal Variables for Release Workflow
BUMP_TYPE ?= patch
CURRENT_VERSION := $(shell grep -m 1 'version = ' $(PYPROJECT_TOML) | sed -e 's/version = "\(.*\)"/\1/')
# Assuming current_version is already set from pyproject.toml
NEW_VERSION := $(shell echo $(CURRENT_VERSION) | awk -F. -v bump=$(BUMP_TYPE) '{ \
    if (bump == "patch") { \
        printf("%d.%d.%d", $$1, $$2, $$3 + 1); \
    } else if (bump == "minor") { \
        printf("%d.%d.0", $$1, $$2 + 1); \
    } else if (bump == "major") { \
        printf("%d.0.0", $$1 + 1); \
    } else { \
        print "Error: Invalid BUMP_TYPE. Expected patch, minor or major. Input was BUMP_TYPE=" bump; \
        exit 1; \
    } \
}')


# Targets for Release Workflow/Automation
.PHONY: update-version-gh release-pypi docs

update-version-gh: pull-main bump-version update-vars-version create-branch ## Update version in GitHub: pull main, bump version, create and push the new branch

release-pypi: clean-dist pull-main build upload docs  ## Release to PyPI: pull main, build and upload to PyPI

pull-main: # Pull main branch
	# stash changes
	@git stash
	# switch to main branch
	@git checkout main
	# fetch latest changes
	@git fetch origin main
	# get a clean copy of main branch
	@git reset --hard origin/main
	# clean
	@git clean -fdX

bump-version: # Bump version (default: patch, options: patch, minor, major)
	@echo "Bumping $(BUMP_TYPE) version from $(CURRENT_VERSION) to $(NEW_VERSION)"
	@echo "Replaces $(CURRENT_VERSION) to $(NEW_VERSION) in $(PYPROJECT_TOML)"
	@echo "Replaces $(CURRENT_VERSION) to $(NEW_VERSION) in $(INIT_FILE)"
	@echo "Current directory: $(shell pwd)"
    # Check if current version was found
	@if [ -z "$(CURRENT_VERSION)" ]; then \
        echo "Error: Could not find current version in $(PYPROJECT_TOML)"; \
        exit 1; \
    fi
    # Replace the version in pyproject.toml
	@if [[ "$(shell uname -s)" == "Darwin" ]]; then \
        sed -i '' 's/version = "$(CURRENT_VERSION)"/version = "$(NEW_VERSION)"/g' $(PYPROJECT_TOML); \
        sed -i '' 's/__version__ = "$(CURRENT_VERSION)"/__version__ = "$(NEW_VERSION)"/g' $(INIT_FILE); \
    else \
        sed -i 's/version = "$(CURRENT_VERSION)"/version = "$(NEW_VERSION)"/g' $(PYPROJECT_TOML); \
        sed -i 's/__version__ = "$(CURRENT_VERSION)"/__version__ = "$(NEW_VERSION)"/g' $(INIT_FILE); \
    fi

update-vars-version: # Update the required variables after bump
	$(eval VERSION := $(shell poetry version -s))
	$(eval BRANCH := verbump_$(shell echo $(VERSION) | tr '.' '_'))
	$(eval TAG := $(VERSION))
	@echo "Updated VERSION to $(VERSION), BRANCH to $(BRANCH), TAG to $(TAG)"

create-branch: # Create verbump_{new_ver} branch
	@git checkout -b $(BRANCH)
	@echo "Created branch $(BRANCH)"
	# commit the version bump
	@git add $(INIT_FILE)
	@git add $(PYPROJECT_TOML)
	@git commit -m "Version Bump to $(VERSION)"
	@echo "Committed version bump to $(VERSION)"
	@git push --set-upstream origin $(BRANCH)
	@echo "Pushed branch $(BRANCH) to origin"

clean-dist: # Remove "volatile" directory dist
	@rm -rf dist
	@echo "Cleaned up dist directory"

build: # Build the project and create the dist directory if it doesn't exist
	@mkdir -p dist
	@poetry build
	@echo "Built the project"
	@twine check --strict dist/*
	@echo "Project is checked"	

confirm-upload: # Confirm before the irreversible zone
	@echo "Are you sure you want to upload to PyPI? (yes/no)"
	@read ans && [ $${ans:-no} = yes ]

upload-pypi: confirm-upload # Upload to PyPI (ensure the token is present in .pypirc file before running upload)
	@twine upload dist/*$(VERSION)* --verbose
	@echo "Uploaded version $(VERSION) to PyPI"
	
docs: ## Update docs site
	@mkdocs gh-deploy
	@echo "Deployed docs"
