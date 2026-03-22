#!/usr/bin/env python3
import argparse
import random
import time
from datetime import datetime

import zmq


def main() -> None:
    parser = argparse.ArgumentParser(description="Q4/Q5 TIME+RANDOM publisher")
    parser.add_argument("--bind", default="tcp://*:5570", help="Publisher bind endpoint")
    parser.add_argument("--interval", type=float, default=1.0, help="Publish interval in seconds")
    args = parser.parse_args()

    context = zmq.Context.instance()
    pub = context.socket(zmq.PUB)
    pub.bind(args.bind)

    print(f"[Q4/Q5 Publisher] Publishing on {args.bind}")

    try:
        while True:
            now_text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            rand_val = random.randint(1, 100)

            pub.send_string(f"TIME {now_text}")
            pub.send_string(f"RANDOM {rand_val}")
            print(f"[Q4/Q5 Publisher] TIME={now_text} RANDOM={rand_val}")

            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\n[Q4/Q5 Publisher] Stopped.")
    finally:
        pub.close(0)
        context.term()


if __name__ == "__main__":
    main()
