#!/usr/bin/env python3
import argparse
import json

import zmq


def main() -> None:
    parser = argparse.ArgumentParser(description="Q8 result collector")
    parser.add_argument("--bind", default="tcp://*:5592", help="Collector bind endpoint")
    parser.add_argument("--expected", type=int, default=20, help="Expected completed task count")
    args = parser.parse_args()

    context = zmq.Context.instance()
    pull = context.socket(zmq.PULL)
    pull.bind(args.bind)

    print(f"[Q8 Collector] Waiting on {args.bind}, expected={args.expected}")

    completed = 0
    try:
        while completed < args.expected:
            message = json.loads(pull.recv_string())
            completed += 1
            print(
                f"[Q8 Collector] completed={completed}/{args.expected} "
                f"task={message['task_id']} worker={message['worker_id']}"
            )

        print("[Q8 Collector] All expected tasks completed.")
    finally:
        pull.close(0)
        context.term()


if __name__ == "__main__":
    main()
