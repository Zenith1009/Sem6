# Practice Numerical for Unit 2 and 3 - Exam Prep Guide

This document is designed as a study guide, not just an answer sheet. The goal is that even if a topic is weak right now, you should still be able to learn the idea, understand the formula, and then solve the numerical in an exam format.

## How to study from this file

Read each topic in this order:

1. Concept and meaning
2. Core formula
3. Exam method
4. Worked numerical

If you only memorize the final numbers, these problems will change slightly in the exam and become hard. If you understand the structure, you can solve new variants too.

## Main topics hidden inside these 10 numericals

- Coordinate transformations between frames
- Forward kinematics of a planar robot arm
- Inverse kinematics of a planar robot arm
- Cubic trajectory planning
- Moment of inertia of robot links
- Gravity loading in manipulators
- Kinetic energy of a robotic link
- Coriolis and centrifugal torque components

## 1. Coordinate transformations and frame changes

### What this means

A robot does not describe everything in one coordinate system. One point may be given in the end-effector frame, another in the link frame, and the final answer may be needed in the base or universal frame. So robotics frequently asks us to convert coordinates from one frame to another.

### Core relation

If a point is known in frame $B$, then in frame $U$ it is written as

$$
{}^{U}Q = {}^{U}_{B}R \; {}^{B}Q + {}^{U}P_B
$$

Here:

- ${}^{U}_{B}R$ is the rotation matrix of frame $B$ with respect to frame $U$
- ${}^{U}P_B$ is the position of the origin of frame $B$ measured in frame $U$

For rotation about the $z$-axis by angle $θ$,

$$
R_z(θ)=
\begin{bmatrix}
\cos θ & -\sin θ & 0 \\
\sin θ & \cos θ & 0 \\
0 & 0 & 1
\end{bmatrix}
$$

### Exam method

1. Write the rotation matrix.
2. Write the translation vector.
3. Multiply the rotation matrix by the local point coordinates.
4. Add the translation vector.

### Common mistakes

- Adding translation before rotation
- Forgetting which frame the point is originally given in
- Using the wrong sign for sine in the rotation matrix

## 2. Forward kinematics of a 2-DOF planar manipulator

### What this means

Forward kinematics means: if the joint angles are known, find the end-effector position.

For a two-link planar robot,

$$
q_x = L_1 \cos θ_1 + L_2 \cos(θ_1 + θ_2)
$$

$$
q_y = L_1 \sin θ_1 + L_2 \sin(θ_1 + θ_2)
$$

### Why the angle becomes $(θ_1 + θ_2)$

The second link is not measured from the global $x$-axis. It is measured relative to the first link. So its absolute orientation is the sum of the two joint angles.

### Exam method

1. Write the forward kinematics equations.
2. Substitute the link lengths and angles.
3. Evaluate the trigonometric values carefully.
4. State the final $(q_x,q_y)$ pair clearly.

## 3. Inverse kinematics of a 2-DOF planar manipulator

### What this means

Inverse kinematics means: if the desired end-effector position is known, find the joint angles required to reach it.

### Core relations

First find $θ_2$ using geometry:

$$
\cos θ_2 = \frac{q_x^2 + q_y^2 - L_1^2 - L_2^2}{2L_1L_2}
$$

Then,

$$
θ_2 = \pm \cos^{-1}\left(\frac{q_x^2 + q_y^2 - L_1^2 - L_2^2}{2L_1L_2}\right)
$$

The two signs correspond to the two physical configurations:

- Elbow-up
- Elbow-down

Now find $θ_1$:

$$
θ_1 = \tan^{-1}\left(\frac{q_y}{q_x}\right) - \tan^{-1}\left(\frac{L_2 \sin θ_2}{L_1 + L_2 \cos θ_2}\right)
$$

### Exam method

1. Find $\cos θ_2$ first.
2. Obtain the two values of $θ_2$.
3. Substitute each value separately into the formula for $θ_1$.
4. Clearly label which answer is elbow-up and which is elbow-down.

### Common mistakes

- Forgetting the second solution for $θ_2$
- Not labeling the two physical configurations
- Losing the sign while substituting $\sin θ_2$

## 4. Cubic trajectory planning

### What this means

The robot should move smoothly from an initial position to a final position. If the initial and final velocities are zero, a cubic polynomial is the standard choice.

### Standard form

$$
θ(t)=a_0+a_1 t+a_2 t^2+a_3 t^3
$$

Velocity is

$$
\dot{θ}(t)=a_1+2a_2 t+3a_3 t^2
$$

### Typical boundary conditions

