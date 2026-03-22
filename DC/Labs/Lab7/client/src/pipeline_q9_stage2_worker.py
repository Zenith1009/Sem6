#!/usr/bin/env python3
import argparse
import json
import time
import uuid

import zmq


def main() -> None:
    parser = argparse.ArgumentParser(description="Q9 stage-2 processing worker")
    parser.add_argument("--input-endpoint", default="tcp://localhost:5600")
    parser.add_argument(
        "--output-endpoints",
        default="tcp://localhost:5602",
        help="Comma-separated stage-3 aggregator endpoints",
    )
    parser.add_argument("--worker-id", default=f"s2-{uuid.uuid4().hex[:5]}")
    parser.add_argument("--process-delay", type=float, default=0.03)
    args = parser.parse_args()

    outputs = [x.strip() for x in args.output_endpoints.split(",") if x.strip()]

    context = zmq.Context.instance()
    pull = context.socket(zmq.PULL)
    pull.connect(args.input_endpoint)

    push = context.socket(zmq.PUSH)
    for endpoint in outputs:
        push.connect(endpoint)

    print(
        f"[Q9 Stage2 {args.worker_id}] input={args.input_endpoint} outputs={outputs}"
    )

    try:
        while True:
            task = json.loads(pull.recv_string())
            time.sleep(args.process_delay)

            result = {
                "task_id": task["task_id"],
                "worker": args.worker_id,
                "input": task["value"],
                "processed": task["value"] * task["value"],
            }
            push.send_string(json.dumps(result))
            print(
                f"[Q9 Stage2 {args.worker_id}] task={result['task_id']} "
                f"input={result['input']} processed={result['processed']}"
            )
    except KeyboardInterrupt:
        print(f"\n[Q9 Stage2 {args.worker_id}] Stopped.")
    finally:
        pull.close(0)
        push.close(0)
        context.term()


if __name__ == "__main__":
    main()
