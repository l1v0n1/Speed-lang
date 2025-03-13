#!/bin/bash

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install the package in development mode
pip install -e .

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

echo "Speed compiler installed successfully!"
echo "To use the compiler, make sure to activate the virtual environment:"
echo "source .venv/bin/activate"
echo "Then you can use the 'speed' command to compile Speed programs." 