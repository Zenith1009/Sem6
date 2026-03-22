#!/usr/bin/env python3
import argparse

import zmq


def main() -> None:
    parser = argparse.ArgumentParser(description="Q3 bad REQ client demonstration")
    parser.add_argument("--endpoint", default="tcp://localhost:5560", help="Broker frontend")
    args = parser.parse_args()

    context = zmq.Context.instance()
    socket = context.socket(zmq.REQ)
    socket.connect(args.endpoint)

    print(f"[Q3 bad-client] Connected to {args.endpoint}")
    print("[Q3 bad-client] Sending two requests without waiting for first reply...")

    try:
        socket.send_string("bad-request-1")
        try:
            socket.send_string("bad-request-2", flags=zmq.NOBLOCK)
        except zmq.ZMQError as err:
            print(f"[Q3 bad-client] Expected strict REQ-REP limitation: {err}")

        reply = socket.recv_string()
        print(f"[Q3 bad-client] First reply received: {reply!r}")
    finally:
        socket.close(0)
        context.term()


if __name__ == "__main__":
    main()
