PYTHON := python3
PIP := $(PYTHON) -m pip
PYTEST := $(PYTHON) -m pytest
APP_DIR := .
DOCKER_IMAGE := bibibool/flask-api

.PHONY: lint test build

lint: ## Install dependencies
	ruff check $(APP_DIR)
	bandit -r $(APP_DIR) -ll

test: ## Run tests with coverage
	$(PYTEST) 

build: ## Build the production Docker image
	docker build -t $(DOCKER_IMAGE):latest .

clean: ## Remove temporary files.
	rm -rf .pytest_cache .coverage htmlcov
	find . -type d -name "__pycache__" -exec rm -rf {} +