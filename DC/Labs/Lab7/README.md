# Distributed Computing (CS332) | Assignment 7
## ZeroMQ Patterns in Python (REQ-REP, PUB-SUB, PUSH-PULL)

This lab implements complete solutions for all questions listed in [Ques.md](Ques.md), following the same documented and runnable style used in Lab5/Lab6.

## Implemented Question-Wise Solutions

- Q0: `pyzmq` installation and verification instructions
- Q1-Q2: REQ-REP transformation server with request counter and graceful termination
- Q3: Multi-client fair handling using ROUTER-DEALER broker and worker pool, plus strict REQ-REP limitation demo
- Q4-Q5: Tagged PUB-SUB (`TIME`, `RANDOM`) with one-tag and two-subscriber demonstrations
- Q6: Multi-publisher event system (`SPORTS`, `WEATHER`, `FINANCE`) with dynamic runtime subscription updates
- Q7: Farmer-worker pipeline with worker identity and workload print
- Q8: Collector process that counts worker completion notifications
- Q9: Three-stage pipeline (generator -> processing workers -> aggregators) with throughput measurement support

## Folder Structure for Sharing

- [server/](server/) -> share with teammate handling server-side processes
- [client/](client/) -> share with teammate handling client/worker/subscriber processes
- [docker-compose.yml](docker-compose.yml) -> optional one-machine two-container environment

## Q0 Installation and Verification

```bash
python3 -m pip install pyzmq
python3 -c "import zmq; print('pyzmq installed:', zmq.__version__)"
```

## Local Run (without Docker)

Open terminals in Lab7 root and run commands from [server/](server/) and [client/](client/).

One-time dependency setup:

```bash
cd server && python3 -m pip install --quiet --disable-pip-version-check -r requirements.txt
cd ../client && python3 -m pip install --quiet --disable-pip-version-check -r requirements.txt
cd ..
```

### Q1-Q2 (REQ-REP transformation + counter + graceful stop)

Terminal 1:

```bash
cd server
python3 src/reqrep_q1_q2_server.py --bind tcp://*:5555
```

Terminal 2:

```bash
cd client
python3 src/reqrep_q1_q2_client.py --endpoint tcp://localhost:5555 --stop-server
```

### Q3 (multi-client fair system + strict REQ limitation demo)

Terminal 1 (broker):

```bash
cd server
python3 src/reqrep_q3_broker.py --frontend-bind tcp://*:5560 --backend-bind tcp://*:5561
```

Terminal 2 (worker 1):

```bash
cd server
python3 src/reqrep_q3_worker.py --backend-endpoint tcp://localhost:5561 --worker-id worker-1
```

Terminal 3 (worker 2):

```bash
cd server
python3 src/reqrep_q3_worker.py --backend-endpoint tcp://localhost:5561 --worker-id worker-2
```

Terminal 4 (normal client A):

```bash
cd client
python3 src/reqrep_q3_client.py --endpoint tcp://localhost:5560 --count 6 --name client-A
```

Terminal 5 (normal client B):

```bash
cd client
python3 src/reqrep_q3_client.py --endpoint tcp://localhost:5560 --count 6 --name client-B
```

Terminal 6 (bad REQ client for limitation):

```bash
cd client
python3 src/reqrep_q3_bad_client.py --endpoint tcp://localhost:5560
```

Expected: bad client shows REQ socket state error when sending another request before receiving reply.

### Q4-Q5 (PUB-SUB tags)

Terminal 1 (publisher):

```bash
cd server
python3 src/pubsub_q4_q5_publisher.py --bind tcp://*:5570 --interval 1.0
```

Terminal 2 (Q4 single-tag subscriber):

```bash
cd client
python3 src/pubsub_q4_subscriber.py --endpoint tcp://localhost:5570 --tag TIME
```

Terminal 3 (Q5 TIME subscriber):

```bash
cd client
python3 src/pubsub_q5_time_subscriber.py --endpoint tcp://localhost:5570
```

Terminal 4 (Q5 RANDOM subscriber):

```bash
cd client
python3 src/pubsub_q5_random_subscriber.py --endpoint tcp://localhost:5570
```

Expected: each subscriber prints only subscribed tag messages.

### Q6 (dynamic event subscriptions)

Terminal 1:

```bash
cd server
python3 src/pubsub_q6_publisher.py --category SPORTS --bind tcp://*:5581 --interval 1.0
```

Terminal 2:

```bash
cd server
python3 src/pubsub_q6_publisher.py --category WEATHER --bind tcp://*:5582 --interval 1.0
```

Terminal 3:

```bash
cd server
python3 src/pubsub_q6_publisher.py --category FINANCE --bind tcp://*:5583 --interval 1.0
```

Terminal 4 (dynamic subscriber):

```bash
cd client
python3 src/pubsub_q6_dynamic_subscriber.py --endpoints tcp://localhost:5581,tcp://localhost:5582,tcp://localhost:5583 --topics SPORTS
```

Inside subscriber terminal, use commands:

