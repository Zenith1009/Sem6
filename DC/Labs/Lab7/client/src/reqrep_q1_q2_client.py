#!/usr/bin/env python3
import argparse
import json

import zmq

DEFAULT_MESSAGES = ["7", "hello world", "-3.5", "value=12", "ZeroMQ"]
TERMINATION_MESSAGE = "STOP_SERVER"


def main() -> None:
    parser = argparse.ArgumentParser(description="Q1/Q2 REQ-REP client")
    parser.add_argument("--endpoint", default="tcp://localhost:5555", help="Server endpoint")
    parser.add_argument(
        "--messages",
        nargs="*",
        default=DEFAULT_MESSAGES,
        help="Messages to send to server",
    )
    parser.add_argument(
        "--stop-server",
        action="store_true",
        help="Send termination message after normal requests",
    )
    args = parser.parse_args()

    context = zmq.Context.instance()
    socket = context.socket(zmq.REQ)
    socket.connect(args.endpoint)

    print(f"[Q1/Q2 Client] Connected to {args.endpoint}")

    try:
        for local_request_number, message in enumerate(args.messages, start=1):
            socket.send_string(message)
            raw_reply = socket.recv_string()
            reply = json.loads(raw_reply)
            print(
                "[Q1/Q2 Client] "
                f"client_req={local_request_number} "
                f"server_req={reply['request_count']} "
                f"input={reply['input']!r} "
                f"output={reply['transformed']!r}"
            )

        if args.stop_server:
            socket.send_string(TERMINATION_MESSAGE)
            raw_reply = socket.recv_string()
            reply = json.loads(raw_reply)
            print(
                "[Q1/Q2 Client] "
                f"stop_ack server_req={reply['request_count']} "
                f"message={reply['transformed']!r}"
            )
    finally:
        socket.close(0)
        context.term()


if __name__ == "__main__":
    main()
