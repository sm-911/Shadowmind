# Contributing to ShadowMind

Thank you for your interest in contributing! This guide explains how to set up the project, run tests, add new features, and submit pull requests.

---

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Getting Started](#getting-started)
3. [Project Structure](#project-structure)
4. [Adding a New Attack Script](#adding-a-new-attack-script)
5. [Running Tests](#running-tests)
6. [Code Style](#code-style)
7. [Submitting a Pull Request](#submitting-a-pull-request)

---

## Prerequisites

- Python 3.10+
- Git
- (Optional) A Cloudflare tunnel URL for remote demo testing

---

## Getting Started

```bash
# 1. Fork the repo and clone your fork
git clone https://github.com/<your-username>/Shadowmind.git
cd Shadowmind

# 2. Create a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 3. Install in editable mode with dev extras
pip install -e ".[dev]"
```

---

## Project Structure

```
Shadowmind/
├── attack_runner.py         # Unified attack simulation script
├── proxy.py                 # Multi-hop proxy relay
├── main.py                  # Application entry point
├── configs/
│   ├── attack_config.yaml   # Attack runner configuration
│   └── thresholds.yaml      # Detection thresholds
├── src/
│   ├── detection/           # CNN, LSTM, MLP, GNN models
│   ├── data/                # Data generators and preprocessors
│   ├── honeypot/            # Decoy managers and interaction logs
│   ├── intelligence/        # Profiler and reporter
│   └── vault/               # AES vault, key rotation, TTL destruct
├── ui/
│   └── tabs/                # Dashboard, honeypot, settings, vault tabs
├── tests/                   # pytest test suite
├── docs/                    # Reports and academic documentation
├── notebooks/               # Jupyter notebooks (CNN/LSTM/GNN demos)
└── website/                 # Landing page (HTML/CSS)
```

---

## Adding a New Attack Script

Instead of creating a standalone script, **add a new mode to `attack_runner.py`**:

1. Write a function `run_<yourmode>(base_url, paths, ...)` following the pattern of `run_parallel` or `run_serial`.
2. Add `"<yourmode>"` to the `--mode` choices in `parse_args`.
3. Add a branch in `main()` to call your function.
4. Add a corresponding YAML key in `configs/attack_config.yaml` for any new parameters.
5. Write unit tests in `tests/test_attack_runner.py`.

---

## Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run a specific test file
pytest tests/test_attack_runner.py -v

# Run with coverage
pip install pytest-cov
pytest tests/ --cov=. --cov-report=term-missing
```

---

## Code Style

This project uses:
- **black** (line length 100) for formatting
- **flake8** for linting
- **logging** module instead of bare `print` statements

```bash
# Format all code
black --line-length 100 attack_runner.py proxy.py src/ tests/

# Lint
flake8 . --max-line-length=100 --exclude=.git,__pycache__,notebooks,website
```

---

## Submitting a Pull Request

1. Create a descriptive branch name: `feature/add-udp-mode`, `fix/proxy-timeout`, etc.
2. Make your changes and add/update tests.
3. Ensure `pytest` and `flake8` pass locally.
4. Push your branch and open a PR against `main` in the **upstream** (`Sourya-Dey05/Shadowmind`) repo.
5. Fill in the PR template describing **what** changed and **why**.
6. Request a review from at least one maintainer.

---

Thank you for contributing! 🛡️
