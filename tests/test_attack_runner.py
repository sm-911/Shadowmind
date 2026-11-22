# =============================================================================
# FILE: tests/test_attack_runner.py
# PURPOSE: Unit tests for attack_runner.py using pytest.
# RUN:   pytest tests/test_attack_runner.py -v
# =============================================================================

import sys
import types
import pytest
from unittest.mock import patch, MagicMock

# ---------------------------------------------------------------------------
# Helpers — mock the `requests` library so tests run without network
# ---------------------------------------------------------------------------
def _make_mock_response(status_code=200, content=b"ok"):
    resp = MagicMock()
    resp.status_code = status_code
    resp.content = content
    return resp


# ---------------------------------------------------------------------------
# validate_url
# ---------------------------------------------------------------------------
class TestValidateUrl:
    def test_accepts_http(self):
        from attack_runner import validate_url
        assert validate_url("http://example.com") == "http://example.com"

    def test_accepts_https(self):
        from attack_runner import validate_url
        assert validate_url("https://example.com") == "https://example.com"

    def test_rejects_ftp(self):
        from attack_runner import validate_url
        with pytest.raises(SystemExit):
            validate_url("ftp://evil.com")

    def test_rejects_bare_hostname(self):
        from attack_runner import validate_url
        with pytest.raises(SystemExit):
            validate_url("evil.com/path")


# ---------------------------------------------------------------------------
# _hit_requests (mocked network)
# ---------------------------------------------------------------------------
class TestHitRequests:
    def test_successful_hit(self):
        mock_resp = _make_mock_response(200, b"hello")
        with patch("requests.get", return_value=mock_resp):
            from attack_runner import _hit_requests
            result = _hit_requests("http://target:8080", "/vault/test")
        assert "HIT" in result
        assert "200" in result

    def test_connection_error(self):
        with patch("requests.get", side_effect=ConnectionError("refused")):
            from attack_runner import _hit_requests
            result = _hit_requests("http://target:8080", "/vault/test")
        assert "MISS" in result
        assert "refused" in result


# ---------------------------------------------------------------------------
# _hit_native (mocked urllib)
# ---------------------------------------------------------------------------
class TestHitNative:
    def test_successful_hit(self):
        mock_resp = MagicMock()
        mock_resp.__enter__ = lambda s: s
        mock_resp.__exit__ = MagicMock(return_value=False)
        mock_resp.read.return_value = b"data"
        mock_resp.status = 200

        with patch("urllib.request.urlopen", return_value=mock_resp):
            from attack_runner import _hit_native
            result = _hit_native("http://target:8080", "/vault/test")
        assert "HIT" in result

    def test_http_error(self):
        import urllib.error
        with patch("urllib.request.urlopen", side_effect=urllib.error.HTTPError(
                url="", code=403, msg="Forbidden", hdrs=None, fp=None)):
            from attack_runner import _hit_native
            result = _hit_native("http://target:8080", "/vault/secret")
        assert "MISS" in result
        assert "403" in result


# ---------------------------------------------------------------------------
# load_config
# ---------------------------------------------------------------------------
class TestLoadConfig:
    def test_returns_dict_when_file_missing(self, tmp_path, monkeypatch):
        monkeypatch.setattr("attack_runner.CONFIG_PATH", tmp_path / "nonexistent.yaml")
        from attack_runner import load_config
        cfg = load_config()
        assert isinstance(cfg, dict)

    def test_reads_yaml_values(self, tmp_path, monkeypatch):
        cfg_file = tmp_path / "attack_config.yaml"
        cfg_file.write_text("target_url: http://test:9000\nworkers: 3\n")
        monkeypatch.setattr("attack_runner.CONFIG_PATH", cfg_file)
        from attack_runner import load_config
        cfg = load_config()
        assert cfg["target_url"] == "http://test:9000"
        assert cfg["workers"] == 3
