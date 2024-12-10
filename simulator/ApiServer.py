"""Simple HTTP Server to simulate the MySmartBike API."""
from __future__ import annotations

from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import os
import sys
from urllib.parse import urlparse

HTTP_SERVER_IP = "0.0.0.0"
HTTP_SERVER_PORT = 8001
LOGGER = logging.getLogger(__package__)

CHAOS_MONKEY = False

class MySmartBikeSimulatorServer(BaseHTTPRequestHandler):
    """Simple HTTP Server to simulate the MySmartBike API."""

    def do_GET(self):
        """Answer get requests."""

        if not CHAOS_MONKEY:
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
                if "list_mode=MAP" in parsed.query:
                    if os.path.isfile("./api/v1/objects/.map-200-dev"):
                        with open("./api/v1/objects/.map-200-dev", "rb") as file:
                            self.wfile.write(file.read())  # Read the file and send the contents
                    else:
                        with open("./api/v1/objects/map-200", "rb") as file:
                            self.wfile.write(file.read())  # Read the file and send the contents
                    return

                if os.path.isfile("./api/v1/objects/.me-200-dev"):
                    with open("./api/v1/objects/.me-200-dev", "rb") as file:
                        self.wfile.write(file.read())  # Read the file and send the contents
                else:
                    with open("./api/v1/objects/me-200", "rb") as file:
                        self.wfile.write(file.read())  # Read the file and send the contents
                return
            LOGGER.debug("Unknown request path: %s", self.path)
        else:
            self.send_error(504, "Gateway not available")

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
    webServer = HTTPServer((HTTP_SERVER_IP, HTTP_SERVER_PORT), MySmartBikeSimulatorServer)
    set_logger()
    LOGGER.debug("Server started http://%s:%s", HTTP_SERVER_IP, HTTP_SERVER_PORT)

    webServer.serve_forever()

    webServer.server_close()
    LOGGER.debug("Server stopped.")
