# Define variables for commands and paths
.PHONY: clean
PYTHON = python3
PIP = pip
TESTS_DIR = tests
REQUIREMENTS = requirements.txt
PACKAGE_NAME = horiana-rag

# Target to install core and development dependencies
install:
	$(PIP) install -r $(REQUIREMENTS)
	@echo "Dependencies installed."

# Target to run tests
test:
	pytest $(TESTS_DIR) # add -s for verbose
	@echo "Tests run."

# Target to lint the code
lint:
	-flake8 --config=.flake8 rag/ tests/
	@echo "Code linted."

# Target to format the code
format:
	black rag/ tests/
	@echo "Code formatted."

# Target to check code quality
quality: lint format

# Target to clean up pyc files and caches
clean:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete
	@echo "Cleaned up."

# Target to display the help message
help:
	@echo "Makefile commands:"
	@echo "  install    - Install core and development dependencies"
	@echo "  test       - Run tests"
	@echo "  lint       - Lint the code"
	@echo "  format     - Format the code"
	@echo "  quality    - Run lint and format"
	@echo "  clean      - Clean up pyc files and caches"
	@echo "  help       - Display this help message"
