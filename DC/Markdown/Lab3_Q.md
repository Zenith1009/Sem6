# Lab Assignment 3

---

## Task 1: CPU Load Calculation

Calculate the CPU load for your machine and identify the state (under loaded or overloaded) of your machine. You have to find out the CPU usage of your computer using some Unix command.

### Load States:
| CPU Usage | State |
|-----------|-------|
| > 70% | Overloaded |
| 30% - 70% | Moderately Loaded |
| < 30% | Lightly Loaded |

> **Hint:** With the help of `grep` Unix command, you can extract CPU usage.

---

## Task 2: Chat Application Scenarios

### Scenario 1: Simple Client-Server Chat

The initial phase of the lab focuses on establishing a basic, **point-to-point connection** between two independent network entities.

- The **server** utilizes a `ServerSocket` to passively listen for connections on a specific port
- The **client** initiates a `Socket` request directed at the server's IP and port
- Once the handshake is complete, they engage in a sequential, **half-duplex** exchange where each party must wait for the other to send data before responding

This scenario illustrates the core lifecycle of a TCP connection, including stream management and final socket termination.

---

### Scenario 2: Multi-Client Broadcasting Chat

The Multi-Client Chat component utilizes a **centralized server architecture** designed to facilitate real-time communication among several users simultaneously.

**Key Features:**
- The server maintains a dynamic registry of all active client connections
- Upon receiving a message from any single user, iterates through this list to broadcast the content to all other participants
- Each connection is handled by a dedicated `ClientHandler` thread, ensuring that new users can join without interference

This architecture demonstrates the **principle of isolation**, where the latency or disconnection of one client does not block the broadcasting logic for the rest of the network.

---

### Scenario 3: Persistent Peer-to-Peer (P2P) Chat

The Persistent P2P Chat represents a **decentralized model** where every node functions as both a client and a server, removing the need for a central hub.

**Architecture:**
- Each application instance runs a **background listener thread** to wait for incoming requests
- The **main thread** provides a user interface for initiating outgoing connections to other peers

**Key Features:**
- **Full-Duplex Nature:** A specialized receiver thread allows users to see incoming messages instantly while they are actively typing
- **Persistent:** When a chat session ends via an `exit` command, the socket closes, but the background listener remains active to accept new requests without a program restart
