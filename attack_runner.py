# =============================================================================
# FILE: attack_runner.py
# PURPOSE: Unified, configurable attack simulation script.
#          Consolidates parallel_attack.py, parallel_native.py,
#          serial_attack.py, and serial_native.py into one parameterised module.
#
# USAGE:
#   python attack_runner.py --mode parallel   [--url http://HOST:PORT] [--native]
#   python attack_runner.py --mode serial     [--url http://HOST:PORT] [--native]
#   python attack_runner.py --mode multihop   [--url http://HOST:PORT]
#
# FLAGS:
#   --mode      parallel | serial | multihop  (required)
#   --url       target base URL               (default: from config.yaml)
#   --native    use stdlib only (no requests) (optional flag)
#   --workers   thread count for parallel     (default: 6)
#   --delay     seconds between serial reqs   (default: 3)
# =============================================================================

import argparse
import concurrent.futures
import logging
import sys
import time
import yaml
from pathlib import Path

# ---------------------------------------------------------------------------
# Logging setup – replaces bare print statements
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("attack_runner")

# ---------------------------------------------------------------------------
# Config loading
# ---------------------------------------------------------------------------
CONFIG_PATH = Path(__file__).parent / "configs" / "attack_config.yaml"


def load_config() -> dict:
    """Load attack configuration from YAML file."""
    if CONFIG_PATH.exists():
        with CONFIG_PATH.open() as f:
            return yaml.safe_load(f) or {}
    return {}


# ---------------------------------------------------------------------------
# Shared target data
# ---------------------------------------------------------------------------
DEFAULT_PATHS = [
    "/vault/credentials.env.enc",
    "/vault/customer_database_dump.sql",
    "/vault/source_code.zip",
    "/vault/aws_production_keys.env",
    "/vault/internal_network_topology.txt",
    "/vault/executive_payroll_salaries.pdf",
]

ALLOWED_URL_PREFIXES = ("http://", "https://")


def validate_url(url: str) -> str:
    """Ensure the target URL starts with http:// or https:// to prevent misuse."""
    if not any(url.startswith(p) for p in ALLOWED_URL_PREFIXES):
        log.error("TARGET_URL must start with http:// or https://. Aborting.")
        sys.exit(1)
    return url


# ---------------------------------------------------------------------------
# Single-request helpers
# ---------------------------------------------------------------------------
def _hit_requests(base_url: str, path: str) -> str:
    """Make one GET request using the `requests` library."""
    import requests  # optional dependency
    url = f"{base_url.rstrip('/')}{path}"
    try:
        start = time.time()
        resp = requests.get(url, timeout=5)
        ms = (time.time() - start) * 1000
        return f"HIT  {path}  status={resp.status_code}  bytes={len(resp.content)}  {ms:.1f}ms"
    except Exception as exc:
        return f"MISS {path}  error={exc}"


def _hit_native(base_url: str, path: str) -> str:
    """Make one GET request using stdlib urllib only (zero external deps)."""
    import urllib.request
    import urllib.error
    url = f"{base_url.rstrip('/')}{path}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "ShadowMind-AttackRunner/1.0"})
        start = time.time()
        with urllib.request.urlopen(req, timeout=5) as resp:
            body = resp.read()
            ms = (time.time() - start) * 1000
            return f"HIT  {path}  status={resp.status}  bytes={len(body)}  {ms:.1f}ms"
    except urllib.error.HTTPError as exc:
        return f"MISS {path}  http_error={exc.code}"
    except Exception as exc:
        return f"MISS {path}  error={exc}"


# ---------------------------------------------------------------------------
# Attack modes
# ---------------------------------------------------------------------------
def run_parallel(base_url: str, paths: list, workers: int, native: bool) -> None:
    """Launch all requests simultaneously using a thread pool."""
    hit = _hit_native if native else _hit_requests
    label = "NATIVE PARALLEL" if native else "PARALLEL"
    log.info("Starting %s attack → %s  (workers=%d)", label, base_url, workers)
    log.info("=" * 60)

    t0 = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(hit, base_url, p): p for p in paths}
        for fut in concurrent.futures.as_completed(futures):
            log.info("  %s", fut.result())

    elapsed = (time.time() - t0) * 1000
    log.info("=" * 60)
    log.info("%s attack complete in %.2f ms", label, elapsed)
    log.info("Check dashboard for GNN topology alert and auto-encryption.")


def run_serial(base_url: str, paths: list, delay: float, native: bool) -> None:
    """Send requests one after another with a configurable delay."""
    hit = _hit_native if native else _hit_requests
    label = "NATIVE SERIAL" if native else "SERIAL"
    log.info("Starting %s attack → %s  (delay=%.1fs)", label, base_url, delay)
    log.info("=" * 60)

    for i, path in enumerate(paths, 1):
        log.info("[%d/%d] %s", i, len(paths), hit(base_url, path))
        if i < len(paths):
            log.info("  Waiting %.1f s before next request…", delay)
            time.sleep(delay)

    log.info("=" * 60)
    log.info("%s attack complete.", label)
    log.info("Check dashboard for confirmed exfiltration and vault auto-encryption.")


def run_multihop(base_url: str, paths: list, native: bool) -> None:
    """Multi-hop demo: logs each hop before hitting the target."""
    hit = _hit_native if native else _hit_requests
    log.info("Starting MULTIHOP attack → %s", base_url)
    log.info("Simulating lateral movement: Phone1 → Phone2 (proxy) → Laptop vault")
    log.info("=" * 60)

    for path in paths:
        log.info("[HOP 3] Reaching target vault path: %s", path)
        log.info("  %s", hit(base_url, path))

    log.info("=" * 60)
    log.info("Multi-hop attack complete. Check HoneyGraph GNN for lateral-movement graph.")


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------
def parse_args(cfg: dict) -> argparse.Namespace:
    default_url = cfg.get("target_url", "http://192.168.29.250:8080")
    default_workers = cfg.get("workers", 6)
    default_delay = cfg.get("serial_delay", 3.0)
    default_paths = cfg.get("paths", DEFAULT_PATHS)

    parser = argparse.ArgumentParser(
        description="ShadowMind Unified Attack Simulation Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--mode", choices=["parallel", "serial", "multihop"],
                        required=True, help="Attack mode to run.")
    parser.add_argument("--url", default=default_url,
                        help="Target base URL (default from config.yaml).")
    parser.add_argument("--native", action="store_true",
                        help="Use stdlib only — no pip installs required.")
    parser.add_argument("--workers", type=int, default=default_workers,
                        help="Thread count for parallel mode.")
    parser.add_argument("--delay", type=float, default=default_delay,
                        help="Seconds between requests in serial mode.")
    # Expose paths list override via config only (not CLI) to keep things simple
    ns = parser.parse_args()
    ns.paths = default_paths
    return ns


def main() -> None:
    cfg = load_config()
    args = parse_args(cfg)
    target = validate_url(args.url)

    if args.mode == "parallel":
        run_parallel(target, args.paths, args.workers, args.native)
    elif args.mode == "serial":
        run_serial(target, args.paths, args.delay, args.native)
    elif args.mode == "multihop":
        run_multihop(target, args.paths, args.native)


if __name__ == "__main__":
    main()
