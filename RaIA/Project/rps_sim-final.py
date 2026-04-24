"""
pip install opencv-python mediapipe numpy
"""

import cv2
import mediapipe as mp
import numpy as np
import time
import random
import math
import json
import os
from dataclasses import dataclass, field

@dataclass
class FingerPose:
    curl: float = 0.0
    spread: float = 0.0


@dataclass
class HandPose:
    thumb:  FingerPose = field(default_factory=FingerPose)
    index:  FingerPose = field(default_factory=FingerPose)
    middle: FingerPose = field(default_factory=FingerPose)
    ring:   FingerPose = field(default_factory=FingerPose)
    little: FingerPose = field(default_factory=FingerPose)
    wrist_y: float = 0.0          

    FINGER_NAMES = ('thumb', 'index', 'middle', 'ring', 'little')

    def copy(self):
        p = HandPose(wrist_y=self.wrist_y)
        for n in self.FINGER_NAMES:
            src = getattr(self, n)
            setattr(p, n, FingerPose(src.curl, src.spread))
        return p

    @staticmethod
    def lerp(a: 'HandPose', b: 'HandPose', t: float) -> 'HandPose':
        t = max(0.0, min(1.0, t))
        p = HandPose(wrist_y=a.wrist_y + (b.wrist_y - a.wrist_y) * t)
        for n in HandPose.FINGER_NAMES:
            fa, fb = getattr(a, n), getattr(b, n)
            setattr(p, n, FingerPose(
                curl   = fa.curl   + (fb.curl   - fa.curl)   * t,
                spread = fa.spread + (fb.spread - fa.spread) * t,
            ))
        return p

POSES = {
    "idle": HandPose(
        thumb  = FingerPose(0.40,  0.00),
        index  = FingerPose(0.50,  0.00),
        middle = FingerPose(0.50,  0.00),
        ring   = FingerPose(0.55,  0.00),
        little = FingerPose(0.60,  0.00),
    ),
    "rock": HandPose(
        thumb  = FingerPose(0.90,  0.20),
        index  = FingerPose(1.00, -0.10),
        middle = FingerPose(1.00,  0.00),
        ring   = FingerPose(1.00,  0.00),
        little = FingerPose(1.00,  0.10),
    ),
    "paper": HandPose(
        thumb  = FingerPose(0.00, -0.40),
        index  = FingerPose(0.00, -0.15),
        middle = FingerPose(0.00, -0.05),
        ring   = FingerPose(0.00,  0.05),
        little = FingerPose(0.00,  0.25),
    ),
    "scissors": HandPose(
        thumb  = FingerPose(0.85,  0.20),
        index  = FingerPose(0.00, -0.25),
        middle = FingerPose(0.00,  0.15),
        ring   = FingerPose(1.00,  0.05),
        little = FingerPose(1.00,  0.15),
    ),
}