$$
θ(0)=θ_i, \qquad θ(T)=θ_f, \qquad \dot{θ}(0)=0, \qquad \dot{θ}(T)=0
$$

### Exam method

1. Assume the cubic form.
2. Differentiate once to get velocity.
3. Apply all four boundary conditions.
4. Solve the simultaneous equations for $a_0,a_1,a_2,a_3$.
5. Substitute the requested time value.

## 5. Moment of inertia of robotic links

### What this means

Moment of inertia tells us how strongly a body resists angular acceleration about a given axis. In robotics, this directly affects how much torque is needed.

### Important idea

Inertia increases when:

- Mass increases
- The axis is farther from the mass distribution
- The geometry places more material away from the axis

### Formulas appearing in this set

Circular link:

$$
I_{xx}=\frac{1}{2}mr^2
$$

$$
I_{yy}=\frac{1}{3}ml^2+\frac{1}{4}mr^2
$$

Rectangular link about $z$-axis:

$$
I_{zz}=m\left(\frac{l^2}{3}+\frac{a^2}{12}\right)
$$

### Exam method

1. Write the relevant inertia formula.
2. Square the dimensions carefully.
3. Keep units with the final answer.

## 6. Dynamics terms: gravity, kinetic energy, and Coriolis effect

### Gravity torque

Gravity torque is the torque required to hold the link against gravity. In this set, the standard interpreted relation is

$$
C_2=\frac{1}{2}m_2 g L_2 \cos(θ_1+θ_2)
$$

### Kinetic energy

For the given single-link case,

$$
K_1=\frac{1}{2}\operatorname{Tr}(U_{11}J_1U_{11}^{T})\dot{q}_1^2
$$

### Coriolis and centrifugal component

The coefficient in the numerical set is

$$
h_{122}=-\frac{1}{2}m_2L_1L_2\sin θ_2
$$

and the required term is

$$
h_{122}\dot{θ}_2^{\,2}
$$

### What to understand

- Gravity terms depend on position
- Kinetic energy depends on velocity squared
- Coriolis and centrifugal terms involve products of link dimensions, mass, and joint velocity

## Detailed solved numericals

## Q1. Coordinate transformation of a point

### Given

Frame $B$ is rotated about the $Z_U$ axis by $30^\circ$ and translated by $5$ units along $X_U$ and $2$ units along $Y_U$. The point in frame $B$ is ${}^{B}Q = [2,1,0]^T$

Find the coordinates of the same point in frame $U$.

### Solution

The rotation matrix is

$$
{}^{U}_{B}R=
\begin{bmatrix}
\cos 30^\circ & -\sin 30^\circ & 0 \\
\sin 30^\circ & \cos 30^\circ & 0 \\
0 & 0 & 1
\end{bmatrix}
=
\begin{bmatrix}
0.8660 & -0.5 & 0 \\
0.5 & 0.8660 & 0 \\
0 & 0 & 1
\end{bmatrix}
$$

The translation vector is

$$
{}^{U}P_B = [5,2,0]^T
$$

Now,

$$
{}^{U}Q = {}^{U}_{B}R\,{}^{B}Q + {}^{U}P_B
$$

$$
{}^{U}_{B}R\,{}^{B}Q =
\begin{bmatrix}
0.8660 & -0.5 & 0 \\
0.5 & 0.8660 & 0 \\
0 & 0 & 1
\end{bmatrix}
\begin{bmatrix}
2 \\
1 \\
0
\end{bmatrix}
=
\begin{bmatrix}
1.2321 \\
1.8660 \\
0
\end{bmatrix}
$$

Therefore,

$$
{}^{U}Q =
\begin{bmatrix}
1.2321 \\
1.8660 \\
0
\end{bmatrix}
+
\begin{bmatrix}
5 \\
2 \\
0
\end{bmatrix}
=
\begin{bmatrix}
6.2321 \\
3.8660 \\
0
\end{bmatrix}
$$

### Final answer

$$
{}^{U}Q = [6.2321,3.8660,0]^T
$$

## Q2. Inverse kinematics of a 2-DOF planar manipulator

### Given

$$
L_1=15\text{ cm}, \qquad L_2=10\text{ cm}, \qquad (q_x,q_y)=(20,5)
$$

### Solution

First,

$$
\cos θ_2 = \frac{q_x^2+q_y^2-L_1^2-L_2^2}{2L_1L_2}
$$

$$
\cos θ_2 = \frac{20^2+5^2-15^2-10^2}{2(15)(10)}
+=\frac{400+25-225-100}{300}
+=\frac{100}{300}
+=0.3333
$$

Hence,

$$
θ_2 = \pm \cos^{-1}(0.3333)=\pm 70.53^\circ
$$

