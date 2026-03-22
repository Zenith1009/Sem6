#!/usr/bin/env python3
import argparse
import uuid

import zmq


def main() -> None:
    parser = argparse.ArgumentParser(description="Q3 normal REQ client")
    parser.add_argument("--endpoint", default="tcp://localhost:5560", help="Broker frontend")
    parser.add_argument("--count", type=int, default=5, help="Number of requests")
    parser.add_argument("--name", default=f"client-{uuid.uuid4().hex[:4]}", help="Client name")
    args = parser.parse_args()

    context = zmq.Context.instance()
    socket = context.socket(zmq.REQ)
    socket.connect(args.endpoint)

    print(f"[Q3 {args.name}] Connected to {args.endpoint}")

    try:
        for i in range(1, args.count + 1):
            message = f"{args.name}-request-{i}"
            socket.send_string(message)
            reply = socket.recv_string()
            print(f"[Q3 {args.name}] sent={message!r} reply={reply!r}")
    finally:
        socket.close(0)
        context.term()


if __name__ == "__main__":
    main()