class HandRenderer:
    FINGERS = {
        'index':  dict(base=(-30, -35), angle=-1.65, l1=38, l2=32, w=11, cr1=1.80, cr2=1.50),
        'middle': dict(base=( -8, -38), angle=-1.57, l1=42, l2=34, w=11, cr1=1.80, cr2=1.50),
        'ring':   dict(base=( 14, -36), angle=-1.50, l1=38, l2=30, w=11, cr1=1.80, cr2=1.50),
        'little': dict(base=( 34, -30), angle=-1.40, l1=32, l2=25, w=10, cr1=1.80, cr2=1.50),
    }
    THUMB = dict(base=(-48, -5), angle=-2.30, l1=30, l2=25, w=13, cr1=1.20, cr2=0.90)

    C_FILL    = (185, 185, 195)
    C_LIGHT   = (200, 200, 210)
    C_DARK    = (145, 145, 155)
    C_EDGE    = ( 95, 100, 110)
    C_JOINT   = (155, 160, 170)
    C_ACCENT  = (210, 150,  85)

    def draw(self, canvas, cx: int, cy: int, pose: HandPose, scale: float = 1.0):
        s = scale
        cy += int(pose.wrist_y * s)

        self._draw_wrist(canvas, cx, cy, s)
        self._draw_palm(canvas, cx, cy, s)

        for name in ('little', 'ring', 'middle', 'index'):
            self._draw_segment(canvas, cx, cy, self.FINGERS[name],
                               getattr(pose, name), s)
        self._draw_segment(canvas, cx, cy, self.THUMB, pose.thumb, s)
        self._draw_palm_accent(canvas, cx, cy, s)

    def _draw_wrist(self, canvas, cx, cy, s):
        pts = self._poly(cx, cy, s, [(-38, 58), (-32, 100), (32, 100), (38, 58)])
        cv2.fillPoly(canvas, [pts], self.C_DARK)
        cv2.polylines(canvas, [pts], True, self.C_EDGE, 2, cv2.LINE_AA)
        p1 = (cx - int(36 * s), cy + int(60 * s))
        p2 = (cx + int(36 * s), cy + int(60 * s))
        cv2.line(canvas, p1, p2, self.C_ACCENT, 2, cv2.LINE_AA)

    def _draw_palm(self, canvas, cx, cy, s):
        pts = self._poly(cx, cy, s,
                         [(-48, 58), (-52, -8), (-38, -35),
                          (38, -33), (52, -5), (48, 58)])
        cv2.fillPoly(canvas, [pts], self.C_FILL)
        cv2.polylines(canvas, [pts], True, self.C_EDGE, 2, cv2.LINE_AA)

    def _draw_palm_accent(self, canvas, cx, cy, s):
        centre = (cx, cy + int(10 * s))
        cv2.circle(canvas, centre, int(8 * s), self.C_ACCENT, 2, cv2.LINE_AA)
        cv2.circle(canvas, centre, int(3 * s), self.C_ACCENT, -1, cv2.LINE_AA)

    def _draw_segment(self, canvas, cx, cy, fdef, fp: FingerPose, s):
        bx = cx + int(fdef['base'][0] * s)
        by = cy + int(fdef['base'][1] * s)

        a1 = fdef['angle'] + fp.spread * 0.4 + fp.curl * fdef['cr1']
        l1 = fdef['l1'] * s
        mx = bx + int(math.cos(a1) * l1)
        my = by + int(math.sin(a1) * l1)

        a2 = a1 + fp.curl * fdef['cr2']
        l2 = fdef['l2'] * s
        tx = mx + int(math.cos(a2) * l2)
        ty = my + int(math.sin(a2) * l2)

        w = int(fdef['w'] * s)

        cv2.line(canvas, (bx, by), (mx, my), self.C_FILL,  w * 2,       cv2.LINE_AA)
        cv2.line(canvas, (mx, my), (tx, ty), self.C_FILL,  int(w * 1.7), cv2.LINE_AA)

        cv2.line(canvas, (bx, by), (mx, my), self.C_EDGE,  2, cv2.LINE_AA)
        cv2.line(canvas, (mx, my), (tx, ty), self.C_EDGE,  2, cv2.LINE_AA)

        # Base joint
        cv2.circle(canvas, (bx, by), int(5 * s), self.C_JOINT,  -1, cv2.LINE_AA)
        cv2.circle(canvas, (bx, by), int(5 * s), self.C_EDGE,    1, cv2.LINE_AA)
        # Mid joint (accent ring)
        cv2.circle(canvas, (mx, my), int(5 * s), self.C_JOINT,  -1, cv2.LINE_AA)
        cv2.circle(canvas, (mx, my), int(5 * s), self.C_ACCENT,  1, cv2.LINE_AA)
        # Fingertip
        cv2.circle(canvas, (tx, ty), int(w * 0.8), self.C_LIGHT, -1, cv2.LINE_AA)
        cv2.circle(canvas, (tx, ty), int(w * 0.8), self.C_EDGE,   2, cv2.LINE_AA)

    @staticmethod
    def _poly(cx, cy, s, offsets):
        return np.array([[cx + int(x * s), cy + int(y * s)]
                         for x, y in offsets], np.int32)

def _ease_in_out_cubic(t: float) -> float:
    if t < 0.5:
        return 4.0 * t * t * t
    return 1.0 - pow(-2.0 * t + 2.0, 3) / 2.0