Now,

$$
θ_1 = \tan^{-1}\left(\frac{q_y}{q_x}\right) - \tan^{-1}\left(\frac{L_2\sin θ_2}{L_1 + L_2\cos θ_2}\right)
$$

Also,

$$
\tan^{-1}\left(\frac{5}{20}\right)=14.04^\circ
$$

For the elbow-up solution,

$$
θ_1 = 14.04^\circ - \tan^{-1}\left(\frac{10\sin 70.53^\circ}{15 + 10\cos 70.53^\circ}\right)
+=-13.18^\circ
$$

For the elbow-down solution,

$$
θ_1 = 14.04^\circ - \tan^{-1}\left(\frac{10\sin(-70.53^\circ)}{15 + 10\cos(-70.53^\circ)}\right)
+=41.25^\circ
$$

### Final answer

Elbow-up:

$$
θ_1=-13.18^\circ, \qquad θ_2=70.53^\circ
$$

Elbow-down:

$$
θ_1=41.25^\circ, \qquad θ_2=-70.53^\circ
$$

## Q3. Cubic polynomial trajectory

### Given

$$
θ_i=10^\circ, \qquad θ_f=70^\circ, \qquad T=2\text{ s}
$$

The robot starts and ends at rest.

### Solution

Assume

$$
θ(t)=a_0+a_1t+a_2t^2+a_3t^3
$$

Then,

$$
\dot{θ}(t)=a_1+2a_2t+3a_3t^2
$$

Applying the boundary conditions,

$$
θ(0)=10 \Rightarrow a_0=10
$$

$$
\dot{θ}(0)=0 \Rightarrow a_1=0
$$

$$
θ(2)=70 \Rightarrow 10+4a_2+8a_3=70
$$

$$
4a_2+8a_3=60
$$

$$
\dot{θ}(2)=0 \Rightarrow 2a_2+6a_3=0
$$

From the last equation,

$$
a_2=-3a_3
$$

Substitute into $4a_2+8a_3=60$:

$$
4(-3a_3)+8a_3=60
$$

$$
-12a_3+8a_3=60
$$

$$
-4a_3=60 \Rightarrow a_3=-15
$$

Hence,

$$
a_2=45
$$

Therefore,

$$
θ(t)=10+45t^2-15t^3
$$

At $t=1$,

$$
θ(1)=10+45(1)^2-15(1)^3=40^\circ
$$

### Final answer

$$
θ(t)=10+45t^2-15t^3
$$

$$
θ(1)=40^\circ
$$

## Q4. Moment of inertia of a slender circular link

### Given

$$
m=2\text{ kg}, \qquad l=0.5\text{ m}, \qquad r=0.02\text{ m}
$$

Using

$$
I_{xx}=\frac{1}{2}mr^2, \qquad I_{yy}=\frac{1}{3}ml^2+\frac{1}{4}mr^2
$$

### Solution

$$
I_{xx}=\frac{1}{2}(2)(0.02)^2=0.0004
$$

$$
I_{yy}=\frac{1}{3}(2)(0.5)^2+\frac{1}{4}(2)(0.02)^2
$$

$$
I_{yy}=0.1666667+0.0002=0.1668667
$$

### Final answer

$$
I_{xx}=0.0004
$$

$$
I_{yy}=0.1669
$$

Units are kg $m^2$ .

## Q5. Gravity torque at Joint 2

### Note on interpretation

The PDF hint is OCR-distorted. The standard robotics interpretation used here is

$$
C_2=\frac{1}{2}m_2gL_2\cos(θ_1+θ_2)
$$

### Given

$$
m_2=1.5\text{ kg}, \qquad L_2=0.4\text{ m}, \qquad g=9.81\text{ m/s}^2
$$

$$
θ_1=30^\circ, \qquad θ_2=15^\circ
$$

### Solution

$$
θ_{12}=θ_1+θ_2=45^\circ
$$

$$
C_2=\frac{1}{2}(1.5)(9.81)(0.4)\cos 45^\circ
$$

$$
C_2=0.75\times 9.81\times 0.4\times 0.7071=2.081
$$

### Final answer

$$
C_2 \approx 2.08
$$

Unit is N m.

## Q6. Kinetic energy of a single-link robot

### Given

$$
\dot{q}_1=2\text{ rad/s}, \qquad \operatorname{Tr}(U_{11}J_1U_{11}^{T})=0.8
$$

For this case,

$$
K_1=\frac{1}{2}\operatorname{Tr}(U_{11}J_1U_{11}^{T})\dot{q}_1^2
$$

### Solution

