.DEFAULT_GOAL := help

.PHONY: help
help:  ## Show this help.
	@grep -E '^\S+:.*?## .*$$' $(firstword $(MAKEFILE_LIST)) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "%-30s %s\n", $$1, $$2}'

.PHONY: build
build: ## Build the docker image
	docker compose build

.PHONY: add-package
add-package: ## Add package to the project ex: make add-package package=XX
	docker compose run --rm --no-deps lift poetry add $(package)
	make build

.PHONY: test
test: ## Run tests
	docker compose run --rm lift poetry run pytest test -ra

.PHONY: format
format: ## Run format
	docker compose run --rm --no-deps lift poetry run black src test

.PHONY: test-coverage
test-coverage: ## Run tests coverage
	docker compose run --rm lift coverage run --branch -m pytest test
	docker compose run --rm lift coverage html
  @echo "You can open the coverage report here: htmlcov/index.html"