class AnimationController:
    def __init__(self):
        self.current  = POSES["idle"].copy()
        self.source   = POSES["idle"].copy()
        self.target   = POSES["idle"].copy()
        self.duration = 0.5
        self.t_start  = 0.0
        self.active   = False       # transition in progress

        self.pumping    = False
        self.pump_speed = 2.5       # pumps per second
        self.pump_amp   = 25.0

    def transition_to(self, target, duration: float = 0.5):
        if isinstance(target, str):
            target = POSES[target]
        self.source   = self.current.copy()
        self.target   = target.copy()
        self.duration = max(duration, 0.01)
        self.t_start  = time.time()
        self.active   = True

    def start_pump(self):
        self.pumping = True
        self.transition_to("rock", duration=0.3)

    def stop_pump(self):
        self.pumping = False

    def update(self) -> HandPose:
        now = time.time()

        if self.active:
            t = min(1.0, (now - self.t_start) / self.duration)
            self.current = HandPose.lerp(self.source, self.target,
                                         _ease_in_out_cubic(t))
            if t >= 1.0:
                self.active  = False
                self.current = self.target.copy()

        if self.pumping:
            phase = now * self.pump_speed * 2.0 * math.pi
            self.current.wrist_y = math.sin(phase) * self.pump_amp
        elif abs(self.current.wrist_y) > 0.5:
            self.current.wrist_y *= 0.85          # decay to rest
        else:
            self.current.wrist_y = 0.0

        return self.current

class QLearningAgent:
    """
    State:  last 3 user moves  (or "initial" if history is short)
    Action: rock / paper / scissors
    Reward: +1 win, 0 draw, -1 loss

    Epsilon-greedy exploration; Q-table persisted to JSON.
    """

    ACTIONS = ["rock", "paper", "scissors"]
    COUNTER = {"rock": "paper", "paper": "scissors", "scissors": "rock"}

    def __init__(self, alpha=0.3, gamma=0.9, epsilon=0.3,
                 epsilon_min=0.05, epsilon_decay=0.995, q_table_path=None):
        self.alpha         = alpha
        self.gamma         = gamma
        self.epsilon       = epsilon
        self.epsilon_min   = epsilon_min
        self.epsilon_decay = epsilon_decay

        if q_table_path is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            self.q_table_path = os.path.join(script_dir, "rps_qtable.json")
        else:
            self.q_table_path = q_table_path

        self.user_history  = []
        self.total_rounds  = 0
        self.wins = self.losses = self.draws = 0
        self.q_table       = self._load_q_table()

    def _state_key(self):
        if len(self.user_history) < 3:
            return "initial"
        return f"{self.user_history[-3]},{self.user_history[-2]},{self.user_history[-1]}"
# Q helper table
    def _get_q(self, state):
        if state not in self.q_table:
            self.q_table[state] = {a: 0.0 for a in self.ACTIONS}
        return self.q_table[state]

    def choose_action(self):
        state = self._state_key()
        if random.random() < self.epsilon:
            return random.choice(self.ACTIONS)
        q = self._get_q(state)
        best = max(q.values())
        return random.choice([a for a, v in q.items() if v == best])

    @staticmethod
    def get_reward(robot, user):
        if robot == user:
            return 0
        return 1 if QLearningAgent.COUNTER[user] == robot else -1

    def update(self, robot_move, user_move):
        state_before = self._state_key()
        reward = self.get_reward(robot_move, user_move)

        self.user_history.append(user_move)
        self.total_rounds += 1
        if   reward > 0: self.wins   += 1
        elif reward < 0: self.losses += 1
        else:            self.draws  += 1

        # Q-update:  Q(s,a) ← Q(s,a) + α[r + γ·max Q(s',·) − Q(s,a)]
        state_after = self._state_key()
        qb = self._get_q(state_before)
        qa = self._get_q(state_after)
        old = qb[robot_move]
        qb[robot_move] = round(old + self.alpha * (
            reward + self.gamma * max(qa.values()) - old), 4)

        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
        self._save_q_table()
        return reward

    def _load_q_table(self):
        if os.path.exists(self.q_table_path):
            try:
                with open(self.q_table_path, 'r') as f:
                    data = json.load(f)
                if "__stats__" in data:
                    s = data.pop("__stats__")
                    self.total_rounds = s.get("total_rounds", 0)
                    self.wins    = s.get("wins", 0)
                    self.losses  = s.get("losses", 0)
                    self.draws   = s.get("draws", 0)
                    self.epsilon = s.get("epsilon", self.epsilon)
                print(f"Loaded Q-table ({len(data)} states, "
                      f"{self.total_rounds} rounds played)")
                return data
            except (json.JSONDecodeError, IOError):
                pass
        print("Starting with fresh Q-table")
        return {}

    def _save_q_table(self):
        data = dict(self.q_table)
        data["__stats__"] = dict(
            total_rounds=self.total_rounds, wins=self.wins,
            losses=self.losses, draws=self.draws,
            epsilon=round(self.epsilon, 4))
        try:
            with open(self.q_table_path, 'w') as f:
                json.dump(data, f, indent=2)
        except IOError as e:
            print(f"Could not save Q-table: {e}")

    def reset_history(self):
        self.user_history = []

    def get_stats_text(self):
        if self.total_rounds == 0:
            return "No data yet"
        wr = self.wins / self.total_rounds * 100
        return f"W:{self.wins} L:{self.losses} D:{self.draws} ({wr:.0f}%)"

    def get_q_table_size(self):
        return len([k for k in self.q_table if k != "__stats__"])


