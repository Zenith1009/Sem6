# Distributed Computing (CS332) | Assignment 3

---

**Student Name :** *Naishadh Rana* <br>
**Roll. No :** U23CS014

---

---

## Task 1: CPU Load Check
- Command used (macOS/Linux):
```
ps -A -o %cpu | awk '{s+=$1} END {print s}'
```
- Measured load during this lab: **140.9%** → exceeds 70%, so classified as **overloaded** (multi-core sum can exceed 100%).
- Interpretation: <30% lightly loaded, 30–70% moderately loaded, >70% overloaded.

## Task 2: Simple Client–Server Chat (half-duplex)
- Server waits, client connects, they take turns sending lines.

**Server.java:**
```java


Outputs: (two terminals):
```bash
# Terminal A (Server)
cd DC/Lab3
naish@MacBook-Air Lab3 % java SimpleChatServer 5001
Server listening on port 5001
Client connected. Type 'exit' to close.
Client: hii
Server> hello
Client: test
Server> test
Client left.
naish@MacBook-Air Lab3 % 
```
```bash
# Terminal B (Client)
naish@MacBook-Air Lab3 % java SimpleChatClient 5001
Connected. Type 'exit' to quit.
You> hii
Server> hello
You> test
Server> test
You> exit
naish@MacBook-Air Lab3 %
```

## Task 3: Multi-Client Broadcasting Chat
- Server keeps a list of connected clients and broadcasts messages from one to all others.
- Each client has a reader thread so messages arrive while typing.

Run:
```bash
cd DC/Lab3
javac -d bin BroadcastChatServer.java BroadcastChatClient.java
java -cp bin BroadcastChatServer    # Terminal 1
java -cp bin BroadcastChatClient    # Terminal 2 (repeat for more clients)
```
Type `exit` on a client to leave.

## Task 4: Persistent P2P Chat (full-duplex)
- Each instance is both a listener and a connector.
- Both peers can connect to each other; duplicates are auto-dropped.
- Commands: `c host port` | `s message` | `q`

Run (two peers):
```bash
cd DC/Lab3
javac -d bin P2PChat.java
java -cp bin P2PChat 7002    # Terminal A
java -cp bin P2PChat 7003    # Terminal B
```
From either terminal, connect to the other:
```
c localhost 7003
```
Send messages:
```
s hello
```
Quit:
```
q
```