- `+WEATHER`
- `+FINANCE`
- `-SPORTS`
- `list`
- `quit`

Expected: only actively subscribed categories are printed. Late subscriptions miss previously published events.

### Q7-Q8 (pipeline + collector)

Terminal 1 (collector):

```bash
cd server
python3 src/pipeline_q8_collector.py --bind tcp://*:5592 --expected 20
```

Terminal 2 (worker 1):

```bash
cd client
python3 src/pipeline_q7_q8_worker.py --input-endpoint tcp://localhost:5590 --collector-endpoint tcp://localhost:5592 --worker-id worker-1
```

Terminal 3 (worker 2):

```bash
cd client
python3 src/pipeline_q7_q8_worker.py --input-endpoint tcp://localhost:5590 --collector-endpoint tcp://localhost:5592 --worker-id worker-2
```

Terminal 4 (worker 3):

```bash
cd client
python3 src/pipeline_q7_q8_worker.py --input-endpoint tcp://localhost:5590 --collector-endpoint tcp://localhost:5592 --worker-id worker-3
```

Terminal 5 (farmer):

```bash
cd server
python3 src/pipeline_q7_q8_farmer.py --bind tcp://*:5590 --tasks 20 --delay 0.05
```

Expected: workers display task/workload; collector shows total completion count.

### Q9 (three-stage pipeline + throughput)

Terminal 1 (aggregator 1):

```bash
cd client
python3 src/pipeline_q9_aggregator.py --bind tcp://*:5602 --name agg-1 --expected 25
```

Terminal 2 (aggregator 2):

```bash
cd client
python3 src/pipeline_q9_aggregator.py --bind tcp://*:5603 --name agg-2 --expected 25
```

Terminal 3 (stage-2 worker 1):

```bash
cd client
python3 src/pipeline_q9_stage2_worker.py --input-endpoint tcp://localhost:5600 --output-endpoints tcp://localhost:5602,tcp://localhost:5603 --worker-id s2-1 --process-delay 0.03
```

Terminal 4 (stage-2 worker 2):

```bash
cd client
python3 src/pipeline_q9_stage2_worker.py --input-endpoint tcp://localhost:5600 --output-endpoints tcp://localhost:5602,tcp://localhost:5603 --worker-id s2-2 --process-delay 0.03
```

Terminal 5 (generator):

```bash
cd server
python3 src/pipeline_q9_generator.py --bind tcp://*:5600 --tasks 50 --delay 0.01
```

Vary number of workers/aggregators and compare per-aggregator throughput printed by each aggregator.

## Docker Compose (optional)

From Lab7 root:

```bash
docker compose up -d --build
```

Then execute scripts inside containers as needed:

```bash
docker compose exec zmq-server bash
docker compose exec zmq-client bash
```

Stop:

```bash
docker compose down
```

## Analysis Notes for Submission

- Strict REQ-REP forces send/receive alternation on each REQ socket; violating this leads to socket state errors.
- ROUTER-DEALER broker with worker pool allows concurrent clients and fair request distribution.
- PUB-SUB is asynchronous and lossy for late subscribers; messages published before subscription are not replayed.
- PUSH-PULL distributes queued tasks fairly among ready workers (load balancing), but slow workers can still reduce end-to-end throughput.
- In Q9, throughput increases when bottleneck stage worker count is increased; imbalance between stages creates queue buildup.

## Viva Preparation Guide (Lab 7)

This section is a viva-oriented explanation of all logic, design decisions, and expected questions for Assignment 7.

### 1) Core ZeroMQ Concepts You Must Explain Clearly

1. Context
- A ZeroMQ context is the container/factory for sockets.
- Typical best practice is one context per process.

2. Bind vs Connect
- `bind` means exposing an endpoint (server-like role).
- `connect` means dialing an endpoint (client-like role).
- In ZeroMQ either side can bind, but stable endpoints usually bind.

3. Message framing
- ZeroMQ sends full messages (not raw byte stream behavior like plain TCP sockets).
- Message boundaries are preserved.

4. Queueing behavior
- ZeroMQ maintains internal queues per socket.
- Slow consumers can create backlog depending on pattern and load.

5. Pattern contract
- Each socket type has expected behavior.
- Example: REQ enforces strict `send -> recv -> send -> recv` order.

### 2) Assignment-Wise Viva Logic

#### Q0 (Install and Verify)
- Install `pyzmq`.
- Verify import and version.
- Viva point: environment verification prevents false debugging due to missing dependency.

#### Q1 (REQ-REP transformation)
- Server receives a string.
- If it contains numeric content, returns square.
- Otherwise returns uppercase text.
- Client sends mixed message types and prints responses.

Viva-ready explanation:
- This demonstrates request processing logic instead of static echo/reply.

#### Q2 (Counter + graceful stop)
- Server keeps `request_count` since startup.
- Every response includes the current server count.
- Special termination message (`STOP_SERVER`) shuts server gracefully.

Viva-ready explanation:
- Counter is in-memory process state; reset happens on restart.
- Graceful shutdown demonstrates controlled server lifecycle and cleanup.

