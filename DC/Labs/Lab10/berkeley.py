"""
Berkeley Algorithm – Clock Synchronization
==========================================
A master node synchronizes clocks across multiple slave nodes
by computing an average and sending individual adjustments.

How it works:
1. Master polls all slaves for their current clock times.
2. Master computes the average of all times (including its own).
3. Master sends each node the adjustment δ needed to reach the average.
4. Each node applies its adjustment.

Time Complexity:
  - Polling:     O(n)
  - Averaging:   O(n)
  - Sending adj: O(n)
  Overall:       O(n)  where n = number of nodes
"""

import time
import random


# ----------  Node  ----------
class Node:
    def __init__(self, name, clock_offset=0):
        """
        clock_offset : seconds added to real time to simulate drift.
        Positive  → node is ahead,  Negative → node is behind.
        """
        self.name = name
        self.clock_offset = clock_offset

    @property
    def clock(self):
        return time.time() + self.clock_offset

    def apply_adjustment(self, delta):
        self.clock_offset += delta
        print(f"  [{self.name}] adjustment = {delta:+.4f}s  →  new offset = {self.clock_offset:+.4f}s")


# ----------  Master  ----------
class Master(Node):
    def synchronize(self, slaves):
        print("\n[Master] Polling clocks...")

        all_nodes   = [self] + slaves
        polled_clocks = {}

        for node in all_nodes:
            t = node.clock
            polled_clocks[node.name] = t
            print(f"  {node.name}: {t:.4f}  (offset {node.clock_offset:+.2f}s)")

        # Compute average
        avg = sum(polled_clocks.values()) / len(polled_clocks)
        print(f"\n[Master] Average time = {avg:.4f}")

        # Compute and send adjustments
        print("\n[Master] Sending adjustments...")
        for node in all_nodes:
            delta = avg - polled_clocks[node.name]
            node.apply_adjustment(delta)


# ----------  Demo  ----------
if __name__ == "__main__":
    print("=" * 55)
    print("        Berkeley Algorithm – Demo")
    print("=" * 55)

    # Create nodes with intentional clock drifts
    master  = Master("Master",   clock_offset=0)
    slave1  = Node("Slave-1",    clock_offset=+5)   # 5s ahead
    slave2  = Node("Slave-2",    clock_offset=-3)   # 3s behind
    slave3  = Node("Slave-3",    clock_offset=+1)   # 1s ahead

    print("\nInitial clock offsets:")
    for n in [master, slave1, slave2, slave3]:
        print(f"  {n.name}: {n.clock_offset:+.2f}s")

    master.synchronize([slave1, slave2, slave3])

    print("\nFinal clock offsets after sync:")
    for n in [master, slave1, slave2, slave3]:
        print(f"  {n.name}: {n.clock_offset:+.4f}s")

    print("\n[Summary]")
    print("  All clocks converge toward their average,")
    print("  eliminating drift without a single authoritative source.")
    print("\nTime Complexity: O(n)  where n = number of nodes in the system.")
