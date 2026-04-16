#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import socket


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        node_id = os.getenv("NODE_ID", "unknown")
        hostname = socket.gethostname()
        pod_ip = socket.gethostbyname(hostname)

        body = (
            f"NODE_ID  : {node_id}\n"
            f"HOSTNAME : {hostname}\n"
            f"POD_IP   : {pod_ip}\n"
        )
        encoded = body.encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def log_message(self, format, *args):
        return


def main() -> None:
    port = int(os.getenv("PORT", "8000"))
    server = HTTPServer(("0.0.0.0", port), Handler)
    print(f"node-id-app listening on 0.0.0.0:{port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
