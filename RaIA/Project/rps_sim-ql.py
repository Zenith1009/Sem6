"""
Rock Paper Scissors - Robot Arm Simulation
==========================================
Simulates a robot arm playing RPS against the user.
- User shows gesture via webcam (detected using MediaPipe)
- Robot arm is rendered on-screen (no hardware needed)
- Two modes: Random or Q-Learning (press 'T' to toggle)
- Q-Learning agent learns user patterns across sessions
- 5 rounds, best score wins

Dependencies: opencv-python, mediapipe, numpy
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

# ==============================
# Initialize MediaPipe Hand Detector
# ==============================
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_drawing = mp.solutions.drawing_utils

# ==============================
# Q-Learning Agent
# ==============================

class QLearningAgent:
    """
    Q-Learning agent for Rock Paper Scissors.
    
    State:  Tuple of the user's last 2 moves (e.g., ("rock", "scissors")).
            This captures short-term patterns in human play.
    Action: The robot's move — "rock", "paper", or "scissors".
    Reward: +1 for a win, 0 for a draw, -1 for a loss.
    
    The agent uses an epsilon-greedy policy:
      - With probability epsilon, explore (random move)
      - Otherwise, exploit (pick the move with highest Q-value for current state)
    
    The Q-table is saved to a JSON file so the robot improves across sessions.
    """
    
    ACTIONS = ["rock", "paper", "scissors"]
    # What beats what: maps user_move -> robot counter-move
    COUNTER = {"rock": "paper", "paper": "scissors", "scissors": "rock"}
    
    def __init__(self, alpha=0.3, gamma=0.9, epsilon=0.3, epsilon_min=0.05,
                 epsilon_decay=0.995, q_table_path=None):
        """
        Args:
            alpha:         Learning rate (how much new info overrides old)
            gamma:         Discount factor (importance of future rewards)
            epsilon:       Initial exploration rate
            epsilon_min:   Minimum exploration rate
            epsilon_decay: Multiply epsilon by this after each round
            q_table_path:  File path to persist Q-table
        """
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        
        # Default path: same directory as this script
        if q_table_path is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            self.q_table_path = os.path.join(script_dir, "rps_qtable.json")
        else:
            self.q_table_path = q_table_path
        
        # History of user moves (for building state)
        self.user_history = []
        
        # Statistics
        self.total_rounds = 0
        self.wins = 0
        self.losses = 0
        self.draws = 0
        
        # Load Q-table from disk (or start fresh)
        self.q_table = self._load_q_table()
    
    def _state_key(self):
        """Build current state from last 2 user moves."""
        if len(self.user_history) < 3:
            # Not enough history — use a special initial state
            return "initial"
        return f"{self.user_history[-3]},{self.user_history[-2]},{self.user_history[-1]}"
    
    def _get_q_values(self, state):
        """Get Q-values for a state, initializing if needed."""
        if state not in self.q_table:
            self.q_table[state] = {a: 0.0 for a in self.ACTIONS}
        return self.q_table[state]
    
    def choose_action(self):
        """Choose robot's move using epsilon-greedy policy."""
        state = self._state_key()
        
        if random.random() < self.epsilon:
            # Explore: random move
            return random.choice(self.ACTIONS)
        else:
            # Exploit: pick move with highest Q-value
            q_values = self._get_q_values(state)
            max_q = max(q_values.values())
            # Break ties randomly
            best_actions = [a for a, q in q_values.items() if q == max_q]
            return random.choice(best_actions)
    
    def get_reward(self, robot_move, user_move):
        """Calculate reward: +1 win, 0 draw, -1 loss."""
        if robot_move == user_move:
            return 0
        elif self.COUNTER[user_move] == robot_move:
            return 1   # Robot wins
        else:
            return -1  # Robot loses
    
    def update(self, robot_move, user_move):
        """
        Update Q-table after a round.
        The key insight: we use the state BEFORE this round to update,
        and the state AFTER (with the new user move added) for the
        future Q-value estimate.
        """
        state_before = self._state_key()
        reward = self.get_reward(robot_move, user_move)
        
        # Record user move
        self.user_history.append(user_move)
        
        # Update stats
        self.total_rounds += 1
        if reward > 0:
            self.wins += 1
        elif reward < 0:
            self.losses += 1
        else:
            self.draws += 1
        
        # Q-learning update: Q(s,a) = Q(s,a) + α[r + γ·max(Q(s',a')) - Q(s,a)]
        state_after = self._state_key()
        q_before = self._get_q_values(state_before)
        q_after = self._get_q_values(state_after)
        
        old_q = q_before[robot_move]
        future_q = max(q_after.values())
        new_q = old_q + self.alpha * (reward + self.gamma * future_q - old_q)
        q_before[robot_move] = round(new_q, 4)
        
        # Decay epsilon (reduce exploration over time)
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
        
        # Save Q-table
        self._save_q_table()
        
        return reward
    
    def _load_q_table(self):
        """Load Q-table from JSON file."""
        if os.path.exists(self.q_table_path):
            try:
                with open(self.q_table_path, 'r') as f:
                    data = json.load(f)
                    # Restore stats if saved
                    if "__stats__" in data:
                        stats = data.pop("__stats__")
                        self.total_rounds = stats.get("total_rounds", 0)
                        self.wins = stats.get("wins", 0)
                        self.losses = stats.get("losses", 0)
                        self.draws = stats.get("draws", 0)
                        self.epsilon = stats.get("epsilon", self.epsilon)
                    print(f"Loaded Q-table ({len(data)} states, {self.total_rounds} rounds played)")
                    return data
            except (json.JSONDecodeError, IOError):
                pass
        print("Starting with fresh Q-table")
        return {}
    
    def _save_q_table(self):
        """Save Q-table to JSON file."""
        data = dict(self.q_table)
        data["__stats__"] = {
            "total_rounds": self.total_rounds,
            "wins": self.wins,
            "losses": self.losses,
            "draws": self.draws,
            "epsilon": round(self.epsilon, 4)
        }
        try:
            with open(self.q_table_path, 'w') as f:
                json.dump(data, f, indent=2)
        except IOError as e:
            print(f"Could not save Q-table: {e}")
    
    def reset_history(self):
        """Reset move history for a new game (keeps Q-table and stats)."""
        self.user_history = []
    
    def get_stats_text(self):
        """Return a formatted stats string."""
        if self.total_rounds == 0:
            return "No data yet"
        win_rate = (self.wins / self.total_rounds) * 100
        return f"W:{self.wins} L:{self.losses} D:{self.draws} ({win_rate:.0f}%)"
    
    def get_q_table_size(self):
        """Number of states learned."""
        return len([k for k in self.q_table if k != "__stats__"])


