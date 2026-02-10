.PHONY: help setup install install-dev format lint check clean server mcp frontend test

# Variables
PYTHON := python3
PIP := pip
VENV := .venv
VENV_BIN := $(VENV)/bin
PYTHON_VENV := $(VENV_BIN)/python
PIP_VENV := $(VENV_BIN)/pip
BLACK := $(VENV_BIN)/black
RUFF := $(VENV_BIN)/ruff
UVICORN := $(VENV_BIN)/uvicorn
STREAMLIT := $(VENV_BIN)/streamlit

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
NC := \033[0m # No Color

help: ## Show this help message
	@echo "$(BLUE)Surf Forecast - Available commands:$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-15s$(NC) %s\n", $$1, $$2}'
	@echo ""

setup: ## Setup project: create venv and install dependencies
	@echo "$(BLUE)Setting up project...$(NC)"
	@if [ ! -d "$(VENV)" ]; then \
		echo "$(BLUE)Creating virtual environment...$(NC)"; \
		$(PYTHON) -m venv $(VENV); \
		echo "$(GREEN)✓ Virtual environment created$(NC)"; \
	else \
		echo "$(YELLOW)Virtual environment already exists$(NC)"; \
	fi
	@echo "$(BLUE)Installing dependencies...$(NC)"
	$(VENV_BIN)/pip install --upgrade pip
	$(VENV_BIN)/pip install -r requirements.txt
	@echo "$(BLUE)Installing dev dependencies...$(NC)"
	$(VENV_BIN)/pip install black ruff
	@echo "$(GREEN)✓ Project setup complete!$(NC)"
	@echo "$(YELLOW)Activate venv: source $(VENV)/bin/activate$(NC)"
	@echo "$(YELLOW)Run 'make server' to start backend$(NC)"
	@echo "$(YELLOW)Run 'make frontend' to start frontend$(NC)"

install: ## Install dependencies
	@echo "$(BLUE)Installing dependencies...$(NC)"
	$(PIP) install -r requirements.txt
	@echo "$(GREEN)✓ Dependencies installed$(NC)"

install-dev: install ## Install dependencies including dev tools (black, ruff)
	@echo "$(BLUE)Installing dev dependencies...$(NC)"
	$(PIP) install black ruff
	@echo "$(GREEN)✓ Dev dependencies installed$(NC)"

venv: ## Create virtual environment
	@echo "$(BLUE)Creating virtual environment...$(NC)"
	@if [ ! -d "$(VENV)" ]; then \
		$(PYTHON) -m venv $(VENV); \
		echo "$(GREEN)✓ Virtual environment created$(NC)"; \
	else \
		echo "$(YELLOW)Virtual environment already exists$(NC)"; \
	fi
	@echo ""
	@echo "$(GREEN)To activate, run:$(NC)"
	@echo "$(YELLOW)  source $(VENV)/bin/activate$(NC)"
	@echo "$(YELLOW)  # or: source activate.sh$(NC)"
	@echo ""
	@echo "$(YELLOW)Note: Makefile commands run in subshells, so activation$(NC)"
	@echo "$(YELLOW)must be done manually in your terminal.$(NC)"

format: ## Format code with black
	@echo "$(BLUE)Formatting code with black...$(NC)"
	@if command -v black > /dev/null; then \
		black . --exclude="$(VENV)|.git|__pycache__|*.pyc"; \
	else \
		echo "$(YELLOW)black not found. Install with: make install-dev$(NC)"; \
		exit 1; \
	fi
	@echo "$(GREEN)✓ Code formatted$(NC)"

lint: ## Lint code with ruff
	@echo "$(BLUE)Linting code with ruff...$(NC)"
	@if command -v ruff > /dev/null; then \
		ruff check . --exclude="$(VENV)|.git|__pycache__"; \
	else \
		echo "$(YELLOW)ruff not found. Install with: make install-dev$(NC)"; \
		exit 1; \
	fi

check: format lint ## Format and lint code
	@echo "$(GREEN)✓ Code check complete$(NC)"

server: ## Run FastAPI backend server
	@echo "$(BLUE)Starting FastAPI server...$(NC)"
	@echo "$(YELLOW)API docs: http://localhost:8000/docs$(NC)"
	@echo "$(YELLOW)Health: http://localhost:8000/health$(NC)"
	uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

mcp: ## Run MCP server
	@echo "$(BLUE)Starting MCP server...$(NC)"
	$(PYTHON) server.py

frontend: ## Run Streamlit frontend
	@echo "$(BLUE)Starting Streamlit frontend...$(NC)"
	@echo "$(YELLOW)Frontend: http://localhost:8501$(NC)"
	streamlit run frontend/app.py --server.port 8501

test: ## Run tests (if available)
	@echo "$(BLUE)Running tests...$(NC)"
	@if [ -d "tests" ]; then \
		pytest tests/ -v; \
	else \
		echo "$(YELLOW)No tests directory found$(NC)"; \
	fi

clean: ## Clean cache and temporary files
	@echo "$(BLUE)Cleaning...$(NC)"
	find . -type d -name "__pycache__" -exec rm -r {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -r {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -r {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -r {} + 2>/dev/null || true
	@echo "$(GREEN)✓ Cleaned$(NC)"

clean-all: clean ## Clean everything including virtual environment
	@echo "$(BLUE)Removing virtual environment...$(NC)"
	rm -rf $(VENV)
	@echo "$(GREEN)✓ All cleaned$(NC)"

dev: install-dev ## Setup development environment
	@echo "$(GREEN)✓ Development environment ready$(NC)"
	@echo "$(YELLOW)Run 'make format' to format code$(NC)"
	@echo "$(YELLOW)Run 'make server' to start backend$(NC)"
	@echo "$(YELLOW)Run 'make frontend' to start frontend$(NC)"

.DEFAULT_GOAL := help
