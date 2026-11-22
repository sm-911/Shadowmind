# =============================================================================
# FILE: tests/test_proxy.py
# PURPOSE: Unit tests for proxy.py using pytest.
# RUN:   pytest tests/test_proxy.py -v
# =============================================================================

from unittest.mock import MagicMock, patch


class TestMultiHopProxyHandler:
    """Tests for MultiHopProxyHandler.do_GET."""

    def _make_handler(self):
        """Instantiate handler with mocked socket/server."""
        from proxy import MultiHopProxyHandler

        handler = MultiHopProxyHandler.__new__(MultiHopProxyHandler)
        handler.path = "/vault/test"
        handler.client_address = ("10.0.0.1", 1234)
        handler.wfile = MagicMock()
        handler.send_response = MagicMock()
        handler.end_headers = MagicMock()
        return handler

    def test_relay_success(self):
        handler = self._make_handler()
        mock_resp = MagicMock()
        mock_resp.__enter__ = lambda s: s
        mock_resp.__exit__ = MagicMock(return_value=False)
        mock_resp.status = 200
        mock_resp.read.return_value = b"vaultdata"

        with patch("urllib.request.urlopen", return_value=mock_resp):
            handler.do_GET()

        handler.send_response.assert_called_once_with(200)
        handler.wfile.write.assert_called_once_with(b"vaultdata")

    def test_relay_error_returns_500(self):
        handler = self._make_handler()
        with patch("urllib.request.urlopen", side_effect=Exception("timeout")):
            handler.do_GET()

        handler.send_response.assert_called_once_with(500)
