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
python3 -m pip install --quiet --disable-pip-version-check -r requirements.txt
```

## Common Run Commands

```bash
python3 src/reqrep_q1_q2_server.py --bind tcp://*:5555
python3 src/reqrep_q3_broker.py --frontend-bind tcp://*:5560 --backend-bind tcp://*:5561
python3 src/reqrep_q3_worker.py --backend-endpoint tcp://localhost:5561 --worker-id worker-1
python3 src/pubsub_q4_q5_publisher.py --bind tcp://*:5570 --interval 1.0
python3 src/pubsub_q6_publisher.py --category SPORTS --bind tcp://*:5581 --interval 1.0
python3 src/pipeline_q7_q8_farmer.py --bind tcp://*:5590 --tasks 20 --delay 0.05
python3 src/pipeline_q8_collector.py --bind tcp://*:5592 --expected 20
python3 src/pipeline_q9_generator.py --bind tcp://*:5600 --tasks 50 --delay 0.01
```
