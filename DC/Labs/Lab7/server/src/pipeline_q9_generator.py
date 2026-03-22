#!/usr/bin/env python3
import argparse
import json
import random
import time

import zmq


def main() -> None:
    parser = argparse.ArgumentParser(description="Q9 stage-1 task generator")
    parser.add_argument("--bind", default="tcp://*:5600", help="Stage-2 worker input")
    parser.add_argument("--tasks", type=int, default=50)
    parser.add_argument("--delay", type=float, default=0.01)
    args = parser.parse_args()

    context = zmq.Context.instance()
    push = context.socket(zmq.PUSH)
    push.bind(args.bind)

    print(f"[Q9 Generator] Sending {args.tasks} tasks on {args.bind}")
    time.sleep(1.0)

    start = time.perf_counter()
    try:
        for task_id in range(1, args.tasks + 1):
            payload = {
                "task_id": task_id,
                "value": random.randint(1, 100),
            }
            push.send_string(json.dumps(payload))
            time.sleep(args.delay)
    finally:
        elapsed = time.perf_counter() - start
        print(f"[Q9 Generator] Finished sending in {elapsed:.3f}s")
        push.close(0)
        context.term()


if __name__ == "__main__":
    main()
