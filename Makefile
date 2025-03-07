# Makefile for Assignment 2

# Variables
PYTHON = python
TEST_FILE = tests/test_lab2.py

# Default target
all: grade-lab2

# Run tests for Assignment 2
grade-lab2:
	$(PYTHON) -m pytest $(TEST_FILE)

# Clean up temporary files
clean:
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf test_logs.json