def get_finger_status(landmarks):
    thumb_open = 1 if landmarks[4].x < landmarks[3].x else 0

    status = [thumb_open]
    for tip, mcp in [(8, 5), (12, 9), (16, 13), (20, 17)]:
        status.append(1 if landmarks[mcp].y - landmarks[tip].y > 0.05 else 0)
    return status


def classify_gesture(fs):
    thumb, index, middle, ring, little = fs
    total = sum(fs)
    if total <= 1:
        return "rock"
    if total >= 4:
        return "paper"
    if index == 1 and middle == 1 and ring == 0 and little == 0:
        return "scissors"
    return "unknown"


class GestureStabiliser:

    def __init__(self, required_frames: int = 4):
        self.required = required_frames
        self.buffer: list[str] = []
        self.stable = "unknown"

    def update(self, gesture: str) -> str:
        self.buffer.append(gesture)
        if len(self.buffer) > self.required:
            self.buffer.pop(0)
        if (len(self.buffer) == self.required
                and len(set(self.buffer)) == 1
                and self.buffer[0] != "unknown"):
            self.stable = self.buffer[0]
        return self.stable

    def reset(self):
        self.buffer.clear()
        self.stable = "unknown"

def decide_winner(user, robot):
    if user == robot:
        return "Draw!", (0, 255, 255)
    if ((user == "rock" and robot == "scissors") or
        (user == "scissors" and robot == "paper") or
        (user == "paper" and robot == "rock")):
        return "You Win!", (0, 255, 0)
    return "Robot Wins!", (0, 100, 255)


def draw_countdown(frame, text, colour=(255, 255, 255)):
    font = cv2.FONT_HERSHEY_DUPLEX
    sc, th = 3, 5
    (tw, tht), _ = cv2.getTextSize(text, font, sc, th)
    h, w = frame.shape[:2]
    x, y = (w - tw) // 2, (h + tht) // 2
    cv2.putText(frame, text, (x, y), font, sc, (0, 0, 0),   th + 3)
    cv2.putText(frame, text, (x, y), font, sc, colour, th)


def draw_hud(frame, rnd, total, u_score, r_score):
    h, w = frame.shape[:2]
    font = cv2.FONT_HERSHEY_SIMPLEX
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (w, 55), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)

    cv2.putText(frame, f"Round {rnd}/{total}",
                (15, 38), font, 0.9, (255, 255, 255), 2)
    stxt = f"You: {u_score}  |  Robot: {r_score}"
    (sw, _), _ = cv2.getTextSize(stxt, font, 0.9, 2)
    cv2.putText(frame, stxt, (w - sw - 15, 38), font, 0.9, (255, 255, 255), 2)


