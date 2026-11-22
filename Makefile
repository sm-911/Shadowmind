# =============================================================================
# FILE: Makefile
# PURPOSE: One-command shortcuts for common development tasks.
# USAGE:
#   make install    — install all dependencies
#   make test       — run the pytest suite
#   make lint       — run flake8 linter
#   make format     — auto-format with black
#   make demo       — run the attack demo against a local server
#   make demo-url   — run demo against a custom URL (URL=http://... make demo-url)
# =============================================================================

PYTHON   := python
PIP      := pip
PYTEST   := pytest
BLACK    := black
FLAKE8   := flake8
LINE_LEN := 100
SRC_DIRS := attack_runner.py proxy.py src/ tests/

.PHONY: install test lint format demo demo-url clean help

help:
	@echo ""
	@echo "  ShadowMind — available make targets"
	@echo "  ------------------------------------"
	@echo "  install    Install all project dependencies"
	@echo "  test       Run the full pytest suite"
	@echo "  lint       Run flake8 linter"
	@echo "  format     Auto-format code with black"
	@echo "  demo       Run parallel attack demo (default local URL)"
	@echo "  demo-url   Run parallel attack demo against URL=<your-url>"
	@echo "  clean      Remove __pycache__ and .pytest_cache"
	@echo ""

install:
	$(PIP) install -e ".[dev]"

test:
	$(PYTEST) tests/ -v --tb=short

lint:
	$(FLAKE8) . --max-line-length=$(LINE_LEN) --exclude=.git,__pycache__,notebooks,website

format:
	$(BLACK) --line-length $(LINE_LEN) $(SRC_DIRS)

demo:
	$(PYTHON) attack_runner.py --mode parallel

demo-url:
	$(PYTHON) attack_runner.py --mode parallel --url $(URL)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache htmlcov .coverage
