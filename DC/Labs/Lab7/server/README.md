# Lab 7 ZeroMQ Server Package

Server-side processes for Assignment 7:

- Q1-Q2 REQ-REP server
- Q3 broker and workers
- Q4-Q5 publisher
- Q6 category publishers
- Q7-Q8 farmer and collector
- Q9 stage-1 generator

## Build

```bash
./build_server.sh
```

## Common Run Commands

```bash
./run_q1_q2_server.sh
./run_q3_broker.sh
./run_q3_worker.sh tcp://localhost:5561 worker-1
./run_q4_q5_publisher.sh
./run_q6_publisher.sh SPORTS tcp://*:5581
./run_q7_q8_farmer.sh tcp://*:5590 20 0.05
./run_q8_collector.sh tcp://*:5592 20
./run_q9_generator.sh tcp://*:5600 50 0.01
```
