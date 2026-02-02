## Lab 4 - Forward and Inverse Kinematics for Planar Robot Arm

### PART A: Forward and Inverse Kinematics for n-R Planar Robot Arm

*Given a 2R planar robotic arm (consisting of two revolute joints and two rigid links), you are required to:*

1. **Forward Kinematics:**  
   Write a Python function that takes joint angles $\theta_1$ and $\theta_2$ (in degrees or radians) and link lengths $L_1$ and $L_2$, then computes and plots the $(x, y)$ position of the end-effector (robotic arm tip).

2. **Inverse Kinematics:**  
   Write a separate Python function that takes the desired $(x, y)$ position of the end-effector and link lengths $L_1$ and $L_2$, then computes all valid possible pairs of joint angles ($\theta_1$, $\theta_2$) that allow the arm to reach that point (if possible).

3. **Validation and Visualization:**  
   - Demonstrate both functions with sample data: choose $L_1 = 3$ m, $L_2 = 2$ m.  
   - For at least three arbitrary target points within the arm's workspace, compute joint angles using your inverse kinematics function and then use your forward kinematics function to validate (by finding the end-effector's position for the computed angles).  
   - Plot the robot configuration in matplotlib for all test cases.

4. Write a python program for Forward and Inverse kinematic for n-R Planar Robot Arm. Take the input n from the user.

**Sample Structure:**

```python
# Forward Kinematics Function
def forward_kinematics(theta1, theta2, L1, L2):
    # Calculate (x, y) for given joint angles
    # ...
    return x, y

# Inverse Kinematics Function
def inverse_kinematics(x, y, L1, L2):
    # Find all (theta1, theta2) pairs that can reach (x, y)
    # ...
    return solutions # e.g. list of (theta1, theta2)
```

---

### PART B: Solve as markdown and Write Python Programs

*Following problems need to be solved by hand and then implemented in Python:*

**Problem B.1: Composite Rotation Matrix**

Consider yourself as Robotic Engineer in a famous UAV Company. Given sequential rotations about fixed axes, of drone starting with yaw of $\pi/2$, followed by pitch of $-\pi/2$ and finally a roll of $\pi/2$. What is the resulting orientation i.e composite rotation matrix?

**Problem B.2: Coordinate Transformation**

A point P at the tool tip has mobile coordinates $[p]^M = [0, 0, 0.6]^T$. After applying the following rotations about fixed axes: Yaw of $45°$ about Z; Pitch of $60°$ about Y; Roll of $90°$ about X. What are the fixed-frame coordinates $[p]^F$?

**Problem B.3: Composite Transformation**

For the sequence of actions translation of M along $f_2$ by 3 units, and then rotate M about $f_3$ by $180°$, find the composite transformation matrix?

**Problem B.4: Complex Transformation**

Suppose we rotate tool about the fixed axes:
- Yaw of $-\pi/2$ about Z
- Translation of 10 cm along X
- Pitch of $\pi/2$ about Y
- Translation of 20 cm along Z
- Roll of $\pi/2$ about X
- Translation of 30 cm along Y

What is the resulting composite homogeneous transformation matrix?