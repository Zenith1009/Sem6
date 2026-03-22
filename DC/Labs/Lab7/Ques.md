# Distributed Computing
## Assignment 7

Install the ZeroMQ Python library (`pyzmq`) and run all examples from Chapter 4:

- Note 4.9: Request-Reply Pattern
- Note 4.10: Publish-Subscribe Pattern
- Note 4.11: Pipeline Pattern

Use separate terminals where required (for example: server/client, publisher/subscriber, farmer/worker) and observe communication behavior.

### Question 0
Install ZeroMQ bindings for Python:

- `pip3 install pyzmq`
- or `pip install pyzmq` (if `pip` maps to Python 3)

Verify installation by importing `zmq` in Python.

## Request-Reply Pattern (REQ-REP)

### Question 1
Modify the basic request-reply example so the server does not only append an asterisk.

The server should inspect each incoming message and transform it based on content:
- if message contains a number, return its square
- if message contains text, return uppercase text

The client should send at least five different message types and display responses.

### Question 2
Extend the same client-server system so the server tracks number of requests processed since startup.

For each reply, include the counter value. The client should display both:
- transformed response
- request number

Stop the server gracefully when a specific termination message is received.

### Question 3
Design a multi-client request-reply system where multiple clients send requests concurrently to one server.

Investigate and demonstrate behavior if one client sends multiple requests without waiting for replies.

Modify the system so it handles multiple clients fairly and does not block indefinitely. Clearly explain:
- limitations of strict REQ-REP
- how your updated design addresses those limitations

## Publish-Subscribe Pattern (PUB-SUB)

### Question 4
Modify a time server so it publishes two message types with tags (for example `TIME` and `RANDOM`) instead of only current time.

Create a client that subscribes to only one tag and prints received messages. Demonstrate that other message types are filtered out.

### Question 5
Create two different subscribers, each subscribed to a different tag from the same publisher.

Run both simultaneously and show that each receives only its subscribed messages. Also test subscriber startup timing:
- subscribers before publisher
- subscribers after publisher

Record observations.

### Question 6
Design an event-notification system using PUB-SUB where multiple publishers generate different categories (for example sports, weather, finance).

Subscribers should dynamically change subscriptions at runtime without restarting.

Demonstrate message loss and analyze implications of:
- late subscription
- asynchronous communication

## Pipeline Pattern (PUSH-PULL)

### Question 7
Modify the farmer-worker example so each worker prints its identity and workload processed.

Run multiple workers simultaneously and observe task distribution. Record load-balancing observations.

### Question 8
Enhance the pipeline by adding a result collector process that gathers completion notifications from workers.

Each worker should send a confirmation after finishing a task. The collector should count and display total completed tasks.

### Question 9
Design a three-stage processing pipeline:

1. task generator
2. intermediate processing workers
3. final aggregators

Each stage should run as a separate process.

Demonstrate throughput changes by varying worker count at different stages. Analyze bottlenecks and explain how ZeroMQ push-pull semantics influence scalability and fairness.