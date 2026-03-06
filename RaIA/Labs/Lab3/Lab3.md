# Robotics and its Application AI352 
## Lab 3: Workspace Analysis for Different Coordinate Systems 

---

### **Part A: For 2R Planar Robot Arm** 
* Animate the robot arm moving along a circular trajectory within the workspace.
* Develop a GUI for the nR Planar Robot Arm and its workspace in realtime.
    * *Note:* You may take the idea from the lab-1 simulator.

---

### **Part B: Workspace Analysis of a 3R Planar Robot Arm** 
A 3R planar robot arm consists of three revolute joints ($\theta_1, \theta_2, \theta_3$) connected by three rigid links of lengths $L_{1}, L_{2}$ and $L_{3}$. Unlike a 2R manipulator, a 3R robot possesses kinematic redundancy, allowing multiple joint configurations to reach the same end-effector position.

**Figure 3.1: 3-D Planar Robotic Arm** 

The end-effector position of a 3R planar robot is given by the forward kinematics equations:

$$
x = L_{1}\cos(\theta_{1}) + L_{2}\cos(\theta_{1}+\theta_{2}) + L_{3}\cos(\theta_{1}+\theta_{2}+\theta_{3})
$$

$$
y = L_{1}\sin(\theta_{1}) + L_{2}\sin(\theta_{1}+\theta_{2}) + L_{3}\sin(\theta_{1}+\theta_{2}+\theta_{3})
$$

**Workspace Visualization Tasks:**
1.  Write a Python code for analysing the workspace of 3R Robot.
2.  Animate the robot arm moving along a circular trajectory within the workspace.
3.  Compare the workspace of 2R and 3R Robots.

---

### **Part C: Workspace Analysis of a PPP/SSS Planar Robot Arm** 

**Figure 3.2: PPP Robotic Arm** 

The forward kinematics determines the position of the end-effector ($x, y, z$) based on the joint displacements ($d_1, d_2, d_3$). In a standard configuration where each joint is aligned with a principal axis, the end-effector position is given by:

$$
x = L_1 + d_1
$$

$$
y = L_2 + d_2
$$

$$
z = L_3 + d_3
$$

**Workspace Visualization Tasks:**
1.  Write a Python code for analysing the workspace of Robot.
2.  Animate the robot arm moving within the workspace.

---

### **Part D: Workspace Analysis of a TPP/RSS Planar Robot Arm** 
The total transformation matrix $T = A_1 A_2 A_3$ provides the final position and orientation.

**Figure 3.3: RPP Robotic Arm** 

For a standard RPP arm, the position ($x, y, z$) of the end-effector is:

$$
x = d_3 \cos(\theta_{1})
$$

$$
y = d_3 \sin(\theta_{1})
$$

$$
z = L_1 + d_2
$$

**Workspace Visualization Tasks:**
1.  Write a Python code for analysing the workspace of Robot.
2.  Animate the robot arm moving within the workspace.

---

### **Part E: Workspace Analysis of a TRP/RRS Planar Robot Arm** 
In a typical spherical configuration, the first joint rotates the base ($\theta_1$), the second joint tilts the arm up and down ($\theta_{2}$), and the third joint extends the arm radially ($d_3$).

**Figure 3.4: RPS Robotic Arm** 

The position ($x, y, z$) of the end-effector is:

$$
x = d_{3}\sin(\theta_{2})\cos(\theta_{1})
$$

$$
y = d_{3}\sin(\theta_{2})\sin(\theta_{1})
$$

$$
z = L_{1} + d_{3}\cos(\theta_{2})
$$

**Workspace Visualization Tasks:**
1.  Write a Python code for analysing the workspace of Robot.
2.  Animate the robot arm moving within the workspace.