# Initialize Q-learning agent
q_agent = QLearningAgent()

# Mode: "random" or "qlearn"
robot_mode = "qlearn"

# ==============================
# Robot Hand Drawing Functions
# ==============================

def draw_robot_hand_rock(canvas, cx, cy, scale=1.0):
    """Draw a closed fist (rock) - all fingers curled"""
    s = scale
    # Palm (rounded rectangle)
    palm_pts = np.array([
        [cx - int(50*s), cy + int(60*s)],
        [cx - int(55*s), cy - int(10*s)],
        [cx - int(40*s), cy - int(40*s)],
        [cx + int(40*s), cy - int(40*s)],
        [cx + int(55*s), cy - int(10*s)],
        [cx + int(50*s), cy + int(60*s)],
    ], np.int32)
    cv2.fillPoly(canvas, [palm_pts], (180, 180, 190))
    cv2.polylines(canvas, [palm_pts], True, (120, 120, 130), 2)

    # Curled fingers (small arcs on top of palm)
    knuckle_positions = [
        (cx - int(30*s), cy - int(40*s)),
        (cx - int(10*s), cy - int(45*s)),
        (cx + int(10*s), cy - int(45*s)),
        (cx + int(30*s), cy - int(40*s)),
    ]
    for kx, ky in knuckle_positions:
        cv2.ellipse(canvas, (kx, ky), (int(12*s), int(15*s)), 0, 180, 360, (170, 170, 180), -1)
        cv2.ellipse(canvas, (kx, ky), (int(12*s), int(15*s)), 0, 180, 360, (120, 120, 130), 2)

    # Thumb curled across
    thumb_pts = np.array([
        [cx - int(55*s), cy - int(5*s)],
        [cx - int(65*s), cy - int(20*s)],
        [cx - int(55*s), cy - int(35*s)],
        [cx - int(40*s), cy - int(25*s)],
        [cx - int(45*s), cy - int(10*s)],
    ], np.int32)
    cv2.fillPoly(canvas, [thumb_pts], (175, 175, 185))
    cv2.polylines(canvas, [thumb_pts], True, (120, 120, 130), 2)

    # Wrist
    wrist_pts = np.array([
        [cx - int(40*s), cy + int(60*s)],
        [cx - int(35*s), cy + int(100*s)],
        [cx + int(35*s), cy + int(100*s)],
        [cx + int(40*s), cy + int(60*s)],
    ], np.int32)
    cv2.fillPoly(canvas, [wrist_pts], (160, 160, 170))
    cv2.polylines(canvas, [wrist_pts], True, (120, 120, 130), 2)


