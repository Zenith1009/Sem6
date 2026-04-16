"""
Lamport Logical Clocks
======================
Provides a partial ordering of events in a distributed system
without physical clocks.

Rules (Lamport, 1978):
  1. Each process increments its counter before every event.
  2. When sending a message, the current counter is included.
  3. On receiving a message:
       clock = max(local_clock, received_clock) + 1

Time Complexity:
  - Local event:   O(1)
  - Send event:    O(1)
  - Receive event: O(1)
  Overall per-event: O(1)
"""


# ----------  Process  ----------
class Process:
    def __init__(self, name):
        self.name  = name
        self.clock = 0

    def _tick(self):
        """Increment clock for any internal or send event."""
        self.clock += 1

    def local_event(self, description):
        self._tick()
        print(f"  [{self.name}] LOCAL  '{description}'  →  clock = {self.clock}")

    def send(self, receiver, message):
        self._tick()
        timestamp = self.clock
        print(f"  [{self.name}→{receiver.name}] SEND  '{message}'  @  clock = {timestamp}")
        receiver.receive(self, timestamp, message)

    def receive(self, sender, received_ts, message):
        self.clock = max(self.clock, received_ts) + 1
        print(f"  [{sender.name}→{self.name}] RECV  '{message}'  →  clock = {self.clock}")


# ----------  Demo  ----------
if __name__ == "__main__":
    print("=" * 60)
    print("          Lamport Logical Clocks – Demo")
    print("=" * 60)

    P1 = Process("P1")
    P2 = Process("P2")
    P3 = Process("P3")

    print("\n--- Sequence of events ---")

    #  P1 does a local event, then sends to P2
    P1.local_event("start computation")
    P1.send(P2, "data-packet-A")

    # P2 does some work, then forwards to P3
    P2.local_event("process data")
    P2.send(P3, "data-packet-B")

    # P3 has a local event, then replies to P1
    P3.local_event("store result")
    P3.send(P1, "ack")

    # P1 receives the ack (already handled inside send)
    P1.local_event("done")

    print("\n--- Final Lamport clocks ---")
    for p in [P1, P2, P3]:
        print(f"  {p.name}: {p.clock}")

    print("\n[Summary]")
    print("  Lamport clocks give a consistent partial order (happened-before).")
    print("  If event A → event B, then clock(A) < clock(B).")
    print("  The converse is NOT guaranteed (use Vector Clocks for that).")
    print("\nTime Complexity: O(1) per event.")
