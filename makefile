.PHONY: build run test test-cov clean help

IMAGE     = equal-sum-pairs
ARGS      ?=

help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

build:  ## Build the Docker image
	docker build --target runtime -t $(IMAGE) .

run: build  ## Run with default examples (or pass ARGS="1 2 3 4")
	docker run --rm $(IMAGE) $(ARGS)

test:  ## Run test suite inside Docker
	docker build --target test -t $(IMAGE)-test .

test-local:  ## Run test suite locally (requires: pip install -r requirements.txt)
	pytest test_equal_sum_pairs.py -v

test-cov:  ## Run tests with coverage report locally
	pytest test_equal_sum_pairs.py -v --cov=equal_sum_pairs --cov-report=term-missing

clean:  ## Remove Docker images
	docker rmi -f $(IMAGE) $(IMAGE)-test 2>/dev/null || true