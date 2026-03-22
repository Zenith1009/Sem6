#!/usr/bin/env python3
import argparse
import queue
import threading

import zmq


def stdin_reader(command_queue: queue.Queue) -> None:
    while True:
        try:
            command = input().strip()
            command_queue.put(command)
        except EOFError:
            command_queue.put("quit")
            return


def apply_command(sub_socket: zmq.Socket, command: str, active: set[str]) -> bool:
    if not command:
        return True
    if command == "list":
        print(f"[Q6 Subscriber] Active subscriptions: {sorted(active)}")
        return True
    if command == "quit":
        print("[Q6 Subscriber] Quit requested.")
        return False
    if command.startswith("+"):
        topic = command[1:].strip().upper()
        sub_socket.setsockopt_string(zmq.SUBSCRIBE, topic)
        active.add(topic)
        print(f"[Q6 Subscriber] Added subscription: {topic}")
        return True
    if command.startswith("-"):
        topic = command[1:].strip().upper()
        sub_socket.setsockopt_string(zmq.UNSUBSCRIBE, topic)
        active.discard(topic)
        print(f"[Q6 Subscriber] Removed subscription: {topic}")
        return True

    print("[Q6 Subscriber] Unknown command. Use +TOPIC, -TOPIC, list, quit")
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="Q6 dynamic subscriber")
    parser.add_argument(
        "--endpoints",
        default="tcp://localhost:5581,tcp://localhost:5582,tcp://localhost:5583",
        help="Comma-separated publisher endpoints",
    )
    parser.add_argument(
        "--topics",
        default="SPORTS",
        help="Comma-separated initial subscriptions",
    )
    args = parser.parse_args()

    endpoints = [endpoint.strip() for endpoint in args.endpoints.split(",") if endpoint.strip()]
    topics = {topic.strip().upper() for topic in args.topics.split(",") if topic.strip()}

    context = zmq.Context.instance()
    sub = context.socket(zmq.SUB)
    for endpoint in endpoints:
        sub.connect(endpoint)

    for topic in topics:
        sub.setsockopt_string(zmq.SUBSCRIBE, topic)

    print(f"[Q6 Subscriber] Connected to: {endpoints}")
    print(f"[Q6 Subscriber] Initial subscriptions: {sorted(topics)}")
    print("[Q6 Subscriber] Commands: +TOPIC, -TOPIC, list, quit")

    command_queue: queue.Queue[str] = queue.Queue()
    input_thread = threading.Thread(target=stdin_reader, args=(command_queue,), daemon=True)
    input_thread.start()

    poller = zmq.Poller()
    poller.register(sub, zmq.POLLIN)

    running = True
    try:
        while running:
            while not command_queue.empty():
                running = apply_command(sub, command_queue.get_nowait(), topics)
                if not running:
                    break

            if not running:
                break

            events = dict(poller.poll(timeout=500))
            if sub in events and events[sub] == zmq.POLLIN:
                print(f"[Q6 Subscriber] {sub.recv_string()}")
    finally:
        sub.close(0)
        context.term()


if __name__ == "__main__":
    main()
