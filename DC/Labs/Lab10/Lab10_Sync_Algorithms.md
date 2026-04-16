# Lab 10 – Synchronization Algorithms in Distributed Systems

**Subject:** Distributed Computing  
**Lab:** 10  
**Topic:** Clock Synchronization & Logical Clock Algorithms

---

## Aim

To implement and demonstrate synchronization algorithms used in distributed systems:
1. Cristian's Algorithm
2. Berkeley Algorithm
3. Lamport Logical Clocks
4. Vector Clocks

---

## Theory

In a distributed system, each node has its own physical clock that drifts over time.
There is no shared memory or global clock. Synchronization is therefore essential for:
- Consistent ordering of events
- Coordination between processes
- Enforcing causality

Two categories are addressed:

| Category | Algorithms | Purpose |
|---|---|---|
| Physical Clock Sync | Cristian's, Berkeley | Align wall-clock times across nodes |
| Logical Clock Sync | Lamport, Vector | Order events without physical clocks |

---

## Algorithm 1 – Cristian's Algorithm

### Concept
A **client** synchronizes its clock with a dedicated **time server**.

### Steps
1. Client records local time **T0** and sends a request to the server.
2. Server responds with its current time **T_server**.
3. Client records the receipt time **T1**.
4. Client estimates one-way network delay = **(T1 − T0) / 2**
5. Client sets its clock to: **T_server + one_way_delay**

```
Client          Server
  |---request---->|   at T0
  |<--T_server----|   at T1
  
  one_way_delay = (T1 - T0) / 2
  new_clock     = T_server + one_way_delay
```

### Code – `cristian.py`

```python
T0 = time.time()
server_time = server.get_time()
T1 = time.time()

one_way_delay = (T1 - T0) / 2
self.clock = server_time + one_way_delay
```

### Sample Output
```
[Node-A] Starting Cristian's sync...
  Clock BEFORE sync : 1776282009.1376  (local time)
  T0 (sent)         : 1776282009.1376
  T1 (received)     : 1776282009.1716
  Round-trip delay  : 33.97 ms
  Estimated one-way : 16.99 ms
  Server time       : 1776282019.1716
  Clock AFTER sync  : 1776282019.1886
```

### Time Complexity
| Operation | Complexity |
|---|---|
| Single sync round | **O(1)** |

### Limitations
- Assumes symmetric network delay (send delay ≈ receive delay).
- Requires a trusted, accurate time server (single point of failure).

---

## Algorithm 2 – Berkeley Algorithm

### Concept
A **master** node coordinates clock synchronization among all **slave** nodes
by computing a consensus average — no external time reference needed.

### Steps
1. Master polls all slaves for their current clock time.
2. Master computes the **average** of all times (including its own).
3. Master sends each node the **adjustment δ** needed to reach the average.
4. Each node applies its adjustment.

```
Master polls:    M=0s,  S1=+5s,  S2=−3s,  S3=+1s
Average offset:  (0 + 5 − 3 + 1) / 4 = +0.75s

Adjustments sent:
  Master  →  +0.75s
  Slave-1 →  −4.25s
  Slave-2 →  +3.75s
  Slave-3 →  −0.25s
```

### Code – `berkeley.py`

```python
avg = sum(polled_clocks.values()) / len(polled_clocks)

for node in all_nodes:
    delta = avg - polled_clocks[node.name]
    node.apply_adjustment(delta)
```

### Sample Output
```
[Master] Polling clocks...
  Master:  1776282009.1960  (offset +0.00s)
  Slave-1: 1776282014.1960  (offset +5.00s)
  Slave-2: 1776282006.1960  (offset -3.00s)
  Slave-3: 1776282010.1960  (offset +1.00s)

[Master] Average time = 1776282009.9460

[Master] Sending adjustments...
  [Master]  adjustment = +0.7500s  →  new offset = +0.7500s
  [Slave-1] adjustment = -4.2500s  →  new offset = +0.7500s
  [Slave-2] adjustment = +3.7500s  →  new offset = +0.7500s
  [Slave-3] adjustment = -0.2500s  →  new offset = +0.7500s
```

### Time Complexity
| Operation | Complexity |
|---|---|
| Poll all nodes | O(n) |
| Compute average | O(n) |
| Send adjustments | O(n) |
| **Overall** | **O(n)** |

### Advantage over Cristian's
No external time server required — clocks converge to their own consensus average.

---

## Algorithm 3 – Lamport Logical Clocks

### Concept
Proposed by **Leslie Lamport (1978)**, logical clocks assign timestamps to events
to enforce a **happened-before (→)** partial ordering without physical clocks.

### Rules
| Event | Action |
|---|---|
| Local event | `clock += 1` |
| Send message | `clock += 1`; attach timestamp to message |
| Receive message | `clock = max(local, received) + 1` |

