#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
import os


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = (
            "Lab 8 Custom Docker App is running.\n"
        )
        encoded = body.encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)


def main() -> None:
    port = int(os.getenv("PORT", "8000"))
    server = HTTPServer(("0.0.0.0", port), Handler)
    print(f"Custom app listening on 0.0.0.0:{port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
