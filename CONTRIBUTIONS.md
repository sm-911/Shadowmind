# CONTRIBUTIONS — ShadowMind

This document tracks all additions and modifications made to the **`sm-911/Shadowmind`** fork (relative to the upstream `Sourya-Dey05/Shadowmind` repository), and what has been contributed back to the upstream via the **`improvements/code-quality-and-ci`** branch.

---

## Branch: `improvements/code-quality-and-ci`

> **Pushed to:** `sm-911/Shadowmind` and `Sourya-Dey05/Shadowmind`
> **Commit:** `770388b` — *improve: consolidate attack scripts, add CI, tests, packaging and contributing guide*
> **Date:** 13 Nov 2026

### New Files Added

| File | Description |
|------|-------------|
| `attack_runner.py` | Unified attack-simulation entry point that **replaces** all four separate scripts (`parallel_attack.py`, `parallel_native.py`, `serial_attack.py`, `serial_native.py`). Single configurable module with `--mode parallel/serial/multihop`, `--native`, `--workers`, and `--delay` flags. Uses the `logging` module (not bare `print`), validates target URLs against an allow-list, and reads defaults from `configs/attack_config.yaml`. |
| `configs/attack_config.yaml` | Central YAML configuration for the attack runner — target URL, thread count, serial delay, and vault paths. No code edits required to change targets or timing. |
| `tests/test_attack_runner.py` | `pytest` unit-test suite covering `validate_url`, `_hit_requests`, `_hit_native`, and `load_config` — all with mocked network calls (no live server needed). |
| `tests/test_proxy.py` | `pytest` unit tests for `proxy.py`'s `MultiHopProxyHandler.do_GET` — covers successful relay and 500-error code path. |
| `.github/workflows/ci.yml` | GitHub Actions CI pipeline. Runs `flake8` linter, `black --check` formatter check, and `pytest` on every push and pull request for Python 3.10 and 3.11. |
| `pyproject.toml` | Formal project packaging (`pip install -e ".[dev]"`), project metadata, dependency list, dev extras (`pytest`, `flake8`, `black`, `mypy`), and `[tool.black]` / `[tool.pytest.ini_options]` configuration. |
| `CONTRIBUTING.md` | Step-by-step contributor guide covering: project setup, virtual environment, project structure, how to add a new attack mode, running tests, code-style rules (black + flake8), and the pull-request workflow. |
| `Makefile` | Developer shortcut targets: `make install`, `make test`, `make lint`, `make format`, `make demo`, `make demo-url URL=...`, `make clean`. |

### Modified Files

| File | Change type | What changed |
|------|-------------|-------------|
| `README.md` | **Major rewrite** | Complete overhaul — added CI badge, updated project structure table (reflects new files), added "Attack Simulation Scripts" section documenting `attack_runner.py` usage and mode flags, added "Contributors" table crediting both authors, added "Technology Stack" table with testing/CI/packaging rows, improved "Testing" section with `pytest-cov` and Makefile commands, added "Contributing" section linking to `CONTRIBUTING.md`. |
| `CONTRIBUTIONS.md` | **New / Updated** | This file — tracks all branch changes and contributions for both repositories. |

---

## Earlier Changes (relative to upstream `main`)

> These were committed on **13 Nov 2026** and are present on `main` of the fork.

| File | Change type | Description |
|------|-------------|-------------|
| `parallel_attack.py` | Added | Parallel HTTP stress-test using `ThreadPoolExecutor` with configurable target URL, path list, latency measurement, and pretty-printed results. |
| `parallel_native.py` | Added | Zero-dependency parallel attack (standard-library only: `urllib.request` + `concurrent.futures`). |
| `serial_attack.py` | Added | Sequential (low-and-slow) attack script (single-threaded loop with 3-second delay between requests). |
| `serial_native.py` | Added | Zero-dependency sequential attack script (standard-library only). |
| `multihop_attack.py` | Added | Demo script for a multi-hop (HoneyGraph GNN) lateral-movement attack via a phone proxy device. |
| `proxy.py` | Modified | Added support for new Cloudflare tunnel URLs, added `SO_REUSEADDR` socket option, and improved startup and error logging. |
| `ui/tabs/dashboard_tab.py` | Modified | Added theme toggle, signal-detection filter mode, and "Last Exfiltration Audit" inspector; refreshed telemetry handling. |
| `docs/academic_novelty.md` | Added/Updated | Comprehensive literature-review table (13 studies) with detailed commentary on the academic novelty of the project. |
| `README.md` | Updated | New project title ("An Adaptive Cyber Defense System"), expanded introduction, architecture diagram, evaluation metrics (accuracy, precision, recall, F1-score, confusion matrix), detailed installation and setup instructions including standalone `.exe` guidance, and links to newly added attack scripts. |
| `requirements.txt` | Minor tweak | Updated dependency list to include packages required by the new scripts. |
| `.gitignore` | Minor tweak | Refreshed ignored paths (compiled executables, temporary logs). |

---

## Repositories & Branch Links

| Repository | Branch | Link |
|------------|--------|------|
| `sm-911/Shadowmind` (fork) | `improvements/code-quality-and-ci` | [View branch](https://github.com/sm-911/Shadowmind/tree/improvements/code-quality-and-ci) |
| `sm-911/Shadowmind` (fork) | `main` | [View main](https://github.com/sm-911/Shadowmind/tree/main) |
| `Sourya-Dey05/Shadowmind` (upstream) | `improvements/code-quality-and-ci` | [View branch](https://github.com/Sourya-Dey05/Shadowmind/tree/improvements/code-quality-and-ci) |

---

*Maintained by [@sm-911](https://github.com/sm-911)*
# Contribution Summary

| Path (relative) | Change type | Description |
|---|---|---|
| `parallel_attack.py` | Added | Parallel HTTP‑request stress‑test. |
| `parallel_native.py` | Added | Zero‑dependency parallel attack script. |
| `serial_attack.py` | Added | Sequential attack script. |
| `serial_native.py` | Added | Zero‑dependency sequential script. |
| `multihop_attack.py` | Added | Multi‑hop HoneyGraph GNN demo script. |
| `proxy.py` | Modified | Cloudflare tunnel support, `SO_REUSEADDR`, improved logging. |
| `ui/tabs/dashboard_tab.py` | Modified | Theme toggle, signal‑filter mode, “Last Exfiltration Audit” inspector, telemetry refresh. |
| `docs/academic_novelty.md` | Added/Updated | 13‑study literature‑review table + novelty commentary. |
| `README.md` | Updated | New title, expanded intro, architecture diagram, evaluation metrics, install/setup guide, links to new scripts. |
| `requirements.txt` | Minor tweak | Updated dependencies. |
| `.gitignore` | Minor tweak | Refreshed ignored paths. |
