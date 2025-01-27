.PHONY: help
help: ## Help for usage
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

act-pr: ## Run github actions locally
	act pull_request

lint: ## Lining
	pre-commit run -a

tests: ## Run pytest
	pytest -n auto -v --capture=sys -x --tb=long
