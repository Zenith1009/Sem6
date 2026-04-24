# 🤖 Rock Paper Scissors — Robot Arm Simulation

> **Course:** Robotics and Its Applications (RaIA)

---

## Project Overview

This project is a **real-time Rock-Paper-Scissors game** where a human player competes against an AI-powered animated robot arm. The robot is not just random — it **learns to predict and counter the human's patterns** using a Q-Learning agent that persists its knowledge across sessions.

The simulation is entirely software-based: no physical hardware is required. The user plays through a **webcam**, and the robot responds with a **procedurally animated skeletal hand** rendered on screen.

## Team Details
- Bhavyanshi Karela (U23CS079)
- Naishadh Rana (U23CS014)
- Dhruv Jindal (U23AI083)
- Ashish Maurya (U23ME073)
- Sujay Bhati (U23EE036)
- Ved Patel (U23EC066)

---

## Project Goals

| Goal | Implementation |
|---|---|
| Simulate a robot arm playing RPS | Articulated 2D skeletal hand drawn with forward kinematics |
| Detect the human's gesture | Real-time hand landmark detection via MediaPipe |
| Make the robot "intelligent" | Q-Learning agent that learns from play history |
| Prevent misdetections from flickering | Gesture stabiliser requiring N consecutive consistent frames |
| Create smooth, natural motion | Cubic ease-in-out interpolation between hand poses |
| Persist learning across sessions | Q-table serialised to `rps_qtable.json` |

---

## Thought Process & Design Decisions

### Q-Learning for the robot's AI:

Q-Learning is a **model-free reinforcement learning** algorithm we used here because:

- The robot does not know the human's strategy in advance.  
- The environment (human behavior) is non-deterministic and changes over time.
- Q-Learning can learn an optimal counter-strategy purely from **reward signals** (win/loss/draw).

**State space:** The last 3 moves made by the human (e.g., `"rock,paper,rock"`). This gives the robot a short-term memory of the human's tendencies.

**Action space:** `{rock, paper, scissors}`

**Reward signal:**
```
+1  →  robot wins (correctly countered human)
 0  →  draw
-1  →  robot loses
```

**Bellman update:**
```
Q(s, a) ← Q(s, a) + α [r + γ · max Q(s', ·) − Q(s, a)]
```

Where:
- `α = 0.3` — learning rate (moderately fast updates)
- `γ = 0.9` — discount factor (values future wins)
- `ε` — exploration rate, starts at 0.3 and decays to 0.05 (ε-greedy policy)

**Why ε-greedy?** Early in the game, the robot needs to explore different moves. As it accumulates more data, ε decays so it increasingly **exploits** its learned Q-table.

---

### Why MediaPipe for gesture detection?

MediaPipe Hands provides **21 hand landmark points** (x, y, z coordinates) detected in real-time from a webcam feed. It was chosen because:

- It runs **on-device** with low latency using TensorFlow Lite + XNNPACK.
- No custom training is needed — it ships with a pre-trained model.
- The landmark schema is well-documented and maps directly to finger-tip/MCP positions.

**Gesture classification logic:**
- A finger is "open" if its **tip landmark is above its MCP (knuckle) joint** by a threshold of 0.05 normalised units.
- Gesture rules:
  - ≤1 open finger → **Rock**
  - ≥4 open fingers → **Paper**
  - Index + Middle open, Ring + Little closed → **Scissors**

---

### Why procedural skeletal animation instead of sprites?

Sprite-based hand images are static and non-interactive. Using **forward kinematics** (computing joint positions from angles using `cos/sin`) allows:

- Any intermediate pose between Rock → Paper → Scissors to be computed mathematically.
- Smooth **interpolated transitions** between gestures using `HandPose.lerp()`.
- A dynamic "pump" animation (sinusoidal `wrist_y` offset during countdown) that syncs naturally to the beat.

**Ease function used:** Cubic ease-in-out
```python
if t < 0.5:  return 4t³
else:         return 1 − (−2t + 2)³ / 2
```
This gives motion that **accelerates out of rest and decelerates into the target pose**, mimicking real physical movement.

