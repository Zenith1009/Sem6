"""
Cristian's Algorithm – Clock Synchronization
=============================================
A client synchronizes its clock with a time server.

How it works:
1. Client records its local time (T0) and sends a request to the server.
2. Server replies with its current time (Tserver).
3. Client records the time it receives the reply (T1).
4. Client estimates one-way network delay = (T1 - T0) / 2
5. Client sets its clock to:  Tserver + estimated_one_way_delay

Time Complexity: O(1) per synchronization round.
"""

import time
import random


# ----------  Simulated Server  ----------
class TimeServer:
    def __init__(self, offset_seconds=0):
        """offset_seconds simulates server clock being ahead/behind real time."""
        self.offset = offset_seconds

    def get_time(self):
        """Simulate a small processing delay then return server time."""
        processing_delay = random.uniform(0.01, 0.05)  # server takes some time
        time.sleep(processing_delay)
        return time.time() + self.offset


# ----------  Client  ----------
class Client:
    def __init__(self, name="Client"):
        self.name = name
        self.clock = time.time()   # starts at real local time

    def sync_with_server(self, server: TimeServer):
        print(f"\n[{self.name}] Starting Cristian's sync...")
        print(f"  Clock BEFORE sync : {self.clock:.4f}  (local time)")

        T0 = time.time()                  # time request is sent
        server_time = server.get_time()   # round-trip (includes processing delay)
        T1 = time.time()                  # time reply is received

        round_trip   = T1 - T0
        one_way_delay = round_trip / 2

        # Adjusted clock
        self.clock = server_time + one_way_delay

        print(f"  T0 (sent)         : {T0:.4f}")
        print(f"  T1 (received)     : {T1:.4f}")
        print(f"  Round-trip delay  : {round_trip*1000:.2f} ms")
        print(f"  Estimated one-way : {one_way_delay*1000:.2f} ms")
        print(f"  Server time       : {server_time:.4f}")
        print(f"  Clock AFTER sync  : {self.clock:.4f}")


# ----------  Demo  ----------
if __name__ == "__main__":
    print("=" * 55)
    print("        Cristian's Algorithm – Demo")
    print("=" * 55)

    # Server clock is 10 seconds ahead of real time
    server = TimeServer(offset_seconds=10)
    client = Client("Node-A")

    client.sync_with_server(server)

    print("\n[Summary]")
    print("  The client adjusted its clock to match the server,")
    print("  compensating for the estimated one-way network delay.")
    print("\nTime Complexity: O(1) per sync request.")