def draw_robot_hand_paper(canvas, cx, cy, scale=1.0):
    """Draw an open hand (paper) - all fingers extended"""
    s = scale
    # Wrist
    wrist_pts = np.array([
        [cx - int(35*s), cy + int(60*s)],
        [cx - int(30*s), cy + int(100*s)],
        [cx + int(30*s), cy + int(100*s)],
        [cx + int(35*s), cy + int(60*s)],
    ], np.int32)
    cv2.fillPoly(canvas, [wrist_pts], (160, 160, 170))
    cv2.polylines(canvas, [wrist_pts], True, (120, 120, 130), 2)

    # Palm
    palm_pts = np.array([
        [cx - int(50*s), cy + int(60*s)],
        [cx - int(50*s), cy - int(20*s)],
        [cx - int(35*s), cy - int(35*s)],
        [cx + int(35*s), cy - int(35*s)],
        [cx + int(50*s), cy - int(20*s)],
        [cx + int(50*s), cy + int(60*s)],
    ], np.int32)
    cv2.fillPoly(canvas, [palm_pts], (180, 180, 190))
    cv2.polylines(canvas, [palm_pts], True, (120, 120, 130), 2)

    # Five extended fingers
    finger_data = [
        # (base_x_offset, base_y_offset, tip_x_offset, tip_y_offset, width)
        (-35, -35, -55, -110, 11),   # index
        (-12, -35, -15, -120, 11),   # middle
        (12,  -35,  15, -115, 11),   # ring
        (35,  -35,  50, -100, 10),   # little
    ]
    for bx_off, by_off, tx_off, ty_off, w in finger_data:
        bx, by = cx + int(bx_off*s), cy + int(by_off*s)
        tx, ty = cx + int(tx_off*s), cy + int(ty_off*s)
        # Draw finger as a thick rounded line
        cv2.line(canvas, (bx, by), (tx, ty), (180, 180, 190), int(w*s*2))
        cv2.line(canvas, (bx, by), (tx, ty), (120, 120, 130), 2)
        # Fingertip circle
        cv2.circle(canvas, (tx, ty), int(w*s), (185, 185, 195), -1)
        cv2.circle(canvas, (tx, ty), int(w*s), (120, 120, 130), 2)
        # Joint circles
        mid_x, mid_y = (bx + tx) // 2, (by + ty) // 2
        cv2.circle(canvas, (mid_x, mid_y), int(4*s), (150, 150, 160), -1)

    # Thumb (angled outward)
    thumb_base = (cx - int(50*s), cy - int(10*s))
    thumb_mid = (cx - int(70*s), cy - int(40*s))
    thumb_tip = (cx - int(75*s), cy - int(70*s))
    cv2.line(canvas, thumb_base, thumb_mid, (180, 180, 190), int(13*s*2))
    cv2.line(canvas, thumb_mid, thumb_tip, (180, 180, 190), int(11*s*2))
    cv2.line(canvas, thumb_base, thumb_mid, (120, 120, 130), 2)
    cv2.line(canvas, thumb_mid, thumb_tip, (120, 120, 130), 2)
    cv2.circle(canvas, thumb_tip, int(11*s), (185, 185, 195), -1)
    cv2.circle(canvas, thumb_tip, int(11*s), (120, 120, 130), 2)
    cv2.circle(canvas, thumb_mid, int(4*s), (150, 150, 160), -1)


