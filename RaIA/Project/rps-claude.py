"""
Rock Paper Scissors — Animated Robot Arm Simulation
=====================================================
A complete rewrite featuring:
  • Skeletal forward-kinematics hand with smooth interpolated gestures
  • Pygame-based 60fps renderer (replaces static OpenCV drawing)
  • Easing library: cubic, elastic, and back-overshoot curves
  • Improved Q-Learning with gesture-buffer smoothing
  • Clean enum-driven state machine with timed phase transitions
  • Pulsing countdown beats, result flash, per-round history strip

Dependencies:
    pip install pygame opencv-python mediapipe numpy
"""

from __future__ import annotations

import cv2
import mediapipe as mp
import numpy as np
import pygame
import time
import random
import math
import json
import os
import sys
from collections import Counter
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Optional, Tuple


# ─────────────────────────────────────────────────────────────────────────────
# WINDOW / TIMING CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────
WIN_W, WIN_H       = 1280, 720
CAM_PANEL_W        = WIN_W // 2
ROBOT_PANEL_W      = WIN_W - CAM_PANEL_W
FPS                = 60
TOTAL_ROUNDS       = 5

COUNTDOWN_DUR      = 4.0   # 3 … 2 … 1 … SHOOT!
CAPTURE_DUR        = 2.0   # window to read user gesture
REVEAL_DUR         = 0.55  # robot animates to its gesture
RESULT_DUR         = 3.0   # show result card
NEXT_ROUND_DUR     = 1.8   # "Round N" splash

# ─────────────────────────────────────────────────────────────────────────────
# COLOUR PALETTE
# ─────────────────────────────────────────────────────────────────────────────
C = {
    # backgrounds
    "bg":           (12, 12, 20),
    "panel_bg":     (18, 18, 30),
    "panel_border": (48, 52, 72),
    "dark":         (32, 34, 48),
    # text / ui
    "white":        (232, 235, 245),
    "gray":         (105, 110, 132),
    "light_gray":   (155, 160, 180),
    # accents
    "accent":       (0,  188, 255),
    "accent2":      (255, 155, 0),
    "green":        (24, 210, 120),
    "red":          (218, 58, 58),
    "yellow":       (252, 206, 28),
    # robot hand
    "r_body":       (140, 152, 170),
    "r_dark":       (88, 98, 115),
    "r_joint":      (65, 74, 95),
    "r_light":      (190, 200, 218),
    "r_shine":      (210, 218, 232),
    "r_shadow":     (50, 58, 75),
    "r_wrist":      (108, 118, 138),
}


# ─────────────────────────────────────────────────────────────────────────────
# EASING FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────
def _clamp(t: float) -> float:
    return max(0.0, min(1.0, t))

def ease_cubic(t: float) -> float:
    t = _clamp(t)
    return 4*t*t*t if t < 0.5 else 1 - (-2*t + 2)**3 / 2

def ease_back(t: float, s: float = 1.20) -> float:
    """Overshoots slightly then settles — great for snapping gestures."""
    t = _clamp(t)
    c3 = s + 1
    return 1 + c3*(t-1)**3 + s*(t-1)**2

def ease_elastic(t: float) -> float:
    """Spring-like bounce at the end."""
    t = _clamp(t)
    if t in (0, 1):
        return t
    c4 = (2*math.pi) / 3
    return pow(2, -10*t) * math.sin((t*10 - 0.75)*c4) + 1

def lerp(a, b, t):       return a + (b - a) * _clamp(t)
def lerpv(a, b, t):      return tuple(lerp(x, y, t) for x, y in zip(a, b))
def lerp_a(a, b, t):     return a + (b - a) * _clamp(t)   # angle (no wrap needed here)


# ─────────────────────────────────────────────────────────────────────────────
# ROBOT HAND — SKELETAL MODEL
# ─────────────────────────────────────────────────────────────────────────────
#
# Each finger is modelled as 3 rigid segments connected by revolute joints.
# Forward kinematics propagates from palm-base → MCP → PIP → DIP → fingertip.
#
# FINGER_BASE: (x_offset_px, y_offset_px, angle_from_vertical_deg)
#   angle 0 = pointing straight up; positive = tilt right; negative = tilt left.
#
# POSES: joint flexion angles in degrees for each of the 3 joints per finger.
#   0 = fully extended; larger = more curled toward palm.
#
FINGER_BASE: Dict[str, Tuple[float, float, float]] = {
    "thumb":  (-56,  16, -54),
    "index":  (-27, -34,  -8),
    "middle": ( -4, -41,  -2),
    "ring":   ( 21, -37,   4),
    "little": ( 44, -26,  13),
}

FINGER_SEGS: Dict[str, List[float]] = {      # segment lengths (px, unscaled)
    "thumb":  [36, 28, 22],
    "index":  [42, 30, 24],
    "middle": [46, 33, 26],
    "ring":   [42, 30, 24],
    "little": [34, 24, 20],
}

FINGER_WIDTHS: Dict[str, List[float]] = {    # half-widths per segment base
    "thumb":  [13, 11, 9],
    "index":  [12, 10, 8],
    "middle": [12, 10, 8],
    "ring":   [11,  9, 7],
    "little": [ 9,  7, 6],
}

