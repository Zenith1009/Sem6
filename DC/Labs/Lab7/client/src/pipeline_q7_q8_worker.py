#!/usr/bin/env python3
import argparse
import json
import time
import uuid

import zmq


def main() -> None:
    parser = argparse.ArgumentParser(description="Q7/Q8 worker")
    parser.add_argument("--input-endpoint", default="tcp://localhost:5590", help="Farmer endpoint")
    parser.add_argument(
        "--collector-endpoint",
        default="",
        help="Collector endpoint for Q8 (optional), e.g. tcp://localhost:5592",
    )
    parser.add_argument("--worker-id", default=f"worker-{uuid.uuid4().hex[:6]}")
    args = parser.parse_args()

    context = zmq.Context.instance()

    pull = context.socket(zmq.PULL)
    pull.connect(args.input_endpoint)

    push = None
    if args.collector_endpoint:
        push = context.socket(zmq.PUSH)
        push.connect(args.collector_endpoint)

    print(
        f"[Q7/Q8 Worker {args.worker_id}] input={args.input_endpoint} "
        f"collector={args.collector_endpoint or 'disabled'}"
    )

    try:
        while True:
            payload = json.loads(pull.recv_string())
            task_id = payload["task_id"]
            workload_ms = payload["workload_ms"]

            print(
                f"[Q7/Q8 Worker {args.worker_id}] processing task={task_id} "
                f"workload_ms={workload_ms}"
            )
            time.sleep(workload_ms / 1000.0)

            if push is not None:
                confirmation = {
                    "worker_id": args.worker_id,
                    "task_id": task_id,
                    "status": "done",
                }
                push.send_string(json.dumps(confirmation))
    except KeyboardInterrupt:
        print(f"\n[Q7/Q8 Worker {args.worker_id}] Stopped.")
    finally:
        pull.close(0)
        if push is not None:
            push.close(0)
        context.term()


if __name__ == "__main__":
    main()