def draw_robot_hand_scissors(canvas, cx, cy, scale=1.0):
    """Draw scissors gesture - index and middle extended, rest curled"""
    s = scale
    # Wrist
    wrist_pts = np.array([
        [cx - int(35*s), cy + int(60*s)],
        [cx - int(30*s), cy + int(100*s)],
        [cx + int(30*s), cy + int(100*s)],
        [cx + int(35*s), cy + int(60*s)],
    ], np.int32)
    cv2.fillPoly(canvas, [wrist_pts], (160, 160, 170))
    cv2.polylines(canvas, [wrist_pts], True, (120, 120, 130), 2)

    # Palm
    palm_pts = np.array([
        [cx - int(50*s), cy + int(60*s)],
        [cx - int(50*s), cy - int(15*s)],
        [cx - int(35*s), cy - int(35*s)],
        [cx + int(35*s), cy - int(35*s)],
        [cx + int(50*s), cy - int(15*s)],
        [cx + int(50*s), cy + int(60*s)],
    ], np.int32)
    cv2.fillPoly(canvas, [palm_pts], (180, 180, 190))
    cv2.polylines(canvas, [palm_pts], True, (120, 120, 130), 2)

    # Index finger (extended, slight V angle)
    idx_base = (cx - int(25*s), cy - int(35*s))
    idx_tip = (cx - int(35*s), cy - int(120*s))
    cv2.line(canvas, idx_base, idx_tip, (180, 180, 190), int(11*s*2))
    cv2.line(canvas, idx_base, idx_tip, (120, 120, 130), 2)
    cv2.circle(canvas, idx_tip, int(11*s), (185, 185, 195), -1)
    cv2.circle(canvas, idx_tip, int(11*s), (120, 120, 130), 2)
    mid_x, mid_y = (idx_base[0] + idx_tip[0]) // 2, (idx_base[1] + idx_tip[1]) // 2
    cv2.circle(canvas, (mid_x, mid_y), int(4*s), (150, 150, 160), -1)

    # Middle finger (extended, slight V angle)
    mid_base = (cx + int(5*s), cy - int(35*s))
    mid_tip = (cx + int(15*s), cy - int(120*s))
    cv2.line(canvas, mid_base, mid_tip, (180, 180, 190), int(11*s*2))
    cv2.line(canvas, mid_base, mid_tip, (120, 120, 130), 2)
    cv2.circle(canvas, mid_tip, int(11*s), (185, 185, 195), -1)
    cv2.circle(canvas, mid_tip, int(11*s), (120, 120, 130), 2)
    mid_x, mid_y = (mid_base[0] + mid_tip[0]) // 2, (mid_base[1] + mid_tip[1]) // 2
    cv2.circle(canvas, (mid_x, mid_y), int(4*s), (150, 150, 160), -1)

    # Ring finger curled
    cv2.ellipse(canvas, (cx + int(25*s), cy - int(35*s)), (int(12*s), int(15*s)),
                0, 180, 360, (170, 170, 180), -1)
    cv2.ellipse(canvas, (cx + int(25*s), cy - int(35*s)), (int(12*s), int(15*s)),
                0, 180, 360, (120, 120, 130), 2)

    # Little finger curled
    cv2.ellipse(canvas, (cx + int(42*s), cy - int(25*s)), (int(10*s), int(13*s)),
                0, 180, 360, (170, 170, 180), -1)
    cv2.ellipse(canvas, (cx + int(42*s), cy - int(25*s)), (int(10*s), int(13*s)),
                0, 180, 360, (120, 120, 130), 2)

    # Thumb curled
    thumb_pts = np.array([
        [cx - int(50*s), cy - int(5*s)],
        [cx - int(62*s), cy - int(18*s)],
        [cx - int(52*s), cy - int(30*s)],
        [cx - int(40*s), cy - int(22*s)],
        [cx - int(42*s), cy - int(8*s)],
    ], np.int32)
    cv2.fillPoly(canvas, [thumb_pts], (175, 175, 185))
    cv2.polylines(canvas, [thumb_pts], True, (120, 120, 130), 2)


