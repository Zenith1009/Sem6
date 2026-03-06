# Comprehensive Explanation of U23CS014_Lab4.ipynb

## Overview
This notebook is an assignment for **Robotics and its Application (AI352)** that covers:
1. **Forward and Inverse Kinematics** for 2-link and n-link planar robot arms
2. **Rotation Matrices** for coordinate transformations in 3D space
3. **Homogeneous Transformations** combining rotation and translation

This is fundamental to robotic manipulator control and motion planning.

---

## Table of Contents
1. [Part A: Forward and Inverse Kinematics](#part-a-forward-and-inverse-kinematics)
2. [Part B: Rotation Matrices and Coordinate Transformations](#part-b-rotation-matrices)
3. [Function Reference](#function-reference)
4. [Variable Dictionary](#variable-dictionary)
5. [Problems and Solutions](#problems-and-solutions)

---

## Part A: Forward and Inverse Kinematics

### Concept Overview

**Forward Kinematics (FK)**: Converts **joint angles** → **end-effector position**
- Input: θ₁, θ₂ (joint angles in radians)
- Output: (x, y) position in Cartesian space
- Always has a unique solution

**Inverse Kinematics (IK)**: Converts **desired position** → **joint angles**
- Input: (x, y) desired position
- Output: θ₁, θ₂ (or multiple solutions)
- May have 0, 1, 2, or infinite solutions depending on robot DOF

### 2R Planar Robot

#### Forward Kinematics: 2R Robot

```python
def forward_kinematics_2r(theta1, theta2, L1, L2):
    x = L1 * np.cos(theta1) + L2 * np.cos(theta1 + theta2)
    y = L1 * np.sin(theta1) + L2 * np.sin(theta1 + theta2)
    return x, y
```

**Mathematical Derivation:**

For a 2-link robot with link lengths L₁ and L₂:

```
Step 1: First joint
  x₁ = L₁·cos(θ₁)
  y₁ = L₁·sin(θ₁)

Step 2: Second joint (relative to first)
  The second link makes angle (θ₁ + θ₂) with X-axis
  x₂ = x₁ + L₂·cos(θ₁ + θ₂)
  y₂ = y₁ + L₂·sin(θ₁ + θ₂)
```

**Parameters:**
- `theta1`: First joint angle (radians)
- `theta2`: Second joint angle relative to first link (radians)
- `L1, L2`: Link lengths (meters)

**Returns:**
- `x, y`: End-effector position in Cartesian coordinates

**Example:**
```
L1 = 1.0, L2 = 1.0
θ₁ = 45°, θ₂ = 30°
→ x ≈ 1.77, y ≈ 1.43
```

#### Inverse Kinematics: 2R Robot

```python
def inverse_kinematics_2r(x, y, L1, L2):
```

**Mathematical Derivation Using Law of Cosines:**

Given target (x, y), we want to find θ₁ and θ₂.

**Step 1: Find θ₂ using distance formula**

The end-effector distance from origin:
$$r^2 = x^2 + y^2$$

By law of cosines in the triangle formed by L₁, L₂, and r:
$$r^2 = L_1^2 + L_2^2 + 2L_1L_2\cos(\theta_2)$$

Solving for θ₂:
$$\cos(\theta_2) = \frac{x^2 + y^2 - L_1^2 - L_2^2}{2L_1L_2}$$

$$\theta_2 = \pm \arccos\left(\frac{x^2 + y^2 - L_1^2 - L_2^2}{2L_1L_2}\right)$$

The **±** sign gives **two solutions**:
- **Positive** (+): Elbow-down configuration
- **Negative** (-): Elbow-up configuration

**Step 2: Find θ₁**

The arm direction to the end-effector:
$$\alpha = \text{atan2}(y, x)$$

The correction angle from L₂:
$$\beta = \text{atan2}(L_2\sin(\theta_2), L_1 + L_2\cos(\theta_2))$$

Therefore:
$$\theta_1 = \alpha - \beta = \text{atan2}(y, x) - \text{atan2}(L_2\sin(\theta_2), L_1 + L_2\cos(\theta_2))$$

**Step 3: Check Reachability**

A point is reachable if and only if:
$$|L_1 - L_2| \leq \sqrt{x^2 + y^2} \leq L_1 + L_2$$

Where:
- **Outer radius**: $R_{out} = L_1 + L_2$ (all links extended)
- **Inner radius**: $R_{in} = |L_1 - L_2|$ (links folded)

**Key Variables in Function:**

```python
d_sq = x**2 + y**2          # Distance squared
d = np.sqrt(d_sq)            # Distance from origin
cos_theta2 = (d_sq - L1**2 - L2**2) / (2 * L1 * L2)  # Cosine of θ₂
cos_theta2 = np.clip(cos_theta2, -1.0, 1.0)  # Clamp to [-1, 1] for numerical stability
```

**Returns:**
- List of solution tuples: `[(θ₁_down, θ₂_down), (θ₁_up, θ₂_up)]`
- Empty list if point is unreachable

#### Plotting 2R Robot

```python
def plot_robot_2r(theta1, theta2, L1, L2, ax=None, title="...", color='blue')
```

**Functionality:**
1. Computes joint positions from FK
2. Draws links as line segments
3. Marks joints with circles and squares
4. Marks end-effector with red star
5. Draws workspace boundaries (circles)

**Variables:**
- `(x0, y0) = (0, 0)`: Base position
- `(x1, y1)`: Position of first joint
- `(x2, y2)`: End-effector position

**Plot Elements:**
- Dashed gray circle at radius $(L_1 + L_2)$: Outer workspace boundary
- Dashed gray circle at radius $|L_1 - L_2|$: Inner workspace boundary

### n-R Planar Robot (Redundant Manipulator)

For robots with **n > 2** links, inverse kinematics becomes **underdetermined** (infinite solutions).

#### Forward Kinematics: n-R Robot

```python
def forward_kinematics_nr(thetas, link_lengths):
```

**Mathematical Formulation:**

For n joints with angles θ = [θ₁, θ₂, ..., θₙ] and link lengths L = [L₁, L₂, ..., Lₙ]:

The cumulative angles are:
$$\phi_i = \sum_{j=1}^{i} \theta_j$$

The end-effector position:
$$x = \sum_{i=1}^{n} L_i \cos(\phi_i)$$
$$y = \sum_{i=1}^{n} L_i \sin(\phi_i)$$

**Key Variables:**

```python
cumulative_angles = np.cumsum(thetas)              # [θ₁, θ₁+θ₂, θ₁+θ₂+θ₃, ...]
x_positions = np.cumsum(link_lengths * np.cos(cumulative_angles))  # Cumulative X
y_positions = np.cumsum(link_lengths * np.sin(cumulative_angles))  # Cumulative Y
X = np.concatenate([[0], x_positions])              # Include base (0, 0)
Y = np.concatenate([[0], y_positions])
```

**Returns:**
- `(x, y)`: End-effector position
- `(X, Y)`: Arrays of all joint positions (for plotting)

#### Jacobian Matrix for n-R Robot

```python
def compute_jacobian_nr(thetas, link_lengths):
```

**Concept:**

The Jacobian matrix relates **joint velocities** to **end-effector velocities**:
$$\dot{\mathbf{p}} = \mathbf{J} \dot{\boldsymbol{\theta}}$$

Where:
- $\dot{\mathbf{p}}$: End-effector velocity [ẋ, ẏ]ᵀ
- $\mathbf{J}$: Jacobian matrix (2×n)
- $\dot{\boldsymbol{\theta}}$: Joint velocities [θ̇₁, θ̇₂, ..., θ̇ₙ]ᵀ

**Jacobian Calculation:**

For each joint i, the contribution to end-effector velocity is:
$$J_{1,i} = -\sum_{j=i}^{n} L_j \sin(\phi_j)$$  (X derivative)
$$J_{2,i} = \sum_{j=i}^{n} L_j \cos(\phi_j)$$   (Y derivative)

**Key Variables:**

```python
J = np.zeros((2, n))                # 2×n Jacobian matrix
cumulative_angles = np.cumsum(thetas)
```

**Returns:**
- Jacobian matrix (2×n array)

#### Inverse Kinematics: n-R Robot (Numerical Method)

```python
def inverse_kinematics_nr(x_target, y_target, link_lengths, initial_thetas=None,
                           max_iterations=1000, tolerance=1e-6, damping=0.1)
```

**Method: Jacobian Pseudo-Inverse (Damped Least Squares)**

This is a **numerical iterative method** that solves the underdetermined IK problem.

**Algorithm:**

1. **Initialize**: Start with zero angles (or provided initial guess)
2. **Compute FK**: Calculate current end-effector position (xc, yc)
3. **Compute Error**: Error = [x_target - xc, y_target - yc]
4. **Check Convergence**: If error < tolerance, done!
5. **Compute Jacobian**: J at current joint configuration
6. **Damped Pseudo-Inverse**: 
   $$\mathbf{J}^{+} = \mathbf{J}^T (\mathbf{J}\mathbf{J}^T + \lambda^2\mathbf{I})^{-1}$$
   where λ is damping factor
7. **Update Angles**: θ ← θ + J⁺ · error
8. **Repeat** until convergence

**Key Variables:**

```python
n = len(link_lengths)                           # Number of joints
max_reach = np.sum(link_lengths)               # Sum of all link lengths
target_dist = np.sqrt(x_target**2 + y_target**2)  # Distance to target
thetas = np.zeros(n)                           # Initial joint angles
```

**Loop Variables:**

```python
x_curr, y_curr = forward_kinematics_nr(thetas, ...)  # Current position
error = np.array([x_target - x_curr, y_target - y_curr])  # Position error
error_magnitude = np.linalg.norm(error)        # ||error||
J = compute_jacobian_nr(thetas, ...)           # Jacobian at current config
JJT = J @ J.T                                  # J·Jᵀ (2×2 matrix)
damped_inverse = J.T @ np.linalg.inv(JJT + damping**2 * np.eye(2))  # Pseudo-inverse
delta_theta = damped_inverse @ error           # Angle increment
```

**Parameters:**
- `x_target, y_target`: Desired end-effector position
- `link_lengths`: Array of link lengths [L₁, L₂, ..., Lₙ]
- `initial_thetas`: Starting joint angles (default: zeros)
- `max_iterations`: Maximum iterations (default: 1000)
- `tolerance`: Convergence threshold (default: 1e-6)
- `damping`: Damping factor λ (default: 0.1)

**Returns:**
- `(thetas, success)`: Final joint angles and convergence status

**Why Damping is Needed:**

At singularities (where Jacobian loses rank), the pseudo-inverse becomes ill-conditioned. The damping term λ prevents numerical instability:
- λ = 0: Pure least-squares (can diverge at singularities)
- λ > 0: Damped least-squares (stable but less accurate near singularities)

#### Plotting n-R Robot

```python
def plot_robot_nr(thetas, link_lengths, ax=None, title="n-R Robot Configuration")
```

Visualizes the n-link chain:
- Draws all links connected end-to-end
- Shows all joint positions
- Displays end-effector as red star
- Indicates maximum reach circle

#### Interactive Demo Function

```python
def demo_nr_robot(n, link_lengths, target_points):
```

**Functionality:**
1. Takes number of joints, link lengths, and target positions
2. Solves IK for each target using numerical method
3. Validates solutions using FK
4. Plots all configurations

**Example Usage:**
```python
n = 4
link_lengths = [2.0, 1.5, 1.0, 0.5]
target_points = [(4.0, 1.0), (2.0, 3.0), (0.5, 0.5)]
demo_nr_robot(n, link_lengths, target_points)
```

---

## Part B: Rotation Matrices and Coordinate Transformations

### Concept Overview

**Rotation Matrices**: 3×3 matrices that rotate vectors in 3D space

**Properties:**
- Determinant = 1 (preserves volume)
- Orthogonal: $R^T R = I$ (inverse equals transpose)
- Preserve vector magnitudes (isometric)

### Basic Rotation Matrices

#### Roll (Rotation about X-axis)

```python
def Rx(phi):
    c, s = np.cos(phi), np.sin(phi)
    return np.array([
        [1, 0, 0],
        [0, c, -s],
        [0, s, c]
    ])
```

**Mathematical Form:**
$$R_x(\phi) = \begin{bmatrix} 1 & 0 & 0 \\ 0 & \cos\phi & -\sin\phi \\ 0 & \sin\phi & \cos\phi \end{bmatrix}$$

**Interpretation:**
- Rotates around the X-axis (right direction)
- X-coordinate unchanged
- Y-Z plane rotated by angle φ
- Like rotating something held horizontally

**Parameters:**
- `phi`: Rotation angle in radians

#### Pitch (Rotation about Y-axis)

```python
def Ry(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([
        [c, 0, s],
        [0, 1, 0],
        [-s, 0, c]
    ])
```

**Mathematical Form:**
$$R_y(\theta) = \begin{bmatrix} \cos\theta & 0 & \sin\theta \\ 0 & 1 & 0 \\ -\sin\theta & 0 & \cos\theta \end{bmatrix}$$

**Interpretation:**
- Rotates around the Y-axis (up direction)
- Y-coordinate unchanged
- X-Z plane rotated by angle θ
- Like pitching (tilting forward/backward)

**Parameters:**
- `theta`: Rotation angle in radians

#### Yaw (Rotation about Z-axis)

```python
def Rz(psi):
    c, s = np.cos(psi), np.sin(psi)
    return np.array([
        [c, -s, 0],
        [s, c, 0],
        [0, 0, 1]
    ])
```

**Mathematical Form:**
$$R_z(\psi) = \begin{bmatrix} \cos\psi & -\sin\psi & 0 \\ \sin\psi & \cos\psi & 0 \\ 0 & 0 & 1 \end{bmatrix}$$

**Interpretation:**
- Rotates around the Z-axis (forward direction)
- Z-coordinate unchanged
- X-Y plane rotated by angle ψ
- Like yawing (turning left/right)

**Parameters:**
- `psi`: Rotation angle in radians

### Composite Rotations (Fixed Axes)

**Important Concept:**

When performing **multiple rotations about fixed axes**, the order matters:

For rotations **Yaw → Pitch → Roll** about **fixed axes**:
$$R_{composite} = R_x(\text{roll}) \cdot R_y(\text{pitch}) \cdot R_z(\text{yaw})$$

**Key Point**: Pre-multiply in **reverse order** of application!

This is because each rotation is applied in the original (fixed) frame, not the rotated frame.

### Homogeneous Transformation Matrices

**Purpose**: Combine rotation and translation in a single 4×4 matrix

**General Form:**
$$T = \begin{bmatrix} R_{3×3} & t_{3×1} \\ 0_{1×3} & 1 \end{bmatrix}$$

Where:
- R: 3×3 rotation matrix
- t: 3×1 translation vector
- Bottom row: [0, 0, 0, 1]

#### Translation Matrices

```python
def Tx(d):  # Translation along X by d
    return np.array([
        [1, 0, 0, d],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ], dtype=float)

def Ty(d):  # Translation along Y by d
    return np.array([
        [1, 0, 0, 0],
        [0, 1, 0, d],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ], dtype=float)

def Tz(d):  # Translation along Z by d
    return np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, d],
        [0, 0, 0, 1]
    ], dtype=float)
```

#### Homogeneous Rotation Matrices

```python
def Rx_h(phi):  # Roll (homogeneous)
    c, s = np.cos(phi), np.sin(phi)
    return np.array([
        [1, 0, 0, 0],
        [0, c, -s, 0],
        [0, s, c, 0],
        [0, 0, 0, 1]
    ])

def Ry_h(theta):  # Pitch (homogeneous)
    c, s = np.cos(theta), np.sin(theta)
    return np.array([
        [c, 0, s, 0],
        [0, 1, 0, 0],
        [-s, 0, c, 0],
        [0, 0, 0, 1]
    ])

def Rz_h(psi):  # Yaw (homogeneous)
    c, s = np.cos(psi), np.sin(psi)
    return np.array([
        [c, -s, 0, 0],
        [s, c, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])
```

### Coordinate Transformation

**Problem**: Transform a point from one coordinate frame to another

**Given:**
- Point P in mobile frame: $[p]^M$
- Transformation matrix T encoding: rotation R and translation t
- Find: Point P in fixed frame: $[p]^F$

**Solution:**
$$[p]^F = R \cdot [p]^M + t$$

In homogeneous coordinates:
$$\begin{bmatrix} [p]^F \\ 1 \end{bmatrix} = T \cdot \begin{bmatrix} [p]^M \\ 1 \end{bmatrix}$$

---

## Function Reference

### Kinematics Functions

| Function | Purpose | Input | Output |
|----------|---------|-------|--------|
| `forward_kinematics_2r(θ₁, θ₂, L₁, L₂)` | Compute end-effector from angles | Angles, link lengths | (x, y) |
| `inverse_kinematics_2r(x, y, L₁, L₂)` | Compute angles from position | Position, link lengths | List of solutions |
| `plot_robot_2r(θ₁, θ₂, L₁, L₂, ...)` | Visualize 2R configuration | Joint angles, lengths | Matplotlib axes |
| `forward_kinematics_nr(θ, L)` | Compute end-effector for n-R | Joint angles, link lengths | (x, y), (X, Y) |
| `compute_jacobian_nr(θ, L)` | Compute Jacobian matrix | Joint angles, link lengths | 2×n matrix |
| `inverse_kinematics_nr(x, y, L, ...)` | Solve n-R IK numerically | Target, link lengths, params | (θ, success) |
| `plot_robot_nr(θ, L, ...)` | Visualize n-R configuration | Joint angles, link lengths | Matplotlib axes |
| `demo_nr_robot(n, L, targets)` | Full n-R demo | Num joints, lengths, targets | Plots |

### Rotation Functions

| Function | Purpose |
|----------|---------|
| `Rx(φ)` | Roll rotation matrix |
| `Ry(θ)` | Pitch rotation matrix |
| `Rz(ψ)` | Yaw rotation matrix |
| `Rx_h(φ)` | Roll (homogeneous 4×4) |
| `Ry_h(θ)` | Pitch (homogeneous 4×4) |
| `Rz_h(ψ)` | Yaw (homogeneous 4×4) |

### Transformation Functions

| Function | Purpose |
|----------|---------|
| `Tx(d)` | Translation along X-axis |
| `Ty(d)` | Translation along Y-axis |
| `Tz(d)` | Translation along Z-axis |

### Utility Functions

| Function | Purpose |
|----------|---------|
| `print_matrix(M, name, precision)` | Pretty-print 3×3 matrix |
| `print_matrix_4x4(M, name)` | Pretty-print 4×4 matrix |

---

## Variable Dictionary

### Kinematics Variables

| Variable | Type | Range | Meaning |
|----------|------|-------|---------|
| `theta1` | float | -π to π | First joint angle (radians) |
| `theta2` | float | -π to π | Second joint angle (radians) |
| `thetas` | array | -π to π | Array of all joint angles |
| `L1, L2, L3` | float | > 0 | Link lengths (meters) |
| `link_lengths` | array | > 0 | Array of all link lengths |
| `x, y` | float | ℝ | End-effector Cartesian coordinates |
| `x_target, y_target` | float | ℝ | Desired end-effector position |
| `d_sq` | float | ≥ 0 | Distance squared to target |
| `cos_theta2` | float | [-1, 1] | Cosine of second joint angle |

### Workspace Variables

| Variable | Type | Meaning |
|----------|------|---------|
| `R_out` | float | Outer reach radius (L₁ + L₂) |
| `R_in` | float | Inner reach radius (\|L₁ - L₂\|) |
| `max_reach` | float | Maximum extension sum of links |
| `reachable` | bool | Whether target is reachable |

### IK Solver Variables

| Variable | Type | Meaning |
|----------|------|---------|
| `max_iterations` | int | Maximum solver iterations |
| `tolerance` | float | Convergence error threshold |
| `damping` | float | Damped least-squares factor |
| `error_magnitude` | float | Current position error |
| `J` | array (2×n) | Jacobian matrix |
| `JJT` | array (2×2) | J·Jᵀ product |
| `delta_theta` | array (n) | Joint angle increment |

### Rotation Variables

| Variable | Type | Meaning |
|----------|------|---------|
| `phi` | float (rad) | Roll angle |
| `theta` | float (rad) | Pitch angle |
| `psi` | float (rad) | Yaw angle |
| `c, s` | float | cos(angle), sin(angle) |
| `R` | array (3×3) | Rotation matrix |
| `T` | array (4×4) | Homogeneous transformation |
| `t_final` | array (3) | Translation component |
| `R_final` | array (3×3) | Rotation component |

---

## Problems and Solutions

### Problem B.1: Composite Rotation (UAV Drone)

**Problem Statement:**
A drone performs these rotations about **fixed axes**:
1. Yaw: π/2 rad about Z-axis
2. Pitch: -π/2 rad about Y-axis
3. Roll: π/2 rad about X-axis

Find the composite rotation matrix.

**Solution:**

For fixed-axis rotations, pre-multiply in **reverse order**:
$$R_{composite} = R_x(\pi/2) \cdot R_y(-\pi/2) \cdot R_z(\pi/2)$$

**Step 1: Individual matrices**

$$R_z(\pi/2) = \begin{bmatrix} 0 & -1 & 0 \\ 1 & 0 & 0 \\ 0 & 0 & 1 \end{bmatrix}$$

$$R_y(-\pi/2) = \begin{bmatrix} 0 & 0 & -1 \\ 0 & 1 & 0 \\ 1 & 0 & 0 \end{bmatrix}$$

$$R_x(\pi/2) = \begin{bmatrix} 1 & 0 & 0 \\ 0 & 0 & -1 \\ 0 & 1 & 0 \end{bmatrix}$$

**Step 2: Intermediate product**

$$R_y \cdot R_z = \begin{bmatrix} 0 & 0 & -1 \\ 1 & 0 & 0 \\ 0 & -1 & 0 \end{bmatrix}$$

**Step 3: Final product**

$$R_{composite} = \begin{bmatrix} 0 & 0 & -1 \\ 0 & 1 & 0 \\ 1 & 0 & 0 \end{bmatrix}$$

**Verification:**
- Determinant: 1 ✓
- Orthogonal: Rᵀ·R = I ✓

### Problem B.2: Point Coordinate Transformation

**Problem Statement:**
A tool tip point P has mobile coordinates $[p]^M = [0, 0, 0.6]^T$ m.

After rotations:
1. Yaw: 45° about Z
2. Pitch: 60° about Y
3. Roll: 90° about X

Find fixed-frame coordinates $[p]^F$.

**Solution:**

**Step 1: Convert to radians**
- Yaw: 45° = π/4
- Pitch: 60° = π/3
- Roll: 90° = π/2

**Step 2: Compute composite rotation**

$$R_{composite} = R_x(\pi/2) \cdot R_y(\pi/3) \cdot R_z(\pi/4)$$

**Step 3: Individual matrices**

$$R_z(45°) = \begin{bmatrix} 0.7071 & -0.7071 & 0 \\ 0.7071 & 0.7071 & 0 \\ 0 & 0 & 1 \end{bmatrix}$$

$$R_y(60°) = \begin{bmatrix} 0.5 & 0 & 0.866 \\ 0 & 1 & 0 \\ -0.866 & 0 & 0.5 \end{bmatrix}$$

$$R_x(90°) = \begin{bmatrix} 1 & 0 & 0 \\ 0 & 0 & -1 \\ 0 & 1 & 0 \end{bmatrix}$$

**Step 4: Transform point**

$$[p]^F = R_{composite} \cdot [p]^M = R_{composite} \cdot \begin{bmatrix} 0 \\ 0 \\ 0.6 \end{bmatrix}$$

Result:
$$[p]^F = \begin{bmatrix} 0.5196 \\ -0.3 \\ 0.0 \end{bmatrix} \text{ meters}$$

**Interpretation:**
- Fixed X: 0.5196 m
- Fixed Y: -0.3 m (rotated to negative)
- Fixed Z: 0.0 m

### Problem B.3: Composite Transformation (Translation + Rotation)

**Problem Statement:**
Find composite transformation for:
1. Translation: +3 m along Y-axis
2. Rotation: +180° about Z-axis

**Solution:**

**Step 1: Translation matrix**

$$T_{trans} = \begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 3 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1 \end{bmatrix}$$

**Step 2: Rotation matrix** (180° = π rad)

$$T_{rot} = \begin{bmatrix} -1 & 0 & 0 & 0 \\ 0 & -1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1 \end{bmatrix}$$

**Step 3: Composite** (rotation after translation)

$$T_{composite} = T_{rot} \cdot T_{trans}$$

$$= \begin{bmatrix} -1 & 0 & 0 & 0 \\ 0 & -1 & 0 & -3 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1 \end{bmatrix}$$

**Interpretation:**
- The 180° rotation flips both X and Y directions
- The translation (0, 3, 0) becomes (0, -3, 0) after rotation
- Bottom row always [0, 0, 0, 1]

### Problem B.4: Complex Multi-Step Transformation

**Problem Statement:**
Find composite transformation for sequence:
1. Yaw: -π/2 about Z
2. Translation: 0.1 m along X
3. Pitch: π/2 about Y
4. Translation: 0.2 m along Z
5. Roll: π/2 about X
6. Translation: 0.3 m along Y

**Solution:**

**Define Each Transformation:**

$$T_1 = R_z(-\pi/2) = \begin{bmatrix} 0 & 1 & 0 & 0 \\ -1 & 0 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1 \end{bmatrix}$$

$$T_2 = T_x(0.1) = \begin{bmatrix} 1 & 0 & 0 & 0.1 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1 \end{bmatrix}$$

$$T_3 = R_y(\pi/2) = \begin{bmatrix} 0 & 0 & 1 & 0 \\ 0 & 1 & 0 & 0 \\ -1 & 0 & 0 & 0 \\ 0 & 0 & 0 & 1 \end{bmatrix}$$

$$T_4 = T_z(0.2) = \begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0.2 \\ 0 & 0 & 0 & 1 \end{bmatrix}$$

$$T_5 = R_x(\pi/2) = \begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 0 & -1 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 1 \end{bmatrix}$$

$$T_6 = T_y(0.3) = \begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0.3 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1 \end{bmatrix}$$

**Composite Transformation:**

$$T_{composite} = T_1 \cdot T_2 \cdot T_3 \cdot T_4 \cdot T_5 \cdot T_6$$

The result encodes:
- **Rotation part** (top-left 3×3): Combined orientation from all rotations
- **Translation part** (top-right 3×1): Accumulated displacement in meters

**Key Insight:** Order matters! Each rotation affects subsequent translations.

---

## Key Concepts Summary

### Forward vs. Inverse Kinematics

| Aspect | Forward | Inverse |
|--------|---------|---------|
| **Direction** | Angles → Position | Position → Angles |
| **Uniqueness** | Always unique | May have 0, 1, 2, or ∞ solutions |
| **Computation** | Direct/analytical | Often numerical/iterative |
| **Speed** | Fast | Slower (depends on method) |
| **Complexity** | Simple | Depends on DOF |

### Rotations: Fixed vs. Moving Axes

| Aspect | Fixed Axes | Moving Axes |
|--------|-----------|------------|
| **Reference** | Rotation about global frame | Rotation about current frame |
| **Matrix Order** | Pre-multiply (reverse) | Post-multiply (forward) |
| **Example** | Z→Y→X (pre-mult as X·Y·Z) | Z→Y→X (post-mult as Z·Y·X) |
| **Use** | Absolute directions | Sequential/iterative rotations |

### Degrees of Freedom (DOF)

- **2 DOF (2R)**: Position only in 2D plane (x, y)
- **3 DOF (3R or PPP)**: Full 2D position + orientation, or 3D Cartesian
- **6 DOF**: Full 3D position + orientation (standard industrial robot)

### Singularities

Points where robot loses dexterity:
- 2R at full extension: All links aligned
- 2R at full fold: Links back-to-back
- General: When Jacobian determinant = 0

---

## Code Execution Examples

### Example 1: 2R IK Validation

```python
# Define robot
L1, L2 = 3.0, 2.0

# Target point
x_target, y_target = 4, 2

# Solve IK
solutions = inverse_kinematics_2r(x_target, y_target, L1, L2)

# Validate each solution with FK
for sol_idx, (theta1, theta2) in enumerate(solutions):
    x_computed, y_computed = forward_kinematics_2r(theta1, theta2, L1, L2)
    error = np.sqrt((x_target - x_computed)**2 + (y_target - y_computed)**2)
    print(f"Solution {sol_idx}: error = {error:.6f}")
```

### Example 2: n-R IK with Numerical Method

```python
# 4-joint robot
n = 4
link_lengths = [2.0, 1.5, 1.0, 0.5]
x_target, y_target = 4.0, 1.0

# Solve
thetas, success = inverse_kinematics_nr(x_target, y_target, link_lengths)

if success:
    x_end, y_end, _ = forward_kinematics_nr(thetas, link_lengths)
    print(f"Converged to: ({x_end:.4f}, {y_end:.4f})")
    print(f"Joint angles: {np.degrees(thetas)} degrees")
```

### Example 3: Rotation Composition

```python
# Roll, Pitch, Yaw about fixed axes
roll, pitch, yaw = np.pi/2, np.pi/3, np.pi/4

# Composite rotation (pre-multiply in reverse)
R = Rx(roll) @ Ry(pitch) @ Rz(yaw)

# Verify orthogonality
assert np.allclose(R @ R.T, np.eye(3)), "Not orthogonal!"
assert np.isclose(np.linalg.det(R), 1.0), "Determinant != 1"
```

---

## Student Information

- **Student Name**: Naishadh Rana
- **Roll No**: U23CS014
- **Course**: AI352 - Robotics and its Application
- **Assignment**: Lab 4 - Forward and Inverse Kinematics, Rotation Matrices

