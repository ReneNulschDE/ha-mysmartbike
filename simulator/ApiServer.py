"""Simple HTTP Server to simulate the Link2Home API."""
from __future__ import annotations

from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import os
import sys
from urllib.parse import urlparse

HTTP_SERVER_IP = "0.0.0.0"
HTTP_SERVER_PORT = 8001
LOGGER = logging.getLogger(__package__)


class Link2HomeSimulatorServer(BaseHTTPRequestHandler):
    """Simple HTTP Server to simulate the Link2Home API."""

    def do_GET(self):
        """Answer get requests."""
        self.send_response(200)
        self.send_header("Content-type", "application/json;charset=UTF-8")
        self.end_headers()

        parsed = urlparse(self.path)
        if parsed.path == "/api/v1/users/login":
            if os.path.isfile("./api/v1/users/.login-200-dev"):
                with open("./api/v1/users/.login-200-dev", "rb") as file:
                    self.wfile.write(file.read())
            else:
                with open("./api/v1/users/login-200", "rb") as file:
                    self.wfile.write(file.read())
            return
        if parsed.path == "/api/v1/objects/me":
            if os.path.isfile("./api/v1/objects/.me-200-dev"):
                with open("./api/v1/objects/.me-200-dev", "rb") as file:
                    self.wfile.write(file.read())  # Read the file and send the contents
            else:
                with open("./api/v1/objects/me-200", "rb") as file:
                    self.wfile.write(file.read())  # Read the file and send the contents
            return
        LOGGER.debug("Unknown request path: %s", self.path)

    def do_POST(self):
        """Answer post requests."""
        self.do_GET()


def set_logger():
    """Set Logger properties."""

    fmt = "%(asctime)s.%(msecs)03d %(levelname)s (%(threadName)s) [%(name)s] %(message)s"
    LOGGER.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(fmt)
    handler.setFormatter(formatter)
    LOGGER.addHandler(handler)


if __name__ == "__main__":
    webServer = HTTPServer((HTTP_SERVER_IP, HTTP_SERVER_PORT), Link2HomeSimulatorServer)
    set_logger()
    LOGGER.debug("Server started http://%s:%s", HTTP_SERVER_IP, HTTP_SERVER_PORT)

    webServer.serve_forever()

    webServer.server_close()
    LOGGER.debug("Server stopped.")
