.DEFAULT_GOAL := help

.PHONY: help
help:  ## Show this help.
	@grep -E '^\S+:.*?## .*$$' $(firstword $(MAKEFILE_LIST)) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "%-30s %s\n", $$1, $$2}'

.PHONY: build
build: ## Build the docker image
	docker compose build

.PHONY: up
up: build ## Runs the app
	docker compose run --rm --remove-orphans --service-ports lift

.PHONY: add-package
add-package: ## Add package to the project ex: make add-package package=XX
	docker compose run --rm --no-deps lift poetry add $(package)
	make build

.PHONY: format
format: ## Run format
	docker compose run --rm --no-deps lift poetry run black src test

.PHONY: check-format
check-format: ## Check format
	docker compose run --rm --no-deps lift poetry run black --check src test

.PHONY: check-typing
check-typing: ## Check typing
	docker compose run --rm --no-deps lift poetry run mypy src test

.PHONY: test
test: ## Run tests
	docker compose run --rm lift poetry run pytest test -ra

.PHONY: test-coverage
test-coverage: ## Run tests coverage
	docker compose run --rm lift coverage run --branch -m pytest test
	docker compose run --rm lift coverage html
  @echo "You can open the coverage report here: htmlcov/index.html"

.PHONY: watch
watch: ## Watch tests
	docker compose run --rm lift poetry run ptw

.PHONY: local-setup
local-setup: ## Set up the local environment (e.g. install git hooks)
	scripts/local-setup.sh

.PHONY: pre-commit
pre-commit: check-format check-typing test