$$
K_1=\frac{1}{2}(0.8)(2)^2=0.4\times 4=1.6
$$

### Final answer

$$
K_1=1.6
$$

Unit is joule.

## Q7. Forward kinematics of a 2-DOF planar arm

### Given

$$
L_1=20\text{ cm}, \qquad L_2=15\text{ cm}, \qquad θ_1=30^\circ, \qquad θ_2=45^\circ
$$

### Solution

$$
q_x=L_1\cos θ_1 + L_2\cos(θ_1+θ_2)
$$

$$
q_y=L_1\sin θ_1 + L_2\sin(θ_1+θ_2)
$$

$$
q_x=20\cos 30^\circ+15\cos 75^\circ
+=20(0.8660)+15(0.2588)
+=21.2028\text{ cm}
$$

$$
q_y=20\sin 30^\circ+15\sin 75^\circ
+=20(0.5)+15(0.9659)
+=24.4889\text{ cm}
$$

### Final answer

$$
(q_x,q_y)=(21.20\text{ cm},\ 24.49\text{ cm})
$$

## Q8. Moment of inertia of a rectangular link about the $z$-axis

### Note on interpretation

The hint in the PDF is OCR-distorted. The interpreted formula used here is

$$
I_{zz}=m\left(\frac{l^2}{3}+\frac{a^2}{12}\right)
$$

### Given

$$
m=5\text{ kg}, \qquad l=1\text{ m}, \qquad a=0.1\text{ m}, \qquad b=0.1\text{ m}
$$

### Solution

$$
I_{zz}=5\left(\frac{1^2}{3}+\frac{0.1^2}{12}\right)
$$

$$
I_{zz}=5(0.333333+0.000833)=1.67083
$$

### Final answer

$$
I_{zz}=1.6708
$$

Unit is kg m$^2$.

## Q9. Torque component due to Coriolis or centrifugal effect

### Given

$$
m_2=2\text{ kg}, \qquad L_1=0.5\text{ m}, \qquad L_2=0.5\text{ m}
$$

$$
θ_2=90^\circ, \qquad \dot{θ}_2=3\text{ rad/s}
$$

Using

$$
h_{122}=-\frac{1}{2}m_2L_1L_2\sin θ_2
$$

### Solution

Since $\sin 90^\circ=1$,

$$
h_{122}=-\frac{1}{2}(2)(0.5)(0.5)(1)=-0.25
$$

Hence,

$$
h_{122}\dot{θ}_2^{\,2}=(-0.25)(3^2)=(-0.25)(9)=-2.25
$$

### Final answer

$$
h_{122}\dot{θ}_2^{\,2}=-2.25
$$

## Q10. Moment of inertia of a circular link

### Given

$$
m=3\text{ kg}, \qquad l=0.8\text{ m}, \qquad r=0.05\text{ m}
$$

Using

$$
I_{xx}=\frac{1}{2}mr^2
$$

### Solution

$$
I_{xx}=\frac{1}{2}(3)(0.05)^2=1.5\times 0.0025=0.00375
$$

### Final answer

$$
I_{xx}=0.00375
$$

Unit is kg m$^2$.

## Final formula sheet for revision

$$
{}^{U}Q = {}^{U}_{B}R \; {}^{B}Q + {}^{U}P_B
$$

$$
R_z(θ)=
\begin{bmatrix}
\cos θ & -\sin θ & 0 \\
\sin θ & \cos θ & 0 \\
0 & 0 & 1
\end{bmatrix}
$$

$$
q_x = L_1 \cos θ_1 + L_2 \cos(θ_1 + θ_2)
$$

$$
q_y = L_1 \sin θ_1 + L_2 \sin(θ_1 + θ_2)
$$

$$
\cos θ_2 = \frac{q_x^2 + q_y^2 - L_1^2 - L_2^2}{2L_1L_2}
$$

$$
θ(t)=a_0+a_1 t+a_2 t^2+a_3 t^3
$$

$$
\dot{θ}(t)=a_1+2a_2 t+3a_3 t^2
$$

$$
I_{xx}=\frac{1}{2}mr^2
$$

$$
I_{yy}=\frac{1}{3}ml^2+\frac{1}{4}mr^2
$$

$$
I_{zz}=m\left(\frac{l^2}{3}+\frac{a^2}{12}\right)
$$

$$
C_2=\frac{1}{2}m_2gL_2\cos(θ_1+θ_2)
$$

$$
K_1=\frac{1}{2}\operatorname{Tr}(U_{11}J_1U_{11}^{T})\dot{q}_1^2
$$

$$
h_{122}=-\frac{1}{2}m_2L_1L_2\sin θ_2
$$