def draw_result_overlay(frame, user_move, robot_choice, result_text, result_colour):
    h, w = frame.shape[:2]
    font = cv2.FONT_HERSHEY_SIMPLEX

    overlay = frame.copy()
    cv2.rectangle(overlay, (0, h // 2 - 80), (w, h // 2 + 80), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)

    utxt = f"You: {user_move.upper()}"
    (uw, _), _ = cv2.getTextSize(utxt, font, 1.0, 2)
    cv2.putText(frame, utxt, ((w - uw) // 2, h // 2 - 35),
                font, 1.0, (0, 255, 200), 2)

    (rw, _), _ = cv2.getTextSize(result_text, font, 1.5, 3)
    cv2.putText(frame, result_text, ((w - rw) // 2, h // 2 + 30),
                font, 1.5, result_colour, 3)


def draw_robot_panel(frame, pose: HandPose, renderer: HandRenderer,
                     game_state: str, robot_choice, mode: str,
                     agent=None, scale: float = 1.0):
    h, w = frame.shape[:2]
    pw = int(w * 0.45)

    panel = np.zeros((h, pw, 3), dtype=np.uint8)
    grad = np.linspace(0, 1, h).reshape(-1, 1)
    panel[:, :, 0] = (35 + 20 * grad).astype(np.uint8)   # B
    panel[:, :, 1] = (25 + 15 * grad).astype(np.uint8)   # G
    panel[:, :, 2] = (25 + 15 * grad).astype(np.uint8)   # R

    font = cv2.FONT_HERSHEY_SIMPLEX

    title = "ROBOT ARM"
    (tw, _), _ = cv2.getTextSize(title, font, 0.8, 2)
    cv2.putText(panel, title, ((pw - tw) // 2, 35), font, 0.8,
                (100, 200, 255), 2)

    if mode == "qlearn":
        mlabel, mcol = "Q-LEARNING", (0, 200, 255)
    else:
        mlabel, mcol = "RANDOM", (200, 200, 200)
    (mw, _), _ = cv2.getTextSize(mlabel, font, 0.5, 1)
    cv2.putText(panel, mlabel, ((pw - mw) // 2, 52), font, 0.5, mcol, 1)
    cv2.line(panel, (20, 60), (pw - 20, 60), (60, 60, 80), 2)

    hand_cx = pw // 2
    hand_cy = h // 2 - 20
    renderer.draw(panel, hand_cx, hand_cy, pose, scale)

    if game_state == "countdown":
        label = "Thinking..."
        (lw, _), _ = cv2.getTextSize(label, font, 0.7, 2)
        cv2.putText(panel, label, ((pw - lw) // 2, h - 100),
                    font, 0.7, (150, 150, 200), 2)
    elif robot_choice and game_state in ("show", "result", "next_round", "game_over"):
        clabel = f"Robot: {robot_choice.upper()}"
        (cw, _), _ = cv2.getTextSize(clabel, font, 0.8, 2)
        cv2.putText(panel, clabel, ((pw - cw) // 2, h - 100),
                    font, 0.8, (0, 255, 200), 2)

    if agent and mode == "qlearn":
        y0 = h - 75
        cv2.line(panel, (20, y0 - 10), (pw - 20, y0 - 10), (60, 60, 80), 1)
        cv2.putText(panel, f"All-time: {agent.get_stats_text()}",
                    (15, y0 + 10), font, 0.4, (180, 180, 200), 1)
        cv2.putText(panel,
                    f"States: {agent.get_q_table_size()}  Eps: {agent.epsilon:.2f}",
                    (15, y0 + 30), font, 0.4, (150, 150, 170), 1)
        cv2.putText(panel, "'T' toggle mode",
                    (15, y0 + 50), font, 0.35, (120, 120, 140), 1)

    cv2.rectangle(panel, (0, 0), (pw - 1, h - 1), (60, 60, 80), 2)
    return panel

def main():
    mp_hands   = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    hands = mp_hands.Hands(
        static_image_mode=False, max_num_hands=1,
        min_detection_confidence=0.7, min_tracking_confidence=0.7)

    q_agent    = QLearningAgent()
    robot_mode = "qlearn"

    renderer   = HandRenderer()
    anim       = AnimationController()
    stabiliser = GestureStabiliser(required_frames=4)

    TOTAL_ROUNDS = 10
    S_COUNTDOWN  = "countdown"
    S_SHOOT      = "shoot"
    S_SHOW       = "show"
    S_RESULT     = "result"
    S_NEXT       = "next_round"
    S_GAMEOVER   = "game_over"

    current_round = 1
    user_score = robot_score = 0
    game_state    = S_COUNTDOWN
    state_time    = None
    robot_choice  = None
    user_move     = None
    result_text   = ""
    result_colour = (255, 255, 255)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Cannot open camera.")
        return
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,  640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    WIN = "Rock Paper Scissors — Robot Arm Simulation"
    print("\n" + "=" * 55)
    print("🎮  ROCK PAPER SCISSORS — ROBOT ARM SIMULATION (v2)")
    print("=" * 55)
    print(f"  Rounds : {TOTAL_ROUNDS}")
    print(f"  Mode   : {'Q-Learning' if robot_mode == 'qlearn' else 'Random'}")
    print("  Keys   : Q=quit  R=restart  T=toggle mode")
    print("=" * 55 + "\n")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        rgb   = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        res   = hands.process(rgb)

        if res.multi_hand_landmarks:
            for hl in res.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hl, mp_hands.HAND_CONNECTIONS)

        if game_state == S_COUNTDOWN:
            if state_time is None:
                state_time = time.time()
                anim.start_pump()

            elapsed = time.time() - state_time

            if   elapsed < 1: draw_countdown(frame, "3",      (0, 255, 255))
            elif elapsed < 2: draw_countdown(frame, "2",      (0, 165, 255))
            elif elapsed < 3: draw_countdown(frame, "1",      (0, 100, 255))
            elif elapsed < 4: draw_countdown(frame, "SHOOT!", (0, 255,   0))
            else:
                if robot_mode == "qlearn":
                    robot_choice = q_agent.choose_action()
                    print(f"🤖 Robot chose: {robot_choice} "
                          f"(Q-Learning, ε={q_agent.epsilon:.2f})")
                else:
                    robot_choice = random.choice(["rock", "paper", "scissors"])
                    print(f"🤖 Robot chose: {robot_choice} (Random)")
                anim.stop_pump()
                game_state = S_SHOOT
                state_time = time.time()

            draw_hud(frame, current_round, TOTAL_ROUNDS, user_score, robot_score)

        elif game_state == S_SHOOT:
            elapsed = time.time() - state_time
            draw_countdown(frame, "SHOOT!", (0, 255, 0))
            draw_hud(frame, current_round, TOTAL_ROUNDS, user_score, robot_score)

            if elapsed > 0.15:
                anim.transition_to(robot_choice, duration=0.45)
                stabiliser.reset()
                game_state = S_SHOW
                state_time = time.time()

        elif game_state == S_SHOW:
            elapsed  = time.time() - state_time
            raw_move = "unknown"

            if res.multi_hand_landmarks:
                for hl in res.multi_hand_landmarks:
                    fs = get_finger_status(hl.landmark)
                    raw_move = classify_gesture(fs)

            stable_move = stabiliser.update(raw_move)

            remaining = max(0.0, 2.0 - elapsed)
            cv2.putText(frame,
                        f"Show your gesture! ({remaining:.1f}s)",
                        (10, frame.shape[0] - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

            accepted = stable_move in ("rock", "paper", "scissors")
            timed_out = elapsed > 2.0

            if accepted or timed_out:
                user_move = stable_move if accepted else "rock"
                if not accepted:
                    print("⚠️  No valid gesture detected, defaulting to rock")

                result_text, result_colour = decide_winner(user_move, robot_choice)
                if   result_text == "You Win!":    user_score  += 1
                elif result_text == "Robot Wins!": robot_score += 1

                # Q-learning update
                if robot_mode == "qlearn":
                    reward = q_agent.update(robot_choice, user_move)
                    sym = {1: "👍", 0: "🤝", -1: "👎"}.get(reward, "")
                    print(f"👤 You chose: {user_move}")
                    print(f"📊 Result: {result_text} {sym}")
                    print(f"🧠 Q-table: {q_agent.get_q_table_size()} states "
                          f"| ε: {q_agent.epsilon:.3f}")
                    print(f"🏆 Score — You: {user_score} "
                          f"| Robot: {robot_score}\n")
                else:
                    print(f"👤 You chose: {user_move}")
                    print(f"📊 Result: {result_text}")
                    print(f"🏆 Score — You: {user_score} "
                          f"| Robot: {robot_score}\n")

                game_state = S_RESULT
                state_time = time.time()

            draw_hud(frame, current_round, TOTAL_ROUNDS, user_score, robot_score)

        elif game_state == S_RESULT:
            elapsed = time.time() - state_time
            draw_result_overlay(frame, user_move, robot_choice,
                                result_text, result_colour)
            draw_hud(frame, current_round, TOTAL_ROUNDS, user_score, robot_score)

            if elapsed > 3:
                if current_round < TOTAL_ROUNDS:
                    current_round += 1
                    game_state = S_NEXT
                    state_time = time.time()
                    anim.transition_to("idle", duration=0.5)
                else:
                    game_state = S_GAMEOVER
                    state_time = time.time()

        elif game_state == S_NEXT:
            elapsed = time.time() - state_time
            draw_countdown(frame, f"Round {current_round}", (255, 255, 0))
            draw_hud(frame, current_round, TOTAL_ROUNDS, user_score, robot_score)

            if elapsed > 2:
                game_state = S_COUNTDOWN
                state_time = None

        elif game_state == S_GAMEOVER:
            h, w = frame.shape[:2]
            font  = cv2.FONT_HERSHEY_SIMPLEX

            overlay = frame.copy()
            cv2.rectangle(overlay, (0, 0), (w, h), (0, 0, 0), -1)
            cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)

            if   user_score > robot_score: ftxt, col = "YOU WIN!",     (0, 255, 0)
            elif robot_score > user_score: ftxt, col = "ROBOT WINS!",  (0, 100, 255)
            else:                          ftxt, col = "IT'S A TIE!",  (255, 255, 0)

            (fw, _), _ = cv2.getTextSize(ftxt, cv2.FONT_HERSHEY_DUPLEX, 2.0, 4)
            cv2.putText(frame, ftxt, ((w - fw) // 2, h // 2 - 50),
                        cv2.FONT_HERSHEY_DUPLEX, 2.0, col, 4)

            stxt = f"Final Score   You: {user_score}  -  Robot: {robot_score}"
            (sw, _), _ = cv2.getTextSize(stxt, font, 1.0, 2)
            cv2.putText(frame, stxt, ((w - sw) // 2, h // 2 + 20),
                        font, 1.0, (255, 255, 255), 2)

            rtxt = "Press 'R' to play again  |  'Q' to quit"
            (rw, _), _ = cv2.getTextSize(rtxt, font, 0.7, 2)
            cv2.putText(frame, rtxt, ((w - rw) // 2, h // 2 + 70),
                        font, 0.7, (180, 180, 180), 2)

        current_pose = anim.update()
        robot_panel  = draw_robot_panel(
            frame, current_pose, renderer, game_state,
            robot_choice, robot_mode, agent=q_agent, scale=1.2)

        sep = np.zeros((frame.shape[0], 3, 3), dtype=np.uint8)
        sep[:, :] = (60, 60, 80)
        combined = np.hstack([frame, sep, robot_panel])

        cv2.imshow(WIN, combined)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('r'):
            current_round = 1
            user_score = robot_score = 0
            game_state = S_COUNTDOWN
            state_time = None
            robot_choice = None
            user_move    = None
            result_text  = ""
            result_colour = (255, 255, 255)
            q_agent.reset_history()
            stabiliser.reset()
            anim.transition_to("idle", duration=0.4)
            print("\n🔄 Game restarted!\n")
        elif key == ord('t'):
            if robot_mode == "random":
                robot_mode = "qlearn"
                print(f"\n🧠 Switched to Q-LEARNING mode")
                print(f"   Q-table: {q_agent.get_q_table_size()} states "
                      f"| All-time: {q_agent.get_stats_text()}\n")
            else:
                robot_mode = "random"
                print("\n🎲 Switched to RANDOM mode\n")

    cap.release()
    cv2.destroyAllWindows()
    q_agent._save_q_table()
    print(f"\n📊 Final Q-Learning stats: {q_agent.get_stats_text()}")
    print(f"   Q-table saved with {q_agent.get_q_table_size()} states")
    print("👋 Thanks for playing!")


if __name__ == "__main__":
    main()
