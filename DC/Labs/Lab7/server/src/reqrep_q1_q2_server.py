#!/usr/bin/env python3
import argparse
import json
import re

import zmq

TERMINATION_MESSAGE = "STOP_SERVER"


def transform_message(message: str) -> str:
    number_match = re.search(r"[-+]?\d+(?:\.\d+)?", message)
    if number_match:
        number_text = number_match.group(0)
        number = float(number_text)
        squared = number * number
        return f"SQUARE({number_text})={squared:g}"
    return message.upper()


def main() -> None:
    parser = argparse.ArgumentParser(description="Q1/Q2 REQ-REP server")
    parser.add_argument("--bind", default="tcp://*:5555", help="Bind endpoint")
    args = parser.parse_args()

    context = zmq.Context.instance()
    socket = context.socket(zmq.REP)
    socket.bind(args.bind)

    request_count = 0
    print(f"[Q1/Q2 Server] Listening on {args.bind}")
    print(f"[Q1/Q2 Server] Send '{TERMINATION_MESSAGE}' from client for graceful stop.")

    try:
        while True:
            message = socket.recv_string()

            if message == TERMINATION_MESSAGE:
                response = {
                    "request_count": request_count,
                    "input": message,
                    "transformed": "Server shutting down gracefully.",
                }
                socket.send_string(json.dumps(response))
                print("[Q1/Q2 Server] Termination message received. Exiting.")
                break

            request_count += 1
            transformed = transform_message(message)
            response = {
                "request_count": request_count,
                "input": message,
                "transformed": transformed,
            }
            socket.send_string(json.dumps(response))
            print(
                f"[Q1/Q2 Server] #{request_count} input={message!r} output={transformed!r}"
            )
    finally:
        socket.close(0)
        context.term()


if __name__ == "__main__":
    main()
