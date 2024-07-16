# Define variables for commands and paths
PYTHON = python3
PIP = pip
TESTS_DIR = tests
VENV_DIR = venv
REQUIREMENTS = requirements.txt
SETUP = setup.py

# Target to create a virtual environment
venv:
	$(PYTHON) -m venv $(VENV_DIR)
	@echo "Virtual environment created."

# Target to install core and development dependencies
install: venv
	$(VENV_DIR)/bin/$(PIP) install -r $(REQUIREMENTS)
	$(VENV_DIR)/bin/$(PIP) install .[dev]
	@echo "Dependencies installed."

# Target to run tests
test:
	$(VENV_DIR)/bin/pytest $(TESTS_DIR)
	@echo "Tests run."

# Target to lint the code
lint:
	$(VENV_DIR)/bin/flake8 rag/ tests/
	@echo "Code linted."

# Target to format the code
format:
	$(VENV_DIR)/bin/black rag/ tests/
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
	@echo "  venv       - Create a virtual environment"
	@echo "  install    - Install core and development dependencies"
	@echo "  test       - Run tests"
	@echo "  lint       - Lint the code"
	@echo "  format     - Format the code"
	@echo "  quality    - Run lint and format"
	@echo "  clean      - Clean up pyc files and caches"
	@echo "  help       - Display this help message"
