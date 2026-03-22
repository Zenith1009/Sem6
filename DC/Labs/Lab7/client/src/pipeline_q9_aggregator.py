#!/usr/bin/env python3
import argparse
import json
import time
import uuid

import zmq


def main() -> None:
    parser = argparse.ArgumentParser(description="Q9 stage-3 aggregator")
    parser.add_argument("--bind", default="tcp://*:5602", help="Bind endpoint for stage-2 output")
    parser.add_argument("--name", default=f"agg-{uuid.uuid4().hex[:4]}")
    parser.add_argument("--expected", type=int, default=0, help="Optional stop after N messages (0 = run forever)")
    args = parser.parse_args()

    context = zmq.Context.instance()
    pull = context.socket(zmq.PULL)
    pull.bind(args.bind)

    print(f"[Q9 Aggregator {args.name}] Listening on {args.bind}")

    count = 0
    start = time.perf_counter()
    try:
        while True:
            result = json.loads(pull.recv_string())
            count += 1
            print(
                f"[Q9 Aggregator {args.name}] count={count} "
                f"task={result['task_id']} worker={result['worker']} processed={result['processed']}"
            )

            if args.expected > 0 and count >= args.expected:
                break
    finally:
        elapsed = max(time.perf_counter() - start, 1e-9)
        throughput = count / elapsed
        print(
            f"[Q9 Aggregator {args.name}] total={count} elapsed={elapsed:.3f}s throughput={throughput:.2f} msg/s"
        )
        pull.close(0)
        context.term()


if __name__ == "__main__":
    main()