def draw_robot_hand_idle(canvas, cx, cy, scale=1.0):
    """Draw a neutral/relaxed hand pose (slightly open)"""
    s = scale
    # Wrist
    wrist_pts = np.array([
        [cx - int(35*s), cy + int(55*s)],
        [cx - int(30*s), cy + int(95*s)],
        [cx + int(30*s), cy + int(95*s)],
        [cx + int(35*s), cy + int(55*s)],
    ], np.int32)
    cv2.fillPoly(canvas, [wrist_pts], (160, 160, 170))
    cv2.polylines(canvas, [wrist_pts], True, (120, 120, 130), 2)

    # Palm
    palm_pts = np.array([
        [cx - int(48*s), cy + int(55*s)],
        [cx - int(45*s), cy - int(15*s)],
        [cx - int(30*s), cy - int(30*s)],
        [cx + int(30*s), cy - int(30*s)],
        [cx + int(45*s), cy - int(15*s)],
        [cx + int(48*s), cy + int(55*s)],
    ], np.int32)
    cv2.fillPoly(canvas, [palm_pts], (180, 180, 190))
    cv2.polylines(canvas, [palm_pts], True, (120, 120, 130), 2)

    # Slightly curled fingers (relaxed, semi-open)
    finger_data = [
        (-30, -30, -40, -70, 10),
        (-10, -30, -12, -75, 10),
        (10,  -30,  12, -72, 10),
        (30,  -28,  38, -62, 9),
    ]
    for bx_off, by_off, tx_off, ty_off, w in finger_data:
        bx, by = cx + int(bx_off*s), cy + int(by_off*s)
        tx, ty = cx + int(tx_off*s), cy + int(ty_off*s)
        cv2.line(canvas, (bx, by), (tx, ty), (180, 180, 190), int(w*s*2))
        cv2.line(canvas, (bx, by), (tx, ty), (120, 120, 130), 2)
        cv2.circle(canvas, (tx, ty), int(w*s), (185, 185, 195), -1)
        cv2.circle(canvas, (tx, ty), int(w*s), (120, 120, 130), 2)

    # Thumb relaxed
    thumb_base = (cx - int(45*s), cy - int(5*s))
    thumb_tip = (cx - int(60*s), cy - int(38*s))
    cv2.line(canvas, thumb_base, thumb_tip, (180, 180, 190), int(12*s*2))
    cv2.line(canvas, thumb_base, thumb_tip, (120, 120, 130), 2)
    cv2.circle(canvas, thumb_tip, int(10*s), (185, 185, 195), -1)
    cv2.circle(canvas, thumb_tip, int(10*s), (120, 120, 130), 2)


