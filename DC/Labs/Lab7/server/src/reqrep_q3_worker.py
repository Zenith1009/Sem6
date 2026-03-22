#!/usr/bin/env python3
import argparse
import time
import uuid

import zmq


def main() -> None:
    parser = argparse.ArgumentParser(description="Q3 worker process")
    parser.add_argument("--backend-endpoint", default="tcp://localhost:5561", help="Broker backend")
    parser.add_argument("--worker-id", default=f"worker-{uuid.uuid4().hex[:6]}")
    args = parser.parse_args()

    context = zmq.Context.instance()
    socket = context.socket(zmq.REP)
    socket.connect(args.backend_endpoint)

    print(f"[Q3 Worker {args.worker_id}] Connected to {args.backend_endpoint}")

    try:
        while True:
            message = socket.recv_string()
            time.sleep(0.1)
            response = f"{args.worker_id} handled: {message.upper()}"
            socket.send_string(response)
            print(f"[Q3 Worker {args.worker_id}] served {message!r}")
    except KeyboardInterrupt:
        print(f"\n[Q3 Worker {args.worker_id}] Stopped.")
    finally:
        socket.close(0)
        context.term()


if __name__ == "__main__":
    main()
