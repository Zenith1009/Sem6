# Lab 7 ZeroMQ Client Package

Client-side processes for Assignment 7:

- Q1-Q2 request client
- Q3 normal and strict-REQ limitation demo clients
- Q4-Q5 subscribers
- Q6 dynamic subscriber
- Q7-Q8 workers
- Q9 stage-2 workers and stage-3 aggregators

## Build

```bash
./build_client.sh
```

## Common Run Commands

```bash
./run_q1_q2_client.sh tcp://localhost:5555 stop
./run_q3_client.sh tcp://localhost:5560 5 client-A
./run_q3_bad_client.sh tcp://localhost:5560
./run_q4_subscriber.sh tcp://localhost:5570 TIME
./run_q5_time_subscriber.sh
./run_q5_random_subscriber.sh
./run_q6_subscriber.sh tcp://localhost:5581,tcp://localhost:5582,tcp://localhost:5583 SPORTS
./run_q7_q8_worker.sh tcp://localhost:5590 tcp://localhost:5592 worker-1
./run_q9_worker.sh tcp://localhost:5600 tcp://localhost:5602,tcp://localhost:5603 s2-1 0.03
./run_q9_aggregator.sh tcp://*:5602 agg-1 25
```