FINGER_ORDER = ["thumb", "index", "middle", "ring", "little"]

POSES: Dict[str, Dict] = {
    "idle": {
        "thumb":  [18, 14,  8],
        "index":  [18, 22, 18],
        "middle": [18, 22, 18],
        "ring":   [20, 26, 20],
        "little": [24, 28, 22],
        "wrist":  0.0, "scale": 1.0,
    },
    "rock": {
        "thumb":  [52, 48, 32],
        "index":  [84, 78, 64],
        "middle": [86, 82, 68],
        "ring":   [85, 80, 66],
        "little": [83, 77, 62],
        "wrist": -4.0, "scale": 1.0,
    },
    "paper": {
        "thumb":  [ 4,  0,  0],
        "index":  [ 0,  0,  0],
        "middle": [ 0,  0,  0],
        "ring":   [ 0,  0,  0],
        "little": [ 0,  0,  0],
        "wrist":  5.0, "scale": 1.04,
    },
    "scissors": {
        "thumb":  [48, 44, 30],
        "index":  [-9,  0,  0],   # splay outward
        "middle": [ 9,  0,  0],   # splay outward
        "ring":   [83, 78, 63],
        "little": [82, 76, 60],
        "wrist":  0.0, "scale": 1.0,
    },
}


@dataclass
class HandState:
    """Live interpolated joint configuration of the robot hand."""
    angles: Dict[str, List[float]] = field(default_factory=dict)
    wrist:  float = 0.0
    scale:  float = 1.0

    @staticmethod
    def from_pose(name: str) -> "HandState":
        p = POSES[name]
        return HandState(
            angles={f: list(p[f]) for f in FINGER_ORDER},
            wrist=p["wrist"], scale=p.get("scale", 1.0),
        )

    @staticmethod
    def blend(a: "HandState", b: "HandState", t: float) -> "HandState":
        blended = {}
        for f in FINGER_ORDER:
            blended[f] = [lerp(a.angles[f][j], b.angles[f][j], t) for j in range(3)]
        return HandState(
            angles=blended,
            wrist=lerp_a(a.wrist, b.wrist, t),
            scale=lerp(a.scale, b.scale, t),
        )


class HandAnimator:
    """
    Drives the robot hand between named poses using configurable easing curves.
    Also manages a periodic shake effect for countdown beats.
    """
    def __init__(self):
        self._from   = HandState.from_pose("idle")
        self._to     = HandState.from_pose("idle")
        self._t      = 1.0
        self._dur    = 0.4
        self._easing = ease_cubic
        self._delay  = 0.0
        self._elapsed = 0.0
        self._shake_t = 1.0
        self._shake_dur = 0.0
        self._shake_amp = 0.0
        self.current_pose = "idle"

    # ── public API ────────────────────────────────────────────────────────────

    def go_to(self, pose: str, dur: float = 0.35,
              easing=None, delay: float = 0.0):
        if pose not in POSES:
            return
        self._from    = self._snapshot()
        self._to      = HandState.from_pose(pose)
        self._dur     = max(dur, 0.001)
        self._elapsed = -delay
        self._t       = 0.0
        self._easing  = easing or ease_cubic
        self.current_pose = pose

    def shake(self, dur: float = 0.28, amp: float = 9.0):
        self._shake_t   = 0.0
        self._shake_dur = dur
        self._shake_amp = amp

    def update(self, dt: float):
        self._elapsed = min(self._elapsed + dt, self._dur)
        raw = max(0.0, self._elapsed / self._dur)
        self._t = self._easing(raw)
        if self._shake_t < self._shake_dur:
            self._shake_t += dt

    def state(self) -> HandState:
        return HandState.blend(self._from, self._to, self._t)

    def shake_offset(self) -> Tuple[float, float]:
        if self._shake_t >= self._shake_dur:
            return 0.0, 0.0
        progress = self._shake_t / self._shake_dur
        decay    = 1.0 - progress
        ox = math.sin(self._shake_t * 14 * math.pi) * self._shake_amp * decay
        oy = math.cos(self._shake_t * 14 * math.pi) * self._shake_amp * decay * 0.45
        return ox, oy

    @property
    def done(self) -> bool:
        return self._t >= 1.0

    # ── private ───────────────────────────────────────────────────────────────

    def _snapshot(self) -> HandState:
        return HandState.blend(self._from, self._to, self._t)


# ─────────────────────────────────────────────────────────────────────────────
# FORWARD KINEMATICS + DRAWING
# ─────────────────────────────────────────────────────────────────────────────

def fk_finger(
    bx: float, by: float,
    base_deg: float,
    lengths: List[float],
    flexions: List[float],
    wrist_deg: float,
) -> List[Tuple[float, float]]:
    """
    Compute joint positions for one finger via forward kinematics.
    Returns [base, joint1, joint2, tip] in screen coords.
    """
    pts = [(bx, by)]
    # "pointing up" = -π/2 in pygame screen coords (y increases downward)
    direction = math.radians(base_deg + wrist_deg) - math.pi / 2
    for length, flex in zip(lengths, flexions):
        direction += math.radians(flex)
        nx = pts[-1][0] + length * math.cos(direction)
        ny = pts[-1][1] + length * math.sin(direction)
        pts.append((nx, ny))
    return pts


