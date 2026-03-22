#!/usr/bin/env python3
import argparse

import zmq


def main() -> None:
    parser = argparse.ArgumentParser(description="Q4 single-tag subscriber")
    parser.add_argument("--endpoint", default="tcp://localhost:5570", help="Publisher endpoint")
    parser.add_argument("--tag", default="TIME", choices=["TIME", "RANDOM"], help="Tag filter")
    args = parser.parse_args()

    context = zmq.Context.instance()
    sub = context.socket(zmq.SUB)
    sub.connect(args.endpoint)
    sub.setsockopt_string(zmq.SUBSCRIBE, args.tag)

    print(f"[Q4 Subscriber] Connected to {args.endpoint}, subscribed to {args.tag}")

    try:
        while True:
            message = sub.recv_string()
            print(f"[Q4 Subscriber] {message}")
    except KeyboardInterrupt:
        print("\n[Q4 Subscriber] Stopped.")
    finally:
        sub.close(0)
        context.term()


if __name__ == "__main__":
    main()