#### Q3 (Multi-client fairness + strict REQ limitation)

What was demonstrated:
- A bad client tries to send multiple REQ messages without receiving reply first.
- This triggers expected REQ state error due to strict lockstep.

What was improved:
- Added ROUTER-DEALER broker with worker pool.
- Multiple clients can send concurrently.
- Requests are forwarded to workers, avoiding single-client lock/block patterns.

Viva-ready explanation:
- Strict REQ-REP is simple but rigid.
- ROUTER-DEALER decouples frontend and backend, improving concurrency and fairness.

#### Q4 (Tagged PUB-SUB filtering)
- Publisher sends tagged events (`TIME`, `RANDOM`).
- Subscriber uses topic filter and receives only selected tag.

Viva-ready explanation:
- Topic filtering is subscription-prefix based at subscriber side.

#### Q5 (Two subscribers, different tags)
- Two subscribers run at once with different subscriptions.
- Each receives only its own category.

Startup-order observation:
- Late subscriber misses earlier published messages.

Viva-ready explanation:
- PUB-SUB is asynchronous and non-persistent by default (no replay buffer by default).

#### Q6 (Dynamic subscriptions, multiple publishers)
- Three category publishers: `SPORTS`, `WEATHER`, `FINANCE`.
- Dynamic subscriber can add/remove topics at runtime.
- Commands: `+TOPIC`, `-TOPIC`, `list`, `quit`.

Viva-ready explanation:
- Demonstrates runtime adaptability of subscriptions.
- Also demonstrates message loss for late joins in asynchronous systems.

#### Q7 (Farmer-worker with identity/workload logs)
- Farmer (PUSH) sends tasks with workload.
- Workers (PULL) process and print worker identity + task workload.

Viva-ready explanation:
- Shows distribution behavior and practical load balancing among available workers.

#### Q8 (Result collector)
- Workers send completion confirmation to collector.
- Collector counts total completed tasks.

Viva-ready explanation:
- Separates dispatch channel from completion channel.
- Enables measurable completion tracking for the pipeline.

#### Q9 (Three-stage pipeline + throughput)
- Stage 1 generator creates tasks.
- Stage 2 workers process tasks.
- Stage 3 aggregators collect and report throughput.
- Varying worker counts demonstrates bottleneck and scaling effects.

Viva-ready explanation:
- End-to-end throughput is constrained by the slowest stage.
- Scaling bottleneck stage improves total throughput.

### 3) Pattern-Specific Key Statements (High-Yield Viva Lines)

1. REQ-REP
- Strict synchronous alternation simplifies protocol, but limits flexibility.

2. ROUTER-DEALER
- Acts as async load-balancing mediation between many clients and many workers.

3. PUB-SUB
- Excellent for broadcast/event streams.
- No guaranteed delivery/replay in default form.

4. PUSH-PULL
- Good for parallel task pipelines and work distribution.
- Slow workers can still reduce overall throughput if they become bottleneck contributors.

### 4) Most-Asked Viva Questions with Crisp Answers

1. Why use ZeroMQ instead of plain sockets?
- ZeroMQ provides high-level messaging patterns, queueing, framing, and scalable topology with less boilerplate.

2. Why did REQ fail when sending twice?
- REQ sockets enforce `send-receive` lockstep state machine.

3. Why ROUTER-DEALER for Q3?
- To decouple client ingress and worker processing for concurrent fair handling.

4. Why are PUB-SUB messages lost for late subscribers?
- Because default PUB-SUB does not store/replay old messages for new subscribers.

5. Is PUB-SUB reliable delivery by default?
- No.

6. Why add collector in Q8?
- To explicitly count completions and verify end-to-end processing.

7. What controls Q9 throughput?
- Capacity of the slowest stage in the pipeline.

8. Does increasing workers always improve speed?
- Only until another stage becomes the bottleneck.

9. What happens to request counter after restart?
- It resets (in-memory state).

10. How to make this production-reliable?
- Add acknowledgments, retries, persistence, and failure-aware orchestration.

### 5) 20-Second Viva Summary Script

"I implemented all Lab 7 ZeroMQ patterns in Python using `pyzmq`. In REQ-REP, I added content-based transformation, request counting, and graceful shutdown, then demonstrated strict REQ limitations and solved concurrency with ROUTER-DEALER plus workers. In PUB-SUB, I implemented tagged publishing, selective subscribers, and dynamic runtime subscriptions with multiple publishers, and demonstrated late-subscription message loss. In PUSH-PULL, I implemented farmer-worker distribution, completion collector, and a 3-stage pipeline with throughput and bottleneck analysis."

### 6) Submission-Friendly Observation Summary

- REQ-REP is deterministic but rigid due to strict alternation.
- ROUTER-DEALER improves fairness and concurrent handling in multi-client settings.
- PUB-SUB favors low-latency asynchronous fan-out but can lose past messages for late subscribers.
- PUSH-PULL naturally supports work distribution; throughput tuning depends on stage balance.
- In multistage pipelines, bottleneck stage optimization yields the largest throughput gain.
