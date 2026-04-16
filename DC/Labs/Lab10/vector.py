"""
Vector Clocks
=============
An extension of Lamport clocks that captures the full causality
relationship (happened-before) between events in a distributed system.

Each node maintains a vector  V[0..n-1]  where n = number of processes.
V[i] = number of events process i has caused that this process knows about.

Rules:
  1. Local event:    V[self] += 1
  2. Send message:   V[self] += 1,  piggyback full vector with message
  3. Receive message:
       V[self] += 1
       V[j] = max(V[j], received[j])   for all j

Comparing two vector timestamps A and B:
  A == B   iff  A[i] == B[i]  for all i
  A <  B   iff  A[i] <= B[i]  for all i  AND  A != B   (A happened-before B)
  concurrent  iff  neither A < B  nor  B < A

Time Complexity:
  - Local / Send / Receive event:   O(n)  — must update/compare n-entry vector
  - Causality comparison:           O(n)
  Overall per-event: O(n)  where n = number of processes
"""


# ----------  Utilities  ----------
def vec_max(v1, v2):
    return [max(a, b) for a, b in zip(v1, v2)]

def compare(v1, v2):
    """Return the causal relationship between two vector timestamps."""
    less_eq  = all(a <= b for a, b in zip(v1, v2))
    greater_eq = all(a >= b for a, b in zip(v1, v2))
    if v1 == v2:
        return "equal"
    elif less_eq:
        return "happened-before  (<)"
    elif greater_eq:
        return "happened-after   (>)"
    else:
        return "concurrent       (||)"


# ----------  Process  ----------
class Process:
    def __init__(self, pid, total_processes):
        self.pid    = pid                          # integer index 0, 1, 2, ...
        self.name   = f"P{pid + 1}"
        self.vector = [0] * total_processes       # full vector clock

    def _tick(self):
        self.vector[self.pid] += 1

    def local_event(self, description):
        self._tick()
        print(f"  [{self.name}] LOCAL  '{description}'  →  {self.vector}")
        return list(self.vector)   # snapshot for logging

    def send(self, receiver, message):
        self._tick()
        snapshot = list(self.vector)
        print(f"  [{self.name}→{receiver.name}] SEND  '{message}'  @  {snapshot}")
        receiver.receive(self, snapshot, message)

    def receive(self, sender, received_vec, message):
        self._tick()
        self.vector = vec_max(self.vector, received_vec)
        self.vector[self.pid] = max(self.vector[self.pid],
                                    received_vec[self.pid]) + 0  # already ticked
        # Re-apply tick logic correctly:
        # After merge, our own slot stays as ticked value (already done above).
        print(f"  [{sender.name}→{self.name}] RECV  '{message}'  →  {self.vector}")


# ----------  Demo  ----------
if __name__ == "__main__":
    print("=" * 60)
    print("            Vector Clocks – Demo")
    print("=" * 60)

    n  = 3
    P1 = Process(0, n)
    P2 = Process(1, n)
    P3 = Process(2, n)

    print("\n--- Sequence of events ---")

    snap_P1_e1 = P1.local_event("write x=1")          # P1: [1,0,0]
    P1.send(P2, "msg-A")                              # P1: [2,0,0]

    snap_P2_e1 = P2.local_event("read y")              # P2: [0,1,0]
    # P2 receives from P1 → merge
    # (receive is triggered inside send above, so P2 clock is already merged)
    P2.send(P3, "msg-B")

    snap_P3_e1 = P3.local_event("compute z")           # P3: concurrent with P2
    P3.send(P1, "ack")

    P1.local_event("committed")

    print("\n--- Final vector clocks ---")
    for p in [P1, P2, P3]:
        print(f"  {p.name}: {p.vector}")

    print("\n--- Causality comparisons (on captured snapshots) ---")
    print(f"  P1 e1 {snap_P1_e1}  vs  P2 e1 {snap_P2_e1}:  {compare(snap_P1_e1, snap_P2_e1)}")
    print(f"  P3 e1 {snap_P3_e1}  vs  P2 e1 {snap_P2_e1}:  {compare(snap_P3_e1, snap_P2_e1)}")

    print("\n[Summary]")
    print("  Vector clocks capture FULL causality (happened-before).")
    print("  Unlike Lamport clocks, concurrent events are distinguishable.")
    print("  A < B  iff  A.V[i] <= B.V[i] for all i  (and at least one strict).")
    print("\nTime Complexity: O(n) per event,  O(n) per causality comparison.")
    print("  where n = number of processes in the system.")