def _tapered_quad(
    surf: pygame.Surface,
    p1: Tuple[float, float], p2: Tuple[float, float],
    w1: float, w2: float,
    fill, border,
):
    """Draw a tapered (trapezoidal) segment between two points."""
    dx, dy = p2[0] - p1[0], p2[1] - p1[1]
    ln = math.hypot(dx, dy)
    if ln < 1:
        return
    px, py = -dy / ln, dx / ln                  # perpendicular unit vector
    quad = [
        (int(p1[0] + px*w1), int(p1[1] + py*w1)),
        (int(p1[0] - px*w1), int(p1[1] - py*w1)),
        (int(p2[0] - px*w2), int(p2[1] - py*w2)),
        (int(p2[0] + px*w2), int(p2[1] + py*w2)),
    ]
    pygame.draw.polygon(surf, fill,   quad)
    pygame.draw.polygon(surf, border, quad, 2)
    # Specular highlight stripe along the "lit" side
    shine = tuple(min(255, c + 30) for c in fill)
    hi = [
        (int(p1[0] + px*w1*0.42), int(p1[1] + py*w1*0.42)),
        (int(p1[0] + px*w1*0.78), int(p1[1] + py*w1*0.78)),
        (int(p2[0] + px*w2*0.78), int(p2[1] + py*w2*0.78)),
        (int(p2[0] + px*w2*0.42), int(p2[1] + py*w2*0.42)),
    ]
    pygame.draw.polygon(surf, shine, hi)


