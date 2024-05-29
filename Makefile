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
BUMP_TYPE ?= patch

# Targets for Release Workflow/Automation
.PHONY: release bump-version update-version create-branch commit-tag changelog push-changes update-main re-tag build upload confirm-upload clean-dist delete-branch

release: bump-version update-version create-branch commit-tag changelog push-changes update-main re-tag build upload confirm-upload clean-dist delete-branch

bump-version: ## Bump version (default: patch, options: patch, minor, major)
	@poetry version $(BUMP_TYPE)
	@echo "Bumped version"

update-version: ## Update the required variables after bump
	$(eval VERSION := $(shell poetry version -s))
	$(eval BRANCH := verbump_$(shell echo $(VERSION) | tr '.' '_'))
	$(eval TAG := $(VERSION))
	@echo "Updated VERSION to $(VERSION), BRANCH to $(BRANCH), TAG to $(TAG)"

create-branch: ## Create verbump_{new_ver} branch
	@git checkout -b $(BRANCH)
	@echo "Created branch $(BRANCH)"

commit-tag: ## Commit version bump, so that it's visible to commitizen
	@git add pyproject.toml
	@git add mostlyai/__init__.py
	# In case of other expectedly changed files to be included, add here
	@git commit -m "bump: to $(VERSION)"
	@git tag $(TAG)
	@echo "Tag $(TAG) created"

changelog: ## Update CHANGELOG.md and commit
	@cz ch --incremental
	@git add CHANGELOG.md
	@git commit -m "bump(changelog): update to $(VERSION)"
	@echo "Changelog updated"

push-changes: ## Push to version bump branch
	@git push origin $(BRANCH)
	@echo "Pushed changes to $(BRANCH) branch"
	
update-main: ## Merge the current branch into main and push changes to origin
	@git checkout main
	@git merge --squash $(BRANCH)
	@git commit -m "bump: to $(VERSION)"
	@git push origin main
	@echo "Merged $(BRANCH) into main and pushed changes"

re-tag:  ## Correct the new version tag on main
	@git tag -d $(TAG)
	@git tag $(TAG)
	@git push origin $(TAG)
	@echo "Re-tagged and pushed $(TAG)"

build: ## Build the project and create the dist directory if it doesn't exist
	@mkdir -p dist
	@poetry build
	@echo "Built the project"

confirm-upload: ## Confirm before the irreversible zone
	@echo "Are you sure you want to upload to PyPI? (yes/no)"
	@read ans && [ $${ans:-no} = yes ]

upload: confirm-upload  # Upload to PyPI
    # Ensure the token is present in .pypirc file before running upload
	@twine upload dist/*$(VERSION)* --verbose
	@echo "Uploaded version $(VERSION) to PyPI"
	
clean-dist: ## Remove "volatile" directory dist
	@rm -rf dist
	@echo "Cleaned up dist directory"
	
delete-branch: ## Delete the branch both locally and remotely
	@git branch -D $(BRANCH)
	@git push origin --delete $(BRANCH)
	@echo "Deleted branch $(BRANCH) locally and remotely"