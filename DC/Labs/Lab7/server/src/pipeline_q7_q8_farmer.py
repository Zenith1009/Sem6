#!/usr/bin/env python3
import argparse
import json
import random
import time

import zmq


def main() -> None:
    parser = argparse.ArgumentParser(description="Q7/Q8 task generator (farmer)")
    parser.add_argument("--bind", default="tcp://*:5590", help="Worker input endpoint")
    parser.add_argument("--tasks", type=int, default=20, help="Number of tasks")
    parser.add_argument("--delay", type=float, default=0.05, help="Delay between tasks")
    args = parser.parse_args()

    context = zmq.Context.instance()
    push = context.socket(zmq.PUSH)
    push.bind(args.bind)

    print(f"[Q7/Q8 Farmer] Sending {args.tasks} tasks on {args.bind}")
    time.sleep(1.0)

    try:
        for task_id in range(1, args.tasks + 1):
            workload_ms = random.randint(100, 900)
            payload = {"task_id": task_id, "workload_ms": workload_ms}
            push.send_string(json.dumps(payload))
            print(f"[Q7/Q8 Farmer] queued task={task_id} workload_ms={workload_ms}")
            time.sleep(args.delay)
    finally:
        push.close(0)
        context.term()


if __name__ == "__main__":
    main()
