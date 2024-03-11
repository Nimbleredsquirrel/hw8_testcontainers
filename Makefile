.DEFAULT_GOAL := help
PYTHONPATH = PYTHONPATH=./
TEST = $(PYTHONPATH) pytest --verbosity=2 --showlocals --log-level=DEBUG --strict-markers $(arg)
CODE = app tests

.PHONY: help
help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: test
#test: ## Runs pytest with coverage
	#$(TEST)

#.PHONY: test-fast
#test-fast: ## Runs pytest with exitfirst
#	$(TEST) --exitfirst

#.PHONY: test-failed
#test-failed: ## Runs pytest from last-failed
#	$(TEST) --last-failed

#.PHONY: test-cov
#test-cov: ## Runs pytest with coverage report
#	$(TEST) --cov --cov-report html

.PHONY: lint
lint: ## Lint code
	black --check $(CODE)
	flake8 --jobs 4 --statistics --show-source --ignore E501,W503,E203 $(CODE)
	pylint $(CODE)
	mypy --namespace-packages --ignore-missing-imports --explicit-package-bases $(CODE)
#	pytest --dead-fixtures --dup-fixtures
#	safety check --full-report
#	bandit -c pyproject.toml -r $(CODE)
	poetry check

.PHONY: format
format: ## Formats all files
	autoflake --recursive --in-place --ignore-init-module-imports --remove-all-unused-imports $(CODE)
	isort $(CODE)
	black $(CODE)

.PHONY: check
check: format lint #test ## Format and lint code then run tests
