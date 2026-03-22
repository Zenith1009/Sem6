#!/usr/bin/env python3
import argparse

import zmq


def main() -> None:
    parser = argparse.ArgumentParser(description="Q3 ROUTER-DEALER broker")
    parser.add_argument("--frontend-bind", default="tcp://*:5560", help="Client-facing bind")
    parser.add_argument("--backend-bind", default="tcp://*:5561", help="Worker-facing bind")
    args = parser.parse_args()

    context = zmq.Context.instance()
    frontend = context.socket(zmq.ROUTER)
    backend = context.socket(zmq.DEALER)

    frontend.bind(args.frontend_bind)
    backend.bind(args.backend_bind)

    print(
        f"[Q3 Broker] frontend={args.frontend_bind} backend={args.backend_bind}. "
        "Press Ctrl+C to stop."
    )

    try:
        zmq.proxy(frontend, backend)
    except KeyboardInterrupt:
        print("\n[Q3 Broker] Stopped.")
    finally:
        frontend.close(0)
        backend.close(0)
        context.term()


if __name__ == "__main__":
    main()
