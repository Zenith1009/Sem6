# Comprehensive Explanation of U23CS014_Lab3.ipynb

## Overview
This notebook is an assignment for **Robotics and its Application (AI352)** that analyzes the **workspace** of different robotic arm configurations. The workspace is the set of all points an end-effector (tool/gripper) can reach.

---

## Table of Contents
1. [Imports & Dependencies](#imports--dependencies)
2. [Part A: 2R Planar Robot](#part-a-2r-planar-robot)
3. [Part B: 3R Planar Robot](#part-b-3r-planar-robot)
4. [Part C: PPP Cartesian Robot](#part-c-ppp-cartesian-robot)
5. [Part D: RPP Cylindrical Robot](#part-d-rpp-cylindrical-robot)
6. [Part E: RRP Spherical Robot](#part-e-rrp-spherical-robot)
7. [Variable Dictionary](#variable-dictionary)
8. [Function Reference](#function-reference)

---

## Imports & Dependencies

```python
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from IPython.display import HTML
from ipywidgets import IntSlider, FloatSlider, VBox, HBox, Output
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
```

- **NumPy**: Numerical computing (arrays, trigonometry)
- **Matplotlib**: Plotting 2D and 3D graphs
- **Animation**: Creating animated robot movements
- **ipywidgets**: Interactive sliders for GUI
- **Axes3D**: 3D plotting toolkit

---

## Part A: 2R Planar Robot

### Concept
A **2R planar robot** has:
- **2 revolute joints** (rotational, like door hinges)
- **2 rigid links** of lengths L₁ and L₂
- **2D workspace** (works on a flat plane)
- **Fixed base** at origin (0, 0)

### Visual Structure
```
        Base (origin)
          |
         L1 link (length L1)
          |
      Joint 1 (θ1) ← rotates
          |
         L2 link (length L2)
          |
      Joint 2 (θ2) ← rotates
          |
    End-Effector (tool)
```

### Forward Kinematics Equations
Forward kinematics converts **joint angles** → **end-effector position**:

```
x = L1·cos(θ1) + L2·cos(θ1 + θ2)
y = L1·sin(θ1) + L2·sin(θ1 + θ2)
```

Where:
- **θ1**: Angle of first joint (radians)
- **θ2**: Angle of second joint relative to first link (radians)
- **x, y**: Cartesian position of end-effector

### Inverse Kinematics
Inverse kinematics converts **desired position** → **joint angles**

```python
def ik_2r(x, y, L1, L2, elbow='down'):
```

**Parameters:**
- `x, y`: Desired end-effector position (target)
- `L1, L2`: Link lengths
- `elbow`: Solution configuration ('down' or 'up')
  - **'down'**: Elbow points downward (intuitive)
  - **'up'**: Elbow points upward (alternate solution)

**Variables Inside:**
- `d`: Normalized distance term = `(x² + y² - L₁² - L₂²) / (2·L₁·L₂)`
  - Used in cosine formula: `cos(θ2) = d`
  - Must be clipped to [-1, 1] (math constraint)

**Returns:**
- `t1`: First joint angle (θ₁)
- `t2`: Second joint angle (θ₂)

### Animation Function

```python
def animate_circle(L1=1.0, L2=1.0, r_ratio=0.6, T=6.0, fps=30, elbow='down'):
```

**Parameters:**
- `L1, L2`: Link lengths (meters, default 1.0 each)
- `r_ratio`: Radius ratio = 0.0 to 1.0
  - **Meaning**: What fraction of max reach should the circle be?
  - **Example**: r_ratio=0.6 means 60% of maximum reach
- `T`: Total animation duration (seconds)
  - **Example**: T=6.0 means animation lasts 6 seconds
- `fps`: Frames per second (30 = smooth animation)
- `elbow`: Joint configuration for IK ('down' or 'up')

**Key Variables Inside:**

| Variable | Meaning | Calculation |
|----------|---------|-------------|
| `R_out` | Outer workspace radius | L₁ + L₂ (all links extended) |
| `R_in` | Inner workspace radius | \|L₁ - L₂\| (links folded) |
| `r` | Actual circle radius | Clamped between safe bounds |
| `frames` | Total animation frames | T × fps |
| `t` | Angle array (0 to 2π) | np.linspace(0, 2π, frames) |
| `x, y` | Circle trajectory points | r·cos(t), r·sin(t) |
| `th1, th2` | Joint angles for trajectory | From IK solution |
| `xs_path, ys_path` | End-effector path history | Accumulated over animation |

**What the function does:**
1. Calculates safe circle radius within workspace
2. Creates circle trajectory: x = r·cos(t), y = r·sin(t)
3. Computes joint angles for each trajectory point using IK
4. Animates robot links following the circular path
5. Displays the path traced by end-effector

**Plot Elements:**
- Dashed circle at R_outer: Maximum reach boundary
- Dashed circle at R_inner: Minimum reach boundary (hole in middle)
- Red line with circles: Robot links (joints as circles)
- Green line: Path traced by end-effector

### Workspace Properties of 2R Robot

| Property | Value |
|----------|-------|
| Reachable Area | Annular ring (donut shape) |
| DOF (Degrees of Freedom) | 2 |
| Singularities | Yes (at fully extended/folded positions) |
| Redundancy | No (unique solution for most points) |

---

## Part B: 3R Planar Robot

### Concept
A **3R planar robot** has:
- **3 revolute joints** (θ₁, θ₂, θ₃)
- **3 rigid links** (L₁, L₂, L₃)
- **Kinematic redundancy**: Multiple joint solutions reach same point
- **Better workspace coverage** than 2R

### Forward Kinematics

```
x = L₁·cos(θ₁) + L₂·cos(θ₁+θ₂) + L₃·cos(θ₁+θ₂+θ₃)
y = L₁·sin(θ₁) + L₂·sin(θ₁+θ₂) + L₃·sin(θ₁+θ₂+θ₃)
```

### Workspace Computation Functions

#### `compute_workspace_3r(L1, L2, L3, resolution=50)`

**Parameters:**
- `L1, L2, L3`: Link lengths
- `resolution`: Grid resolution per axis
  - **Meaning**: 50 × 50 × 50 = 125,000 joint configurations tested
  - **Trade-off**: Higher resolution = more accurate but slower

**How it works:**
1. Creates grid of angles from -π to π
2. For each combination of (θ₁, θ₂, θ₃), calculates end-effector (x, y)
3. Returns all reachable points

**Returns:**
- Arrays of x and y coordinates for all reachable points

#### `compute_workspace_3r_monte_carlo(L1, L2, L3, samples=10000)`

**More Efficient Approach**: Random sampling instead of grid

**Parameters:**
- `samples`: Number of random joint configurations
  - **Example**: 10,000 random trials instead of 125,000 grid points
  - Much faster, statistically accurate

**How it works:**
1. Randomly generates 10,000 sets of angles (θ₁, θ₂, θ₃)
2. Calculates end-effector position for each
3. Returns all points (sparser but faster)

### Inverse Kinematics for 3R

```python
def ik_3r_fixed_orientation(x, y, L1, L2, L3, phi=0):
```

**Key Idea**: Fix the end-effector orientation (φ) to reduce redundancy

**Parameters:**
- `x, y`: Desired position
- `L1, L2, L3`: Link lengths
- `phi`: Fixed end-effector orientation angle (radians)
  - **Example**: phi=0 means end-effector points right (0°)

**Variables:**
- `xw, yw`: "Wrist position" (where the 3rd link should start)
  - Calculated by subtracting the fixed link from desired position
- Then uses 2R IK on the first two links

### Animation for 3R

```python
def animate_3r_circle(L1=1.0, L2=0.8, L3=0.5, r_ratio=0.5, T=6.0, fps=30):
```

**Same concept as 2R but extended to 3R**

**Key difference:**
- End-effector traces circle while maintaining orientation
- Shows how redundancy allows flexibility
- Can reach same point with different joint configurations

---

## Part C: PPP (Cartesian) Robot

### Concept
**PPP = Prismatic-Prismatic-Prismatic**

Three **prismatic joints** (linear actuators, like drawers):
- Each joint moves in straight line (X, Y, Z axes)
- No rotation, purely linear motion
- Simplest kinematics: position = joint values directly

### Forward Kinematics
```
x = L₁ + d₁  (base offset + prismatic extension in X)
y = L₂ + d₂  (base offset + prismatic extension in Y)
z = L₃ + d₃  (base offset + prismatic extension in Z)
```

**Where:**
- `L₁, L₂, L₃`: Base offsets (initial positions)
- `d₁, d₂, d₃`: Prismatic joint extensions

### Workspace Properties

| Property | Value |
|----------|-------|
| Shape | Rectangular box |
| Dimensions | d₁_range × d₂_range × d₃_range |
| Singularities | None (simple, no complications) |
| Direct mapping | Joint space = Cartesian space |

### Key Variables in PPP Workspace Calculation

```python
d1 = np.linspace(0, 2, 10)      # 10 positions along X axis
d2 = np.linspace(0, 1.5, 10)    # 10 positions along Y axis
d3 = np.linspace(0, 1, 10)      # 10 positions along Z axis
D1, D2, D3 = np.meshgrid(d1, d2, d3)  # Create 3D grid (10×10×10)
X, Y, Z = D1.flatten(), D2.flatten(), D3.flatten()  # Flatten to 1D arrays
```

### Visualization Function

```python
def plot_workspace_multiview(X, Y, Z, title, cmap='viridis'):
```

**Creates 3 views simultaneously:**

1. **3D Isometric View**: Full 3D perspective
   - Shows overall workspace shape
   - View angle: elev=25°, azim=45°

2. **Top View (XY plane)**: Looking down from Z
   - Shows X-Y coverage
   - Useful for 2D planning

3. **Side View (XZ plane)**: Looking from Y direction
   - Shows X-Z coverage (height profile)

**Color coding:**
- Colors represent distance from origin: √(x² + y² + z²)
- Warmer colors = farther from origin
- Helps visualize 3D depth

---

## Part D: RPP (Cylindrical) Robot

### Concept
**RPP = Revolute-Prismatic-Prismatic**

**Structure:**
- 1st joint: **Revolute** (rotates around Z axis)
  - Parameter: θ₁ (angle in XY plane)
- 2nd joint: **Prismatic** (moves vertically along Z)
  - Parameter: d₂ (height)
- 3rd joint: **Prismatic** (extends radially from center)
  - Parameter: d₃ (distance from Z axis)

### Forward Kinematics

```
x = d₃·cos(θ₁)    (radial distance × direction angle)
y = d₃·sin(θ₁)    (radial distance × direction angle)
z = L₁ + d₂       (base height + vertical extension)
```

**Visual Example:**
```
        Z (vertical axis)
        |
        |-----θ₁ (rotating arm)
        |     |
        |     d₃ (radial reach)
        |   /
   (d₂) | /
        |/
    ----O---- (base)
```

### Workspace Properties

| Property | Value |
|----------|-------|
| Shape | Hollow cylinder (like a cup) |
| Rotation | 360° around Z axis |
| Height range | L₁ to L₁ + d₂_max |
| Radial range | d₃_min to d₃_max |

### Key Variables

```python
theta = np.linspace(-np.pi, np.pi, 40)   # Rotation angles (0 to 360°)
d2 = np.linspace(0, 1.5, 12)             # 12 height levels
d3 = np.linspace(0.3, 1.5, 12)           # 12 radial distances
T, D2, D3 = np.meshgrid(theta, d2, d3)   # Create 3D grid
```

### RPP Forward Kinematics Function

```python
def rpp_fk(theta1, d2, d3, L1=0.5):
    return d3*np.cos(theta1), d3*np.sin(theta1), L1+d2
```

---

## Part E: RRP (Spherical) Robot

### Concept
**RRP = Revolute-Revolute-Prismatic**

Also called **Spherical/Polar robot**

**Structure:**
- 1st joint: **Revolute** (azimuth rotation around Z)
  - Parameter: θ₁ (0 to 2π, compass direction)
- 2nd joint: **Revolute** (elevation rotation)
  - Parameter: θ₂ (0 to π, up/down angle)
- 3rd joint: **Prismatic** (radial extension)
  - Parameter: d₃ (reach distance)

### Forward Kinematics

```
x = d₃·sin(θ₂)·cos(θ₁)    (spherical to Cartesian conversion)
y = d₃·sin(θ₂)·sin(θ₁)
z = L₁ + d₃·cos(θ₂)
```

**Mathematical Explanation:**
- **sin(θ₂)**: Projects d₃ onto XY plane (diminishes toward poles)
- **cos(θ₁), sin(θ₁)**: Angular direction in XY plane
- **cos(θ₂)**: Vertical component

### Workspace Properties

| Property | Value |
|----------|-------|
| Shape | Thick spherical shell |
| Coverage | Near-complete sphere (except singularities) |
| Azimuth range | θ₁: 0 to 2π (full rotation) |
| Elevation range | θ₂: 0.1 to π-0.1 (avoids singularities at poles) |
| Reach range | d₃: 0.5 to 1.5 |

### Key Variables

```python
theta1 = np.linspace(0, 2*np.pi, 40)           # Azimuth angles (360°)
theta2 = np.linspace(0.1, np.pi-0.1, 20)      # Elevation (avoid poles)
d3 = np.linspace(0.5, 1.5, 8)                  # Radial reach
T1, T2, D3 = np.meshgrid(theta1, theta2, d3)   # 3D grid
```

### RRP Forward Kinematics Function

```python
def rrp_fk(theta1, theta2, d3, L1=0.5):
    return (d3*np.sin(theta2)*np.cos(theta1), 
            d3*np.sin(theta2)*np.sin(theta1), 
            L1+d3*np.cos(theta2))
```

---

## Animation Functions for 3D Robots

### `animate_3d_with_projection(positions, limits, title, T=5.0, fps=20)`

**Creates dual views for 3D robot:**

1. **3D View (Left)**: Full 3D trajectory
2. **Top View (Right)**: XY projection (bird's eye view)

**Parameters:**
- `positions`: List of (x, y, z) tuples for each frame
- `limits`: 3-tuple of axis ranges: [(x_min, x_max), (y_min, y_max), (z_min, z_max)]
- `title`: Animation title
- `T`: Total duration (seconds)
- `fps`: Frames per second (lower = slower animation)

**Key Variables:**
- `xs, ys, zs`: Lists accumulating the path history
- `line3d, path3d`: 3D line plots (current frame + history)
- `line2d, path2d`: 2D line plots (XY projection)

---

## Variable Dictionary

### Common Robot Parameters

| Variable | Type | Typical Range | Meaning |
|----------|------|---------------|---------|
| `L1, L2, L3` | float | 0.5 to 2.0 | Link lengths (meters) |
| `θ1, θ2, θ3` | float | -π to π | Joint angles (radians) |
| `d1, d2, d3` | float | 0 to 2.0 | Prismatic extensions (meters) |
| `r_ratio` | float | 0.0 to 1.0 | Circle radius as fraction of max reach |
| `T` | float | > 0 | Animation duration (seconds) |
| `fps` | int | 20-60 | Frames per second |

### Workspace Variables

| Variable | Type | Meaning |
|----------|------|---------|
| `R_out` | float | Outer workspace radius (max reach) |
| `R_in` | float | Inner workspace radius (min reach) |
| `x, y, z` | array | Cartesian coordinates of points |
| `frames` | int | Total animation frames = T × fps |
| `samples` | int | Monte Carlo sample count |
| `resolution` | int | Grid resolution per dimension |

### Animation Variables

| Variable | Type | Meaning |
|----------|------|---------|
| `fig` | Figure | Matplotlib figure object |
| `ax` | Axes | Plot axes |
| `line` | Line2D | Line object for robot links |
| `path` | Line2D | Line object for end-effector path |
| `ani` | FuncAnimation | Animation object |

---

## Function Reference

### Kinematics Functions

| Function | Input | Output | Purpose |
|----------|-------|--------|---------|
| `ik_2r(x, y, L1, L2)` | Position + link lengths | θ1, θ2 | Inverse kinematics for 2R |
| `ik_3r_fixed_orientation(x, y, L1, L2, L3, phi)` | Position + links + orientation | θ1, θ2, θ3 | 3R IK with fixed end-effector angle |
| `rpp_fk(θ1, d2, d3, L1)` | Joint values | x, y, z | Forward kinematics for RPP robot |
| `rrp_fk(θ1, θ2, d3, L1)` | Joint values | x, y, z | Forward kinematics for RRP robot |

### Workspace Functions

| Function | Purpose | Returns |
|----------|---------|---------|
| `fk_chain(angles, lengths)` | Compute all joint positions for nR chain | X array, Y array |
| `sample_workspace(lengths, samples)` | Monte Carlo workspace sampling | x points, y points |
| `compute_workspace_3r(L1, L2, L3, resolution)` | Grid-based 3R workspace | x points, y points |
| `compute_workspace_3r_monte_carlo(L1, L2, L3, samples)` | Random sampling 3R workspace | x points, y points |
| `plot_workspace_multiview(X, Y, Z, title)` | Visualize 3D workspace with 3 views | None (displays plot) |

### Animation Functions

| Function | Purpose |
|----------|---------|
| `animate_circle(L1, L2, ...)` | Animate 2R robot on circular path |
| `animate_3r_circle(L1, L2, L3, ...)` | Animate 3R robot on circular path |
| `animate_3d_with_projection(positions, limits, ...)` | Animate 3D path with dual views |

---

## Matplotlib & NumPy Operations

### Common NumPy Operations in This Notebook

```python
np.linspace(start, stop, num)      # Create evenly spaced array
np.meshgrid(x, y, z)               # Create 3D coordinate grids
np.cumsum(array)                   # Cumulative sum (for joint angle accumulation)
np.random.uniform(low, high, size) # Random numbers in range
np.cos(), np.sin()                 # Trigonometric functions
np.arccos(), np.arctan2()          # Inverse trig functions
np.clip(array, min, max)           # Clamp values to range
np.sqrt(x**2 + y**2 + z**2)        # Distance calculation
array.flatten()                    # Reshape to 1D
```

### Common Matplotlib Operations

```python
plt.figure(figsize=)               # Create figure
plt.gca()                          # Get current axes
ax.plot([], [], ...)               # Line plot
ax.scatter(..., s=, alpha=, c=)    # Scatter plot
ax.add_patch(plt.Circle(...))      # Add circle patch
ax.set_xlim(), set_ylim()          # Set axis limits
ax.set_aspect('equal')             # Equal aspect ratio
animation.FuncAnimation()          # Create animation
plt.close()                        # Close figure
```

---

## Robotics Concepts Summary

### Joint Type Notation

| Symbol | Full Name | Motion | Example | Parameters |
|--------|-----------|--------|---------|------------|
| **R** | Revolute | Rotation | Door hinge | θ (angle, -π to π) |
| **P** | Prismatic | Linear slide | Drawer slide | d (distance) |

### Degrees of Freedom (DOF)

- **2R**: 2 DOF → Can position end-effector in 2D (x, y)
- **3R**: 3 DOF → Can position in 2D + control orientation (x, y, θ)
- **PPP**: 3 DOF → Can position in 3D Cartesian (x, y, z)
- **RPP**: 3 DOF → Can position in cylindrical coords (r, θ, z)
- **RRP**: 3 DOF → Can position in spherical coords (ρ, θ, φ)

### Workspace vs Configuration Space

- **Workspace**: Set of all points end-effector can reach (Cartesian space)
  - 2D for planar robots
  - 3D for spatial robots
- **Configuration Space**: Set of all possible joint angles
  - 2D for 2R (θ1, θ2)
  - 3D for 3R (θ1, θ2, θ3)
  - Much larger than workspace (many configs → same point due to redundancy)

### Singularities

Points where the robot loses dexterity:
- **2R at full extension**: All links aligned, cannot rotate freely
- **2R at full fold**: Links folded back, minimal reach
- **RRP at poles**: θ2 = 0 or π, no azimuth control

---

## Complete Example Walkthrough: 2R Animation

```python
# Create animation with these parameters:
animate_circle(L1=1.0, L2=1.0, r_ratio=0.7, T=5.0, fps=30, elbow='down')

# Step-by-step execution:
# 1. R_out = 1.0 + 1.0 = 2.0 m (maximum reach)
# 2. R_in = |1.0 - 1.0| = 0.0 m (no hole in workspace)
# 3. r = 0.7 × 2.0 = 1.4 m (circle radius = 70% of max reach)
# 4. frames = 5.0 × 30 = 150 frames total
# 5. t = [0, 0.042, 0.084, ..., 6.283] radians (150 points around circle)
# 6. x = 1.4 × cos(t) = [1.4, 1.394, 1.377, ..., 1.4]
# 7. y = 1.4 × sin(t) = [0, 0.058, 0.116, ..., -0.001]
# 8. For each (x, y), compute (θ1, θ2) using inverse kinematics
# 9. Create 150-frame animation showing robot following the circle
# 10. Each frame shows: robot links + path traced so far
```

---

## Key Insights from the Notebook

1. **Workspace Shape Depends on Robot Type:**
   - Planar (2R, 3R) → 2D shapes (annulus, disk)
   - Prismatic (PPP) → Box (simple)
   - Mixed (RPP) → Cylinder
   - Double-revolute (RRP) → Sphere

2. **Redundancy Increases Flexibility:**
   - 3R can reach interior points with multiple joint solutions
   - Better coverage of workspace
   - More flexibility in motion planning

3. **Visualization is Critical:**
   - 3D robots need multiple views to understand workspace
   - Color-coding helps visualize depth/distance
   - Animations show robot motion, not static positions

4. **Forward vs Inverse Kinematics:**
   - **Forward**: Easy, always unique solution (joint angles → position)
   - **Inverse**: Hard, may have multiple solutions (position → joint angles)
   - 2R has 0 or 2 solutions; 3R has ∞ solutions (redundant)

---

## Student Information

- **Student Name**: Naishadh Rana
- **Roll No**: U23CS014
- **Course**: AI352 - Robotics and its Application
- **Assignment**: Lab 3 - Workspace Analysis for Different Coordinate Systems