def draw_robot_panel(frame, robot_choice, game_state, mode="random",
                     agent=None, countdown_val=None, scale=1.0):
    """
    Create a panel showing the robot hand and return it.
    Panel size matches the camera frame height.
    """
    h, w = frame.shape[:2]
    panel_w = int(w * 0.45)
    panel = np.zeros((h, panel_w, 3), dtype=np.uint8)

    # Dark gradient background
    for y in range(h):
        ratio = y / h
        r = int(25 + 15 * ratio)
        g = int(25 + 15 * ratio)
        b = int(35 + 20 * ratio)
        panel[y, :] = (b, g, r)

    # Panel title
    title = "ROBOT ARM"
    font = cv2.FONT_HERSHEY_SIMPLEX
    (tw, th), _ = cv2.getTextSize(title, font, 0.8, 2)
    tx = (panel_w - tw) // 2
    cv2.putText(panel, title, (tx, 35), font, 0.8, (100, 200, 255), 2)

    # Mode indicator
    if mode == "qlearn":
        mode_label = "Q-LEARNING"
        mode_color = (0, 200, 255)  # Orange-yellow
    else:
        mode_label = "RANDOM"
        mode_color = (200, 200, 200)
    (mw, _), _ = cv2.getTextSize(mode_label, font, 0.5, 1)
    cv2.putText(panel, mode_label, ((panel_w - mw)//2, 48), font, 0.5, mode_color, 1)

    # Decorative line under title
    cv2.line(panel, (20, 55), (panel_w - 20, 55), (60, 60, 80), 2)

    # Robot hand center
    hand_cx = panel_w // 2
    hand_cy = h // 2 - 20

    # Draw the robot hand based on game state
    if game_state == "countdown":
        draw_robot_hand_idle(panel, hand_cx, hand_cy, scale)
        # Show "Thinking..." text
        label = "Thinking..."
        (lw, lh), _ = cv2.getTextSize(label, font, 0.7, 2)
        cv2.putText(panel, label, ((panel_w - lw)//2, h - 100), font, 0.7, (150, 150, 200), 2)
    elif game_state in ["show", "result", "next_round", "game_over"]:
        if robot_choice == "rock":
            draw_robot_hand_rock(panel, hand_cx, hand_cy, scale)
        elif robot_choice == "paper":
            draw_robot_hand_paper(panel, hand_cx, hand_cy, scale)
        elif robot_choice == "scissors":
            draw_robot_hand_scissors(panel, hand_cx, hand_cy, scale)
        else:
            draw_robot_hand_idle(panel, hand_cx, hand_cy, scale)

        # Show robot's choice
        if robot_choice:
            choice_label = f"Robot: {robot_choice.upper()}"
            (lw, lh), _ = cv2.getTextSize(choice_label, font, 0.8, 2)
            cv2.putText(panel, choice_label, ((panel_w - lw)//2, h - 100),
                        font, 0.8, (0, 255, 200), 2)
    else:
        draw_robot_hand_idle(panel, hand_cx, hand_cy, scale)

    # Q-Learning stats at the bottom of the panel
    if agent and mode == "qlearn":
        y_start = h - 75
        cv2.line(panel, (20, y_start - 10), (panel_w - 20, y_start - 10), (60, 60, 80), 1)
        
        stats_text = agent.get_stats_text()
        cv2.putText(panel, f"All-time: {stats_text}", (15, y_start + 10),
                    font, 0.4, (180, 180, 200), 1)
        
        states_text = f"States: {agent.get_q_table_size()}  Eps: {agent.epsilon:.2f}"
        cv2.putText(panel, states_text, (15, y_start + 30),
                    font, 0.4, (150, 150, 170), 1)
        
        cv2.putText(panel, "'T' toggle mode", (15, y_start + 50),
                    font, 0.35, (120, 120, 140), 1)

    # Border around panel
    cv2.rectangle(panel, (0, 0), (panel_w - 1, h - 1), (60, 60, 80), 2)

    return panel


# ==============================
# Helper functions (from original)
# ==============================
def get_finger_status(hand_landmarks):
    """Determine which fingers are open (1) or closed (0)"""
    thumb_tip = hand_landmarks[4]
    thumb_ip = hand_landmarks[3]
    thumb_open = 1 if thumb_tip.x < thumb_ip.x else 0

    fingers = [
        {'tip': 8, 'mcp': 5},   # index
        {'tip': 12, 'mcp': 9},  # middle
        {'tip': 16, 'mcp': 13}, # ring
        {'tip': 20, 'mcp': 17}  # little
    ]

    finger_status = [thumb_open]
    for finger in fingers:
        tip_y = hand_landmarks[finger['tip']].y
        mcp_y = hand_landmarks[finger['mcp']].y
        finger_status.append(1 if mcp_y - tip_y > 0.05 else 0)
    return finger_status


def classify_gesture(finger_status):
    """Classify hand gesture as rock, paper, or scissors"""
    thumb, index, middle, ring, little = finger_status
    # Rock: All closed
    if sum(finger_status) == 0:
        return "rock"
    # Paper: All open
    elif sum(finger_status) == 5:
        return "paper"
    # Scissors: Only index & middle open
    elif index == 1 and middle == 1 and ring == 0 and little == 0:
        return "scissors"
    else:
        return "unknown"


def decide_winner(user, robot):
    """Determine the winner of a round"""
    if user == robot:
        return "Draw!", (255, 255, 0)
    elif (user == "rock" and robot == "scissors") or \
         (user == "scissors" and robot == "paper") or \
         (user == "paper" and robot == "rock"):
        return "You Win!", (0, 255, 0)
    else:
        return "Robot Wins!", (0, 100, 255)


def draw_countdown(frame, text, color=(255, 255, 255)):
    """Draw large centered countdown text on the camera feed"""
    font = cv2.FONT_HERSHEY_DUPLEX
    font_scale = 3
    thickness = 5

    (text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, thickness)
    height, width = frame.shape[:2]
    x = (width - text_width) // 2
    y = (height + text_height) // 2

    # Black outline + colored text
    cv2.putText(frame, text, (x, y), font, font_scale, (0, 0, 0), thickness + 3)
    cv2.putText(frame, text, (x, y), font, font_scale, color, thickness)


def draw_hud(frame, current_round, total_rounds, user_score, robot_score):
    """Draw the heads-up display with round info and scores"""
    h, w = frame.shape[:2]
    font = cv2.FONT_HERSHEY_SIMPLEX

    # Semi-transparent overlay at top
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (w, 55), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)

    # Round info
    round_text = f"Round {current_round}/{total_rounds}"
    cv2.putText(frame, round_text, (15, 38), font, 0.9, (255, 255, 255), 2)

    # Scores
    score_text = f"You: {user_score}  |  Robot: {robot_score}"
    (sw, _), _ = cv2.getTextSize(score_text, font, 0.9, 2)
    cv2.putText(frame, score_text, (w - sw - 15, 38), font, 0.9, (255, 255, 255), 2)


def draw_result_overlay(frame, user_move, robot_choice, result_text, result_color):
    """Draw result overlay on the camera frame"""
    h, w = frame.shape[:2]
    font = cv2.FONT_HERSHEY_SIMPLEX

    # Semi-transparent dark overlay
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, h//2 - 80), (w, h//2 + 80), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)

    # User move
    user_text = f"You: {user_move.upper()}"
    (uw, _), _ = cv2.getTextSize(user_text, font, 1.0, 2)
    cv2.putText(frame, user_text, ((w - uw)//2, h//2 - 35), font, 1.0, (0, 255, 200), 2)

    # Result
    (rw, _), _ = cv2.getTextSize(result_text, font, 1.5, 3)
    cv2.putText(frame, result_text, ((w - rw)//2, h//2 + 30), font, 1.5, result_color, 3)


# ==============================
# Game State Variables
# ==============================
TOTAL_ROUNDS = 10
current_round = 1
user_score = 0
robot_score = 0

# Game states
STATE_COUNTDOWN = "countdown"
STATE_SHOW = "show"
STATE_RESULT = "result"
STATE_NEXT_ROUND = "next_round"
STATE_GAME_OVER = "game_over"

game_state = STATE_COUNTDOWN
countdown_start_time = None
robot_choice = None
user_move = None
result_text = ""
result_color = (255, 255, 255)

# ==============================
# Main Loop
# ==============================
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ Cannot open camera. Make sure a webcam is connected.")
    exit(1)

# Set camera resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print("\n" + "="*50)
print("🎮  ROCK PAPER SCISSORS - ROBOT ARM SIMULATION")
print("="*50)
print(f"  Rounds: {TOTAL_ROUNDS}")
print(f"  Mode:   {'Q-Learning' if robot_mode == 'qlearn' else 'Random'}")
print("  Show your gesture when the countdown reaches SHOOT!")
print("  Press 'Q' to quit at any time")
print("  Press 'R' to restart the game")
print("  Press 'T' to toggle Random/Q-Learning mode")
print("="*50 + "\n")

WINDOW_NAME = "Rock Paper Scissors - Robot Arm Simulation"

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    # Draw hand landmarks if detected
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # ==============================
    # STATE: COUNTDOWN (3...2...1...SHOOT!)
    # ==============================
    if game_state == STATE_COUNTDOWN:
        if countdown_start_time is None:
            countdown_start_time = time.time()

        elapsed = time.time() - countdown_start_time

        if elapsed < 1:
            draw_countdown(frame, "3", (0, 255, 255))
        elif elapsed < 2:
            draw_countdown(frame, "2", (0, 165, 255))
        elif elapsed < 3:
            draw_countdown(frame, "1", (0, 100, 255))
        elif elapsed < 4:
            draw_countdown(frame, "SHOOT!", (0, 255, 0))
        else:
            # Transition to SHOW state
            game_state = STATE_SHOW
            countdown_start_time = time.time()
            # Robot chooses based on mode
            if robot_mode == "qlearn":
                robot_choice = q_agent.choose_action()
                print(f"🤖 Robot chose: {robot_choice} (Q-Learning, ε={q_agent.epsilon:.2f})")
            else:
                robot_choice = random.choice(["rock", "paper", "scissors"])
                print(f"🤖 Robot chose: {robot_choice} (Random)")

        # Draw HUD
        draw_hud(frame, current_round, TOTAL_ROUNDS, user_score, robot_score)

    # ==============================
    # STATE: SHOW (Capture user gesture - give 2 second window)
    # ==============================
    elif game_state == STATE_SHOW:
        elapsed = time.time() - countdown_start_time
        user_move = "unknown"

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                finger_status = get_finger_status(hand_landmarks.landmark)
                user_move = classify_gesture(finger_status)

        # Instruction text
        remaining = max(0, 2.0 - elapsed)
        cv2.putText(frame, f"Show your gesture! ({remaining:.1f}s)",
                    (10, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

        # If user made a valid move, or time is up
        if user_move in ["rock", "paper", "scissors"] or elapsed > 2.0:
            if user_move not in ["rock", "paper", "scissors"]:
                user_move = "rock"  # default to rock if no gesture detected
                print("⚠️  No valid gesture detected, defaulting to rock")

            result_text, result_color = decide_winner(user_move, robot_choice)
            if result_text == "You Win!":
                user_score += 1
            elif result_text == "Robot Wins!":
                robot_score += 1

            # Update Q-learning agent
            if robot_mode == "qlearn":
                reward = q_agent.update(robot_choice, user_move)
                reward_str = {1: "👍", 0: "🤝", -1: "👎"}.get(reward, "")
                print(f"👤 You chose: {user_move}")
                print(f"📊 Result: {result_text} {reward_str}")
                print(f"🧠 Q-table states: {q_agent.get_q_table_size()} | ε: {q_agent.epsilon:.3f}")
                print(f"🏆 Score - You: {user_score} | Robot: {robot_score}\n")
            else:
                print(f"👤 You chose: {user_move}")
                print(f"📊 Result: {result_text}")
                print(f"🏆 Score - You: {user_score} | Robot: {robot_score}\n")

            game_state = STATE_RESULT
            countdown_start_time = time.time()

        draw_hud(frame, current_round, TOTAL_ROUNDS, user_score, robot_score)

    # ==============================
    # STATE: RESULT (Show result for 3 seconds)
    # ==============================
    elif game_state == STATE_RESULT:
        elapsed = time.time() - countdown_start_time

        draw_result_overlay(frame, user_move, robot_choice, result_text, result_color)
        draw_hud(frame, current_round, TOTAL_ROUNDS, user_score, robot_score)

        if elapsed > 3:
            if current_round < TOTAL_ROUNDS:
                current_round += 1
                game_state = STATE_NEXT_ROUND
                countdown_start_time = time.time()
            else:
                game_state = STATE_GAME_OVER
                countdown_start_time = time.time()

    # ==============================
    # STATE: NEXT ROUND (Transition message)
    # ==============================
    elif game_state == STATE_NEXT_ROUND:
        elapsed = time.time() - countdown_start_time

        draw_countdown(frame, f"Round {current_round}", (255, 255, 0))
        draw_hud(frame, current_round, TOTAL_ROUNDS, user_score, robot_score)

        if elapsed > 2:
            game_state = STATE_COUNTDOWN
            countdown_start_time = None

    # ==============================
    # STATE: GAME OVER (Final scores)
    # ==============================
    elif game_state == STATE_GAME_OVER:
        h, w = frame.shape[:2]
        font = cv2.FONT_HERSHEY_SIMPLEX

        # Full overlay
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (w, h), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)

        # Determine overall winner
        if user_score > robot_score:
            final_text = "YOU WIN!"
            color = (0, 255, 0)
            emoji = ":)"
        elif robot_score > user_score:
            final_text = "ROBOT WINS!"
            color = (0, 100, 255)
            emoji = ":("
        else:
            final_text = "IT'S A TIE!"
            color = (255, 255, 0)
            emoji = ":|"

        # Title
        (fw, fh), _ = cv2.getTextSize(final_text, cv2.FONT_HERSHEY_DUPLEX, 2.0, 4)
        cv2.putText(frame, final_text, ((w - fw)//2, h//2 - 50),
                    cv2.FONT_HERSHEY_DUPLEX, 2.0, color, 4)

        # Final score
        score_str = f"Final Score   You: {user_score}  -  Robot: {robot_score}"
        (sw, _), _ = cv2.getTextSize(score_str, font, 1.0, 2)
        cv2.putText(frame, score_str, ((w - sw)//2, h//2 + 20),
                    font, 1.0, (255, 255, 255), 2)

        # Instructions
        restart_text = "Press 'R' to play again  |  'Q' to quit"
        (rw, _), _ = cv2.getTextSize(restart_text, font, 0.7, 2)
        cv2.putText(frame, restart_text, ((w - rw)//2, h//2 + 70),
                    font, 0.7, (180, 180, 180), 2)

    # ==============================
    # Build the robot panel and composite
    # ==============================
    robot_panel = draw_robot_panel(frame, robot_choice, game_state,
                                   mode=robot_mode, agent=q_agent, scale=1.2)

    # Add a thin separator
    separator = np.zeros((frame.shape[0], 3, 3), dtype=np.uint8)
    separator[:, :] = (60, 60, 80)

    # Combine: camera feed | separator | robot panel
    combined = np.hstack([frame, separator, robot_panel])

    cv2.imshow(WINDOW_NAME, combined)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('r'):
        # Reset game
        current_round = 1
        user_score = 0
        robot_score = 0
        game_state = STATE_COUNTDOWN
        countdown_start_time = None
        robot_choice = None
        user_move = None
        result_text = ""
        result_color = (255, 255, 255)
        q_agent.reset_history()  # Reset move history, keep Q-table
        print("\n🔄 Game restarted!\n")
    elif key == ord('t'):
        # Toggle mode
        if robot_mode == "random":
            robot_mode = "qlearn"
            print("\n🧠 Switched to Q-LEARNING mode")
            print(f"   Q-table: {q_agent.get_q_table_size()} states | All-time: {q_agent.get_stats_text()}\n")
        else:
            robot_mode = "random"
            print("\n🎲 Switched to RANDOM mode\n")

# ==============================
# Clean up
# ==============================
cap.release()
cv2.destroyAllWindows()
q_agent._save_q_table()  # Final save
print(f"\n📊 Final Q-Learning stats: {q_agent.get_stats_text()}")
print(f"   Q-table saved with {q_agent.get_q_table_size()} states")
print("👋 Thanks for playing!")
