# RPS Robot Arm Simulation — Enhancement Walkthrough

## Key Issues in the Original Implementation

### 1. **Instant State Changes — No Animation**
The single biggest weakness. When the robot reveals its gesture, the hand *snaps* instantly from idle → rock/paper/scissors. Each gesture is a completely independent drawing function (`draw_robot_hand_rock`, `draw_robot_hand_paper`, etc.) with hardcoded polygon coordinates. There is zero interpolation between states — the visual jumps from one static image to another.

### 2. **Non-Articulated Hand Model**
Each gesture is drawn as a set of raw OpenCV polygons/lines with manually computed coordinates. This means:
- Every new gesture requires duplicating ~40 lines of drawing code
- You **cannot** smoothly morph between gestures because the shapes have different topologies
- The coordinates are arbitrary pixel offsets, not derived from any skeletal model

### 3. **No Gesture Stabilisation**
The original accepts the **first valid gesture** detected in any frame. MediaPipe can flicker between states (e.g., "scissors" → "unknown" → "scissors" in consecutive frames), causing misdetections. There is no debouncing or stability check.

### 4. **Monolithic Global-Scope Code**
All game state variables (`current_round`, `user_score`, `countdown_start_time`, etc.) are globals. The main loop is a 200-line `while` block with no encapsulation. This makes the code fragile to modify and hard to test.

### 5. **Slow Background Rendering**
The gradient background is drawn pixel-by-pixel with a Python `for` loop over every row — very slow for high resolutions. Should use vectorised NumPy operations.

### 6. **No Anti-Aliasing**
Most `cv2.line()`, `cv2.circle()`, `cv2.polylines()` calls omit `cv2.LINE_AA`, resulting in visible jaggies on the robot hand.

---

## Design Improvements

### 🦾 Articulated Skeletal Hand Model

**Before:** 4 separate functions, each ~40 lines, drawing static polygons.
**After:** A single `HandRenderer` class that draws any pose via **forward kinematics**.

Each finger is defined by a skeleton:
```python
FINGERS = {
    'index': dict(base=(-30,-35), angle=-1.65, l1=38, l2=32, w=11, cr1=1.80, cr2=1.50),
    ...
}
```

Each finger is two segments (proximal + distal) whose angles are derived from a `curl` parameter (0.0 = extended, 1.0 = curled):

```
angle₁ = rest_angle + spread × 0.4 + curl × curl_range₁
angle₂ = angle₁ + curl × curl_range₂
```

Joint positions are computed with `cos`/`sin` (forward kinematics):
```
mid = base + (cos(a₁), sin(a₁)) × length₁
tip = mid  + (cos(a₂), sin(a₂)) × length₂
```

This means **any gesture is just a set of 5 `(curl, spread)` values**, and any two gestures can be smoothly interpolated.

---

### 🎬 Smooth Animation with Eased Interpolation

The `AnimationController` manages transitions:

```python
anim.transition_to("paper", duration=0.45)
```

Every frame calls `anim.update()`, which:
1. Computes elapsed time since transition started
2. Applies cubic ease-in-out: `4t³` for t<0.5, `1 - (-2t+2)³/2` otherwise
3. Lerps every finger parameter between source and target poses
4. Returns the interpolated `HandPose` that the renderer draws

The easing function gives natural-feeling motion — slow start, fast middle, gentle landing.

---

### 👊 Countdown Fist Pumping

**Before:** Static idle hand during countdown.
**After:** Robot forms a fist and *pumps it up and down*, synced to the "3… 2… 1…" beat.

```python
if self.pumping:
    phase = now * pump_speed * 2π
    self.current.wrist_y = sin(phase) * amplitude
```

After "SHOOT!", there's a brief 150ms freeze (dramatic pause), then the hand rapidly animates to the chosen gesture over 450ms. This **"reveal"** effect makes the game feel much more dynamic.

---

### 🎯 Gesture Stabiliser

New `GestureStabiliser` class requires the same gesture for **4 consecutive frames** before accepting:

```python
stable_move = stabiliser.update(raw_move)
```

This prevents flicker-based misdetections where MediaPipe briefly classifies a gesture differently for a single frame.

---

### 🏗️ Better Code Structure

| Aspect | Before | After |
|---|---|---|
| Hand drawing | 4 separate functions, ~170 lines | 1 `HandRenderer` class, ~80 lines |
| Animation | None | `AnimationController` with easing |
| Poses | Hardcoded polygons | `HandPose` dataclass — 5 curl/spread values |
| Gesture detection | Raw, no stabilisation | `GestureStabiliser` with frame buffering |
| Globals | ~15 mutable globals | All encapsulated in `main()` |
| Background | Pixel-by-pixel loop | Vectorised NumPy `linspace` |
| Anti-aliasing | Missing | `cv2.LINE_AA` on all primitives |

---

## Changes Made

- [rps_sim-final.py](file:///Users/naish/Desktop/College/Sem6/rps_sim-final.py) — Complete rewrite

render_diffs(file:///Users/naish/Desktop/College/Sem6/rps_sim-final.py)

## Verification

- ✅ Syntax check passed (`py_compile`)
- ⚠️ Full runtime test requires webcam + MediaPipe — run with `python3 rps_sim-final.py`
