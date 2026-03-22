#!/usr/bin/env python3
import argparse

import zmq


def main() -> None:
    parser = argparse.ArgumentParser(description="Q5 RANDOM subscriber")
    parser.add_argument("--endpoint", default="tcp://localhost:5570", help="Publisher endpoint")
    args = parser.parse_args()

    context = zmq.Context.instance()
    sub = context.socket(zmq.SUB)
    sub.connect(args.endpoint)
    sub.setsockopt_string(zmq.SUBSCRIBE, "RANDOM")

    print(f"[Q5 RANDOM subscriber] Connected to {args.endpoint}")

    try:
        while True:
            print(f"[Q5 RANDOM subscriber] {sub.recv_string()}")
    except KeyboardInterrupt:
        print("\n[Q5 RANDOM subscriber] Stopped.")
    finally:
        sub.close(0)
        context.term()


if __name__ == "__main__":
    main()