### Happened-Before Relation (→)
- If A and B are in the **same process** and A occurs before B → A → B
- If A is a **send** event and B is the corresponding **receive** → A → B
- **Transitivity**: If A → B and B → C, then A → C

> **Key Property:** `A → B  ⟹  clock(A) < clock(B)`  
> The **converse is NOT true** — equal or greater timestamps don't imply causality.

### Code – `lamport.py`

```python
def local_event(self, description):
    self.clock += 1

def send(self, receiver, message):
    self.clock += 1
    receiver.receive(self, self.clock, message)

def receive(self, sender, received_ts, message):
    self.clock = max(self.clock, received_ts) + 1
```

### Sample Output
```
[P1] LOCAL  'start computation'  →  clock = 1
[P1→P2] SEND  'data-packet-A'   →  clock = 2
[P1→P2] RECV  'data-packet-A'   →  clock = 3
[P2] LOCAL  'process data'       →  clock = 4
[P2→P3] SEND  'data-packet-B'   →  clock = 5
[P3] LOCAL  'store result'       →  clock = 7
[P3→P1] SEND  'ack'             →  clock = 8
[P1] LOCAL  'done'               →  clock = 10
```

### Time Complexity
| Operation | Complexity |
|---|---|
| Any event (local/send/receive) | **O(1)** |

---

## Algorithm 4 – Vector Clocks

### Concept
An extension of Lamport clocks. Each process maintains a **vector** of size n
(one entry per process). This captures **full causality** and correctly identifies
**concurrent events** — something Lamport clocks cannot do.

### Rules
| Event | Action |
|---|---|
| Local event | `V[self] += 1` |
| Send message | `V[self] += 1`; piggyback full vector |
| Receive message | `V[self] += 1`; `V[j] = max(V[j], received[j])` for all j |

### Causality Comparison

Given timestamps **A** and **B** from two events:

| Relation | Condition |
|---|---|
| A **happened-before** B | `A[i] ≤ B[i]` for all i, and at least one strict |
| A **happened-after** B | `A[i] ≥ B[i]` for all i, and at least one strict |
| A and B are **concurrent** | Neither condition holds |

> **Key advantage:** `A → B  ⟺  A.V < B.V`  — bidirectional causality detection!

### Code – `vector.py`

```python
def local_event(self):
    self.vector[self.pid] += 1

def send(self, receiver, message):
    self.vector[self.pid] += 1
    receiver.receive(self, list(self.vector), message)

def receive(self, sender, received_vec, message):
    self.vector[self.pid] += 1
    self.vector = [max(a, b) for a, b in zip(self.vector, received_vec)]
```

### Sample Output
```
[P1] LOCAL  'write x=1'  →  [1, 0, 0]
[P1→P2] SEND  'msg-A'   @  [2, 0, 0]
[P1→P2] RECV  'msg-A'   →  [2, 1, 0]
[P2] LOCAL  'read y'     →  [2, 2, 0]
[P2→P3] SEND  'msg-B'   @  [2, 3, 0]
[P2→P3] RECV  'msg-B'   →  [2, 3, 1]
[P3] LOCAL  'compute z'  →  [2, 3, 2]

Causality comparisons:
  P1 e1 [1,0,0]  vs  P2 e1 [2,2,0]  →  happened-before (<)
  P3 e1 [2,3,2]  vs  P2 e1 [2,2,0]  →  happened-after  (>)
```

### Time Complexity
| Operation | Complexity |
|---|---|
| Any event (local/send/receive) | **O(n)** |
| Causality comparison | **O(n)** |

---

## Comparison Summary

| Feature | Cristian's | Berkeley | Lamport | Vector |
|---|---|---|---|---|
| Type | Physical sync | Physical sync | Logical clock | Logical clock |
| Clock type | Wall clock | Wall clock | Integer counter | Integer vector |
| Requires time server | ✅ Yes | ❌ No | ❌ No | ❌ No |
| Detects causality | ✅ (physical) | ✅ (physical) | Partial only | ✅ Full |
| Detects concurrency | ❌ | ❌ | ❌ | ✅ |
| Time complexity | O(1) | O(n) | O(1)/event | O(n)/event |
| Space per process | O(1) | O(1) | O(1) | **O(n)** |

---

## Conclusion

- **Cristian's Algorithm** offers a simple and fast way to sync a client's clock with a server,
  assuming symmetric network delays.
- **Berkeley Algorithm** eliminates the need for an external time server by using a consensus
  average — more robust for distributed environments.
- **Lamport Clocks** provide a lightweight logical ordering of events (happened-before),
  sufficient for many coordination problems.
- **Vector Clocks** give complete causal information and can identify concurrent events,
  making them essential for conflict detection in distributed databases and version control systems.