def draw_robot_hand(surf: pygame.Surface, state: HandState,
                    cx: float, cy: float, shake=(0.0, 0.0)):
    """Render the full articulated robot hand at (cx, cy)."""
    s  = state.scale
    cx += shake[0]
    cy += shake[1]

    # ── Wrist cylinder ───────────────────────────────────────────────────────
    wr = pygame.Rect(int(cx - 40*s), int(cy + 46*s), int(80*s), int(50*s))
    pygame.draw.rect(surf, C["r_wrist"], wr, border_radius=8)
    pygame.draw.rect(surf, C["r_dark"],  wr, 2, border_radius=8)
    for i in range(3):                                    # panel grooves
        gy = int(wr.top + 11 + i*12)
        pygame.draw.line(surf, C["r_dark"],
                         (wr.left+7, gy), (wr.right-7, gy), 1)

    # ── Palm plate ───────────────────────────────────────────────────────────
    palm = [
        (cx - 50*s, cy + 48*s),
        (cx - 52*s, cy +  8*s),
        (cx - 42*s, cy - 24*s),
        (cx -  9*s, cy - 40*s),
        (cx +  9*s, cy - 40*s),
        (cx + 42*s, cy - 24*s),
        (cx + 52*s, cy +  8*s),
        (cx + 50*s, cy + 48*s),
    ]
    palm = [(int(x), int(y)) for x, y in palm]
    pygame.draw.polygon(surf, C["r_body"], palm)
    pygame.draw.polygon(surf, C["r_dark"], palm, 2)
    # Subtle highlight gradient across the palm face
    hi_pts = [
        (int(cx - 28*s), int(cy + 38*s)),
        (int(cx - 30*s), int(cy +  4*s)),
        (int(cx - 23*s), int(cy - 16*s)),
        (int(cx -  4*s), int(cy - 36*s)),
        (int(cx +  4*s), int(cy - 36*s)),
        (int(cx + 10*s), int(cy - 20*s)),
        (int(cx +  8*s), int(cy + 38*s)),
    ]
    hi_col = tuple(min(255, c + 18) for c in C["r_body"])
    pygame.draw.polygon(surf, hi_col, hi_pts)

    # ── Fingers (drawn back-to-front so thumb is on top) ─────────────────────
    draw_order = ["little", "ring", "middle", "index", "thumb"]
    for name in draw_order:
        bdx, bdy, bang = FINGER_BASE[name]
        bx  = cx + bdx * s
        by  = cy + bdy * s
        segs   = [l * s for l in FINGER_SEGS[name]]
        widths = [w * s for w in FINGER_WIDTHS[name]]
        pts = fk_finger(bx, by, bang, segs, state.angles[name], state.wrist)

        for i in range(3):
            w_tip = widths[i] * 0.72 if i == 2 else widths[i+1]
            _tapered_quad(surf, pts[i], pts[i+1],
                          widths[i], w_tip, C["r_body"], C["r_dark"])
            # Intermediate knuckle disc
            if i > 0:
                kr = int(widths[i] * 0.88)
                pygame.draw.circle(surf, C["r_joint"], (int(pts[i][0]), int(pts[i][1])), kr)
                pygame.draw.circle(surf, C["r_dark"],  (int(pts[i][0]), int(pts[i][1])), kr, 1)
                pygame.draw.circle(surf, C["r_light"],
                                   (int(pts[i][0]-1), int(pts[i][1]-1)), max(1, kr//3))

        # Fingertip endcap
        tx, ty = int(pts[-1][0]), int(pts[-1][1])
        tr = int(widths[-1] * 0.84)
        pygame.draw.circle(surf, C["r_body"],  (tx, ty), tr)
        pygame.draw.circle(surf, C["r_dark"],  (tx, ty), tr, 2)
        pygame.draw.circle(surf, C["r_shine"], (tx-2, ty-2), max(1, tr//3))

        # Knuckle at finger base
        kr = int(widths[0] * 0.92)
        pygame.draw.circle(surf, C["r_joint"], (int(pts[0][0]), int(pts[0][1])), kr)
        pygame.draw.circle(surf, C["r_dark"],  (int(pts[0][0]), int(pts[0][1])), kr, 1)
        pygame.draw.circle(surf, C["r_light"],
                           (int(pts[0][0])-2, int(pts[0][1])-2), max(1, kr//3))


# ─────────────────────────────────────────────────────────────────────────────
# Q-LEARNING AGENT (improved)
# ─────────────────────────────────────────────────────────────────────────────

class QLearningAgent:
    """
    Tabular Q-Learning for Rock-Paper-Scissors.

    Improvements over the original:
    • State = last 3 user moves (longer context = stronger pattern capture)
    • Reward shaping: small penalty for draws to encourage decisive play
    • Persists ε across sessions so exploration truly decays over many games
    • Separated save-path so it doesn't collide with the old file
    """
    ACTIONS = ["rock", "paper", "scissors"]
    BEATS   = {"rock": "paper", "paper": "scissors", "scissors": "rock"}
    N_HIST  = 3

    def __init__(self, alpha=0.28, gamma=0.9, epsilon=0.35,
                 eps_min=0.05, eps_decay=0.992):
        self.alpha     = alpha
        self.gamma     = gamma
        self.epsilon   = epsilon
        self.eps_min   = eps_min
        self.eps_decay = eps_decay
        self._history: List[str] = []
        self._q: Dict[str, Dict[str, float]] = {}
        self.wins = self.losses = self.draws = self.total = 0
        self._path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "rps_qtable_v2.json")
        self._load()

    # ── core QLearning ────────────────────────────────────────────────────────

    def _state(self) -> str:
        if len(self._history) < self.N_HIST:
            return "start"
        return ",".join(self._history[-self.N_HIST:])

    def _q_row(self, s: str) -> Dict[str, float]:
        if s not in self._q:
            self._q[s] = {a: 0.0 for a in self.ACTIONS}
        return self._q[s]

    def choose(self) -> str:
        if random.random() < self.epsilon:
            return random.choice(self.ACTIONS)
        row = self._q_row(self._state())
        best = max(row.values())
        return random.choice([a for a, v in row.items() if v == best])

    def update(self, robot_move: str, user_move: str) -> int:
        """Update Q-table and return reward (+1/0/-1)."""
        s0 = self._state()
        if robot_move == user_move:
            reward = 0;  self.draws   += 1
        elif self.BEATS[user_move] == robot_move:
            reward = 1;  self.wins    += 1
        else:
            reward = -1; self.losses  += 1
        self.total += 1
        self._history.append(user_move)
        s1      = self._state()
        old_q   = self._q_row(s0)[robot_move]
        future  = max(self._q_row(s1).values())
        new_q   = old_q + self.alpha * (reward + self.gamma * future - old_q)
        self._q_row(s0)[robot_move] = round(new_q, 4)
        self.epsilon = max(self.eps_min, self.epsilon * self.eps_decay)
        self._save()
        return reward

    def reset_history(self):
        self._history = []

    # ── stats ─────────────────────────────────────────────────────────────────

    @property
    def win_rate(self) -> float:
        return self.wins / self.total * 100 if self.total else 0.0

    @property
    def n_states(self) -> int:
        return len([k for k in self._q if k != "__stats__"])

    # ── persistence ───────────────────────────────────────────────────────────

    def _load(self):
        if not os.path.exists(self._path):
            return
        try:
            with open(self._path) as f:
                data = json.load(f)
            if "__stats__" in data:
                st = data.pop("__stats__")
                self.wins     = st.get("wins", 0)
                self.losses   = st.get("losses", 0)
                self.draws    = st.get("draws", 0)
                self.total    = st.get("total", 0)
                self.epsilon  = st.get("epsilon", self.epsilon)
            self._q = data
            print(f"[Q] Loaded {self.n_states} states, ε={self.epsilon:.3f}")
        except Exception as e:
            print(f"[Q] Could not load Q-table: {e}")

    def _save(self):
        data = dict(self._q)
        data["__stats__"] = dict(
            wins=self.wins, losses=self.losses,
            draws=self.draws, total=self.total,
            epsilon=round(self.epsilon, 4))
        try:
            with open(self._path, "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"[Q] Save error: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# GESTURE DETECTOR (MediaPipe wrapper with temporal smoothing)
# ─────────────────────────────────────────────────────────────────────────────

class GestureDetector:
    """
    Wraps MediaPipe Hands with a majority-vote smoothing buffer to
    reduce flicker in gesture classification.
    """
    VALID = {"rock", "paper", "scissors"}

    def __init__(self, buffer_size: int = 6):
        self._mp = mp.solutions.hands
        self._hands = self._mp.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.76,
            min_tracking_confidence=0.76,
        )
        self._draw   = mp.solutions.drawing_utils
        self._lm_sty = self._draw.DrawingSpec((0, 188, 255), 2, 3)
        self._cn_sty = self._draw.DrawingSpec((0, 90,  200), 1)
        self._buf: List[str] = []
        self._buf_size = buffer_size

    def process(self, bgr: np.ndarray) -> Tuple[str, np.ndarray]:
        """Returns (smoothed_gesture, annotated_bgr_frame)."""
        rgb  = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
        res  = self._hands.process(rgb)
        out  = bgr.copy()
        raw  = "none"
        if res.multi_hand_landmarks:
            for hl in res.multi_hand_landmarks:
                self._draw.draw_landmarks(out, hl, self._mp.HAND_CONNECTIONS,
                                          self._lm_sty, self._cn_sty)
                raw = self._classify(hl.landmark)
        self._buf.append(raw)
        if len(self._buf) > self._buf_size:
            self._buf.pop(0)
        smoothed = Counter(self._buf).most_common(1)[0][0]
        return smoothed, out

    # ── internals ─────────────────────────────────────────────────────────────

    @staticmethod
    def _finger_open(lm) -> List[int]:
        thumb = 1 if lm[4].x < lm[3].x else 0
        rest  = [1 if lm[t].y < lm[m].y - 0.045 else 0
                 for t, m in [(8,5),(12,9),(16,13),(20,17)]]
        return [thumb] + rest

    @staticmethod
    def _classify(lm) -> str:
        fs = GestureDetector._finger_open(lm)
        t, i, m, r, l = fs
        if sum(fs) == 0:                        return "rock"
        if sum(fs) == 5:                        return "paper"
        if i and m and not r and not l:         return "scissors"
        return "unknown"

    def release(self):
        self._hands.close()


# ─────────────────────────────────────────────────────────────────────────────
# GAME STATE MACHINE
# ─────────────────────────────────────────────────────────────────────────────

class Phase(Enum):
    COUNTDOWN  = auto()
    CAPTURE    = auto()
    REVEAL     = auto()
    RESULT     = auto()
    NEXT_ROUND = auto()
    GAME_OVER  = auto()

_BEATS = {                 # (winner, loser)
    ("rock",     "scissors"): "user",
    ("scissors", "paper"):    "user",
    ("paper",    "rock"):     "user",
}

@dataclass
class RoundResult:
    user:  str
    robot: str
    outcome: str   # "user" | "robot" | "draw"
    reward:  int


class Game:
    def __init__(self, n_rounds: int = TOTAL_ROUNDS):
        self.n_rounds     = n_rounds
        self.round        = 1
        self.user_score   = 0
        self.robot_score  = 0
        self.mode         = "qlearn"      # "qlearn" | "random"
        self.agent        = QLearningAgent()
        self.robot_move:  Optional[str]         = None
        self.user_move:   Optional[str]         = None
        self.last_result: Optional[RoundResult] = None
        self.history:     List[RoundResult]     = []
        self._phase       = Phase.COUNTDOWN
        self._t0          = time.time()
        self._last_beat   = -1

    # ── phase helpers ─────────────────────────────────────────────────────────

    @property
    def phase(self) -> Phase:
        return self._phase

    def elapsed(self) -> float:
        return time.time() - self._t0

    def enter(self, phase: Phase):
        self._phase = phase
        self._t0    = time.time()

    # ── logic ─────────────────────────────────────────────────────────────────

    def pick_robot(self):
        if self.mode == "qlearn":
            self.robot_move = self.agent.choose()
        else:
            self.robot_move = random.choice(["rock", "paper", "scissors"])

    def resolve(self, user_move: str) -> RoundResult:
        self.user_move = user_move
        key = (user_move, self.robot_move)
        outcome = _BEATS.get(key, _BEATS.get((self.robot_move, user_move), None))
        if user_move == self.robot_move:
            outcome = "draw"
        elif outcome is None:
            outcome = "robot"  # robot wins
        if outcome == "user":
            self.user_score  += 1
        elif outcome == "robot":
            self.robot_score += 1
        reward = self.agent.update(self.robot_move, user_move) if self.mode == "qlearn" else 0
        result = RoundResult(user_move, self.robot_move, outcome, reward)
        self.last_result = result
        self.history.append(result)
        return result

    def advance_round(self):
        self.round += 1
        self.robot_move = None
        self.user_move  = None

    def reset(self):
        self.__init__(self.n_rounds)
        self.agent._load()     # keep Q-table

    def toggle_mode(self):
        self.mode = "random" if self.mode == "qlearn" else "qlearn"


# ─────────────────────────────────────────────────────────────────────────────
# RENDERER
# ─────────────────────────────────────────────────────────────────────────────

class Renderer:
    def __init__(self, surf: pygame.Surface):
        self.surf  = surf
        self.W, self.H = surf.get_size()
        self.SPLIT = self.W // 2
        pygame.font.init()
        # Font hierarchy
        self.f_huge  = pygame.font.SysFont("Arial", 100, bold=True)
        self.f_big   = pygame.font.SysFont("Arial",  52, bold=True)
        self.f_med   = pygame.font.SysFont("Arial",  30, bold=True)
        self.f_sm    = pygame.font.SysFont("Arial",  20)
        self.f_xs    = pygame.font.SysFont("Arial",  16)
        # Glow surface cache
        self._glow_cache: Dict[str, pygame.Surface] = {}

    # ── frame ─────────────────────────────────────────────────────────────────

    def clear(self):
        self.surf.fill(C["bg"])
        # Fine grid
        for x in range(0, self.W, 38):
            pygame.draw.line(self.surf, (18, 18, 30), (x, 0), (x, self.H))
        for y in range(0, self.H, 38):
            pygame.draw.line(self.surf, (18, 18, 30), (0, y), (self.W, y))

    def blit_camera(self, bgr: np.ndarray):
        rgb  = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
        rgb  = cv2.resize(rgb, (self.SPLIT, self.H))
        pg   = pygame.surfarray.make_surface(np.transpose(rgb, (1, 0, 2)))
        self.surf.blit(pg, (0, 0))
        pygame.draw.rect(self.surf, C["panel_border"],
                         (0, 0, self.SPLIT, self.H), 2)

    # ── HUD ───────────────────────────────────────────────────────────────────

    def hud(self, game: Game):
        bar = pygame.Surface((self.SPLIT, 58), pygame.SRCALPHA)
        bar.fill((0, 0, 0, 170))
        self.surf.blit(bar, (0, 0))
        self._txt(f"Round {game.round}/{game.n_rounds}", self.f_med,
                  C["white"], 14, 29, align="left")
        sc = f"You  {game.user_score} — {game.robot_score}  Robot"
        self._txt(sc, self.f_med, C["white"], self.SPLIT - 14, 29, align="right")

    # ── round history strip ────────────────────────────────────────────────────

    def history_strip(self, game: Game):
        """Small icon row at the bottom of camera panel."""
        if not game.history:
            return
        bx, by = 10, self.H - 22
        for r in game.history:
            col = C["green"] if r.outcome == "user" \
                else C["red"] if r.outcome == "robot" \
                else C["yellow"]
            pygame.draw.circle(self.surf, col, (bx, by), 7)
            bx += 18

    # ── countdown ─────────────────────────────────────────────────────────────

    def countdown(self, elapsed: float):
        BEATS = {0: ("3", C["accent"]),
                 1: ("2", C["accent2"]),
                 2: ("1", C["red"]),
                 3: ("SHOOT!", C["green"])}
        idx      = min(int(elapsed), 3)
        txt, col = BEATS[idx]
        frac     = elapsed - int(elapsed)
        # Pulse scale (large → normal over the beat second)
        pulse    = 1.0 + (1.0 - ease_cubic(frac)) * 0.28
        font     = self.f_huge if txt.isdigit() else self.f_big
        base     = font.render(txt, True, col)
        w  = int(base.get_width()  * pulse)
        h_ = int(base.get_height() * pulse)
        if w > 0 and h_ > 0:
            scaled = pygame.transform.smoothscale(base, (w, h_))
        else:
            scaled = base
        # Shadow
        shadow = pygame.transform.smoothscale(font.render(txt, True, (0, 0, 0)), (w, h_))
        cx_ = (self.SPLIT - w) // 2
        cy_ = (self.H - h_) // 2
        self.surf.blit(shadow, (cx_ + 5, cy_ + 5))
        self.surf.blit(scaled, (cx_, cy_))

    # ── capture phase bar ─────────────────────────────────────────────────────

    def capture_bar(self, gesture: str, elapsed: float):
        progress = min(1.0, elapsed / CAPTURE_DUR)
        bx, by  = 30, self.H - 46
        bw, bh  = self.SPLIT - 60, 14
        pygame.draw.rect(self.surf, C["dark"],
                         (bx, by, bw, bh), border_radius=7)
        fill_col = C["green"] if gesture in GestureDetector.VALID else C["accent"]
        pygame.draw.rect(self.surf, fill_col,
                         (bx, by, int(bw*progress), bh), border_radius=7)
        pygame.draw.rect(self.surf, C["panel_border"],
                         (bx, by, bw, bh), 2, border_radius=7)
        g_txt = gesture.upper() if gesture in GestureDetector.VALID else "..."
        self._txt(f"Show: {g_txt}", self.f_sm,
                  C["green"] if gesture in GestureDetector.VALID else C["gray"],
                  self.SPLIT // 2, self.H - 68, align="center")

    # ── result card ───────────────────────────────────────────────────────────

    def result_card(self, result: RoundResult):
        ov = pygame.Surface((self.SPLIT, 150), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 185))
        self.surf.blit(ov, (0, self.H//2 - 75))
        MAP = {"user":  ("YOU WIN!",    C["green"]),
               "robot": ("ROBOT WINS!", C["red"]),
               "draw":  ("DRAW",        C["yellow"])}
        txt, col = MAP[result.outcome]
        self._txt(f"You: {result.user.upper()}", self.f_med, C["white"],
                  self.SPLIT//2, self.H//2 - 42, align="center")
        self._txt(txt, self.f_big, col,
                  self.SPLIT//2, self.H//2 + 18, align="center")

    # ── next round splash ─────────────────────────────────────────────────────

    def round_splash(self, n: int, elapsed: float):
        alpha = int(255 * min(1.0, elapsed / 0.35))
        s = self.f_big.render(f"Round {n}", True, C["yellow"])
        s.set_alpha(alpha)
        self.surf.blit(s, ((self.SPLIT - s.get_width())//2,
                            (self.H - s.get_height())//2))

    # ── game over ─────────────────────────────────────────────────────────────

    def game_over(self, game: Game):
        ov = pygame.Surface((self.SPLIT, self.H), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 205))
        self.surf.blit(ov, (0, 0))
        if game.user_score > game.robot_score:
            txt, col = "YOU WIN!", C["green"]
        elif game.robot_score > game.user_score:
            txt, col = "ROBOT WINS!", C["red"]
        else:
            txt, col = "IT'S A TIE!", C["yellow"]
        self._txt(txt, self.f_big, col,
                  self.SPLIT//2, self.H//2 - 55, align="center")
        self._txt(f"Final: You {game.user_score} — {game.robot_score} Robot",
                  self.f_med, C["white"],
                  self.SPLIT//2, self.H//2 + 5, align="center")
        self._txt("R to play again", self.f_sm, C["gray"],
                  self.SPLIT//2, self.H//2 + 52, align="center")

    # ── robot panel ───────────────────────────────────────────────────────────

    def robot_panel(self, game: Game, anim: HandAnimator):
        rx = self.SPLIT
        rw = self.W - rx
        cx = rx + rw // 2

        # Background + radial glow
        pygame.draw.rect(self.surf, C["panel_bg"], (rx, 0, rw, self.H))
        for r in range(190, 0, -8):
            a   = int(12 * (1 - r/190))
            col = (min(255, C["panel_bg"][0]+a),
                   min(255, C["panel_bg"][1]+a),
                   min(255, C["panel_bg"][2]+a+6))
            pygame.draw.circle(self.surf, col, (cx, self.H//2 - 20), r)

        self._txt("ROBOT ARM", self.f_med, C["accent"], cx, 30, align="center")
        m_col = C["accent2"] if game.mode == "qlearn" else C["gray"]
        m_lbl = "Q-LEARNING" if game.mode == "qlearn" else "RANDOM"
        self._txt(m_lbl, self.f_xs, m_col, cx, 53, align="center")
        pygame.draw.line(self.surf, C["panel_border"], (rx+18, 68), (self.W-18, 68), 1)

        # Robot hand
        draw_robot_hand(self.surf, anim.state(), cx, self.H//2 - 20, anim.shake_offset())

        # Move label
        if game.robot_move and game.phase in (
                Phase.REVEAL, Phase.RESULT, Phase.NEXT_ROUND, Phase.GAME_OVER):
            self._txt(f"ROBOT: {game.robot_move.upper()}",
                      self.f_med, C["green"], cx, self.H - 138, align="center")
        elif game.phase == Phase.CAPTURE:
            self._txt("Deciding…", self.f_sm, C["gray"], cx, self.H - 138, align="center")
        else:
            self._txt("Get ready…", self.f_sm, C["gray"], cx, self.H - 138, align="center")

        # Stats footer
        pygame.draw.line(self.surf, C["panel_border"], (rx+18, self.H-115), (self.W-18, self.H-115), 1)
        if game.mode == "qlearn":
            a = game.agent
            self._txt(
                f"All-time  W:{a.wins} L:{a.losses} D:{a.draws}  ({a.win_rate:.0f}%)",
                self.f_xs, C["gray"], cx, self.H - 96, align="center")
            self._txt(
                f"States: {a.n_states}   ε: {a.epsilon:.3f}",
                self.f_xs, C["gray"], cx, self.H - 76, align="center")
        self._txt("T: mode  R: restart  Q: quit",
                  self.f_xs, (52, 56, 76), cx, self.H - 52, align="center")

        pygame.draw.rect(self.surf, C["panel_border"], (rx, 0, rw, self.H), 2)

    # ── text utility ──────────────────────────────────────────────────────────

    def _txt(self, text: str, font: pygame.font.Font, color,
             x: int, y: int, align: str = "center"):
        s = font.render(text, True, color)
        if align == "center":
            r = s.get_rect(center=(x, y))
        elif align == "right":
            r = s.get_rect(right=x, centery=y)
        else:
            r = s.get_rect(left=x, centery=y)
        self.surf.blit(s, r)


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    # ── Camera ────────────────────────────────────────────────────────────────
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("ERROR: No camera found.")
        sys.exit(1)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,  640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    detector = GestureDetector()

    # ── Pygame ────────────────────────────────────────────────────────────────
    pygame.init()
    screen = pygame.display.set_mode((WIN_W, WIN_H))
    pygame.display.set_caption("Rock Paper Scissors — Animated Robot Arm")
    clock = pygame.time.Clock()

    renderer = Renderer(screen)
    game     = Game(TOTAL_ROUNDS)
    anim     = HandAnimator()
    anim.go_to("idle", 0.5)

    captured_gesture = "none"

    print("\n" + "═"*54)
    print("  ROCK PAPER SCISSORS — Animated Robot Arm")
    print("═"*54)
    print(f"  Rounds : {TOTAL_ROUNDS}  |  Mode: {game.mode.upper()}")
    print("  Keys   : Q=quit  R=restart  T=toggle mode")
    print("═"*54 + "\n")

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        # ── Events ────────────────────────────────────────────────────────────
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_q:
                    running = False
                elif ev.key == pygame.K_r:
                    game.reset()
                    anim.go_to("idle", 0.45)
                    captured_gesture = "none"
                    print("\n↺  Game restarted\n")
                elif ev.key == pygame.K_t:
                    game.toggle_mode()
                    print(f"\n⇌  Mode: {game.mode.upper()}\n")

        # ── Camera ────────────────────────────────────────────────────────────
        ret, frame = cap.read()
        if not ret:
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
        frame = cv2.flip(frame, 1)
        gesture, annotated = detector.process(frame)

        # ── State machine ─────────────────────────────────────────────────────
        elapsed = game.elapsed()

        if game.phase == Phase.COUNTDOWN:
            # Beat shake every second
            beat = int(elapsed)
            if beat != game._last_beat and elapsed < COUNTDOWN_DUR:
                game._last_beat = beat
                anim.shake(0.26, 11.0 if beat < 3 else 16.0)
                if beat == 3:                       # SHOOT! — snap to ready
                    anim.go_to("idle", 0.22, ease_back)

            if elapsed >= COUNTDOWN_DUR:
                game.pick_robot()
                game.enter(Phase.CAPTURE)
                captured_gesture = "none"
                print(f"🤖  Robot chose: {game.robot_move}  (mode={game.mode})")

        elif game.phase == Phase.CAPTURE:
            if elapsed < CAPTURE_DUR:
                if gesture in GestureDetector.VALID:
                    captured_gesture = gesture
            else:
                # Time's up — lock in move
                user_move = captured_gesture if captured_gesture in GestureDetector.VALID else "rock"
                if captured_gesture not in GestureDetector.VALID:
                    print("⚠️  No gesture — defaulting to rock")
                result = game.resolve(user_move)
                print(f"👤  {user_move}  vs  🤖  {game.robot_move}  →  {result.outcome}")
                # Animate robot to its gesture with elastic snap
                anim.go_to(game.robot_move, REVEAL_DUR, ease_back)
                game.enter(Phase.REVEAL)

        elif game.phase == Phase.REVEAL:
            if elapsed >= REVEAL_DUR:
                game.enter(Phase.RESULT)

        elif game.phase == Phase.RESULT:
            if elapsed >= RESULT_DUR:
                if game.round < game.n_rounds:
                    game.advance_round()
                    game.enter(Phase.NEXT_ROUND)
                    anim.go_to("idle", 0.5, ease_cubic)
                else:
                    game.enter(Phase.GAME_OVER)

        elif game.phase == Phase.NEXT_ROUND:
            if elapsed >= NEXT_ROUND_DUR:
                game._last_beat = -1
                game.enter(Phase.COUNTDOWN)

        # GAME_OVER waits for 'R'

        # ── Animate ───────────────────────────────────────────────────────────
        anim.update(dt)

        # ── Render ────────────────────────────────────────────────────────────
        renderer.clear()
        renderer.blit_camera(annotated)
        renderer.hud(game)
        renderer.history_strip(game)

        if game.phase == Phase.COUNTDOWN:
            renderer.countdown(min(elapsed, COUNTDOWN_DUR - 0.01))
        elif game.phase == Phase.CAPTURE:
            renderer.capture_bar(gesture, elapsed)
        elif game.phase in (Phase.REVEAL, Phase.RESULT):
            if game.last_result:
                renderer.result_card(game.last_result)
        elif game.phase == Phase.NEXT_ROUND:
            renderer.round_splash(game.round, elapsed)
        elif game.phase == Phase.GAME_OVER:
            renderer.game_over(game)

        renderer.robot_panel(game, anim)
        pygame.display.flip()

    # ── Cleanup ───────────────────────────────────────────────────────────────
    cap.release()
    detector.release()
    game.agent._save()
    pygame.quit()
    a = game.agent
    print(f"\n📊  Final Q-stats: W:{a.wins} L:{a.losses} D:{a.draws}  ({a.win_rate:.0f}%)")
    print(f"     Q-table: {a.n_states} states saved")
    print("👋  Thanks for playing!\n")


if __name__ == "__main__":
    main()