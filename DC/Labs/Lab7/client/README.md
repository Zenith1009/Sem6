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
python3 -m pip install --quiet --disable-pip-version-check -r requirements.txt
```

## Common Run Commands

```bash
python3 src/reqrep_q1_q2_client.py --endpoint tcp://localhost:5555 --stop-server
python3 src/reqrep_q3_client.py --endpoint tcp://localhost:5560 --count 5 --name client-A
python3 src/reqrep_q3_bad_client.py --endpoint tcp://localhost:5560
python3 src/pubsub_q4_subscriber.py --endpoint tcp://localhost:5570 --tag TIME
python3 src/pubsub_q5_time_subscriber.py --endpoint tcp://localhost:5570
python3 src/pubsub_q5_random_subscriber.py --endpoint tcp://localhost:5570
python3 src/pubsub_q6_dynamic_subscriber.py --endpoints tcp://localhost:5581,tcp://localhost:5582,tcp://localhost:5583 --topics SPORTS
python3 src/pipeline_q7_q8_worker.py --input-endpoint tcp://localhost:5590 --collector-endpoint tcp://localhost:5592 --worker-id worker-1
python3 src/pipeline_q9_stage2_worker.py --input-endpoint tcp://localhost:5600 --output-endpoints tcp://localhost:5602,tcp://localhost:5603 --worker-id s2-1 --process-delay 0.03
python3 src/pipeline_q9_aggregator.py --bind tcp://*:5602 --name agg-1 --expected 25
```