---

## Architecture

```
rps_sim-final.py
│
├── FingerPose / HandPose          ← Data model (dataclasses)
│     • curl, spread per finger
│     • lerp() for interpolation
│
├── HandRenderer                   ← Articulated 2D drawing (OpenCV)
│     • Forward kinematics per finger
│     • Wrist, palm, joints, fingertips
│
├── AnimationController            ← Smooth pose transitions
│     • ease_in_out_cubic()
│     • Pump animation (sinusoidal wrist bounce)
│
├── QLearningAgent                 ← AI brain
│     • State: last 3 user moves
│     • ε-greedy action selection
│     • Bellman Q-update
│     • rps_qtable.json persistence
│
├── GestureStabiliser              ← Anti-flicker filter
│     • N-frame consistency check
│
├── get_finger_status()            ← MediaPipe landmark → open/closed
├── classify_gesture()             ← Finger status → RPS label
│
└── main()                         ← Game loop (state machine)
      States: countdown → shoot → show → result → next_round → game_over
```

---

## Libraries Used

| Library | Purpose |
|---|---|
| **OpenCV (`cv2`)** | Camera capture, all drawing, window display |
| **MediaPipe** | Real-time 21-point hand landmark detection |
| **NumPy** | Panel/frame construction, gradient backgrounds, polygon arrays |
| **json** | Q-table persistence |
| **dataclasses** | `FingerPose`, `HandPose` |
| **math** | `cos`, `sin`, `pi` for forward kinematics |
| **time** | State timing, animation interpolation |

---

## 🎮 Controls

| Key | Action |
|---|---|
| `Q` | Quit the game |
| `R` | Restart from round 1 (preserves Q-table) |
| `T` | Toggle between Q-Learning and Random mode |

---

## 🔄 Game State Machine

```
[COUNTDOWN]  →  3…2…1…SHOOT!  (robot pumps fist)
     ↓
  [SHOOT]    →  Brief freeze (0.15s), robot commits choice
     ↓
   [SHOW]    →  2s window to show gesture to camera
     ↓
  [RESULT]   →  Display result for 3s, update Q-table
     ↓
[NEXT_ROUND] →  (if rounds remain) 2s transition title
     ↓
[GAME_OVER]  →  Final score screen, press R to restart
```

---

## Persistence: `rps_qtable.json`

The Q-table is saved to disk after every round and loaded on startup. It stores:

- All encountered states (keyed by `"move1,move2,move3"`)
- Q-values for all 3 actions per state
- `__stats__`: cumulative wins/losses/draws and current ε value

This means **the robot gets smarter the more you play**, even across separate sessions.

---

## Sample Output

```
=======================================================
🎮  ROCK PAPER SCISSORS — ROBOT ARM SIMULATION (v2)
=======================================================
  Rounds : 10
  Mode   : Q-Learning
  Keys   : Q=quit  R=restart  T=toggle mode
=======================================================

Loaded Q-table (9 states, 13 rounds played)

🤖 Robot chose: paper (Q-Learning, ε=0.28)
👤 You chose: rock
📊 Result: Robot Wins! 👍
🧠 Q-table: 9 states | ε: 0.280
🏆 Score — You: 0 | Robot: 1
```

---

## Setup & Dependencies

```bash
pip install opencv-python mediapipe numpy
python3 rps_sim-final.py
```

> **Requirements:** Python 3.10+, a working webcam, decent lighting for hand detection.

---

## Key AI/RL Concepts Demonstrated

1. **Reinforcement Learning** — Agent learns via trial-and-error with reward signals, not labelled data.
2. **Q-Learning (off-policy TD control)** — Model-free; no prior knowledge of the environment required.
3. **ε-greedy Exploration** — Balances exploration vs. exploitation; decays over time.
4. **Temporal Difference Learning** — Q-values updated after each round without needing complete episode rollouts.
5. **State Representation** — History window of last 3 moves captures short-term patterns in human behaviour.
6. **Gesture Recognition** — Computer vision pipeline (camera → landmarks → classification → stabilisation) feeding into the AI loop.
