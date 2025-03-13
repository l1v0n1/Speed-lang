.PHONY: install test clean build

install:
	./install.sh

test:
	pytest

clean:
	rm -rf build/ dist/ *.egg-info/ .pytest_cache/ .coverage
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build:
	python setup.py build

# Development targets
lint:
	black .
	mypy .

# Example targets
examples: build
	speed examples/hello.speed -o hello
	speed examples/async_network.speed -o network

# Run examples
run-hello: examples
	./hello

run-network: examples
	./network 