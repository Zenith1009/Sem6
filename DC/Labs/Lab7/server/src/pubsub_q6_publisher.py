#!/usr/bin/env python3
import argparse
import random
import time
from datetime import datetime

import zmq

EVENT_SAMPLES = {
    "SPORTS": ["Team A won", "Player traded", "Tournament scheduled"],
    "WEATHER": ["Rain expected", "Heatwave alert", "Cloud cover increased"],
    "FINANCE": ["Market up", "Market down", "Inflation data released"],
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Q6 category publisher")
    parser.add_argument("--category", choices=["SPORTS", "WEATHER", "FINANCE"], required=True)
    parser.add_argument("--bind", required=True, help="Bind endpoint, e.g. tcp://*:5581")
    parser.add_argument("--interval", type=float, default=1.0)
    args = parser.parse_args()

    context = zmq.Context.instance()
    pub = context.socket(zmq.PUB)
    pub.bind(args.bind)

    print(f"[Q6 Publisher {args.category}] Publishing on {args.bind}")

    try:
        while True:
            event_text = random.choice(EVENT_SAMPLES[args.category])
            payload = f"{args.category} {datetime.now().isoformat()} {event_text}"
            pub.send_string(payload)
            print(f"[Q6 Publisher {args.category}] {payload}")
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print(f"\n[Q6 Publisher {args.category}] Stopped.")
    finally:
        pub.close(0)
        context.term()


if __name__ == "__main__":
    main()
