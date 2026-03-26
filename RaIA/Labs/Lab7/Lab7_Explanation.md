# Lab 7: Inverse Dynamics Explanation

## Part A: Lagrange-Euler Inverse Dynamics

### 2. Manual Calculation

**Objective:** Calculate the instantaneous joint torques ($\tau_1$ and $\tau_2$) required for the 2-DOF planar robot at $t = 2.5$ seconds using the Lagrange-Euler formulation.

**Given Parameters:**
* **Link Lengths:** $L_1 = 1.0$ m, $L_2 = 1.0$ m
* **Link Masses (assumed as point masses at distal ends):** $m_1 = 4.0$ kg, $m_2 = 2.0$ kg
* **Friction Constants:** Coulomb friction $f_c = 1.5$ Nm, Viscous friction $v = 0.3$ Nm$\cdot$s/rad
* **Gravity:** $g = 9.81$ m/s$^2$

---

#### Step 1: Define the Desired Trajectory Equations
The problem specifies a smooth sine profile that moves the arm from a horizontal rest position ($\theta_1=0$, $\theta_2=0$) to a vertical position ($\theta_1=\pi/2$, $\theta_2=0$) over 5 seconds. Based on the provided formulation, we have:

* **Position profiles:**
  $$ \theta_1(t) = \frac{\pi}{4} \left( 1 - \cos\left(\frac{\pi t}{5}\right) \right) $$
  $$ \theta_2(t) = \frac{\pi}{4} \sin\left(\frac{\pi t}{5}\right) $$

* **Velocity profiles** (First derivative with respect to time):
  $$ \dot{\theta}_1(t) = \frac{\pi^2}{20} \sin\left(\frac{\pi t}{5}\right) $$
  $$ \dot{\theta}_2(t) = \frac{\pi^2}{20} \cos\left(\frac{\pi t}{5}\right) $$

* **Acceleration profiles** (Second derivative with respect to time):
  $$ \ddot{\theta}_1(t) = \frac{\pi^3}{100} \cos\left(\frac{\pi t}{5}\right) $$
  $$ \ddot{\theta}_2(t) = -\frac{\pi^3}{100} \sin\left(\frac{\pi t}{5}\right) $$

---

#### Step 2: Evaluate Kinematics at $t = 2.5$ seconds
At the target evaluate time $t = 2.5$ s, we can solve the internal argument in our trigonometric functions: $\frac{\pi (2.5)}{5} = \frac{\pi}{2}$.
Substituting this into our equations above:

**Joint 1:**
* **Position:** $\theta_1(2.5) = \frac{\pi}{4}(1 - \cos(\frac{\pi}{2})) = \frac{\pi}{4}$ rad $\approx 0.785$ rad
* **Velocity:** $\dot{\theta}_1(2.5) = \frac{\pi^2}{20}\sin(\frac{\pi}{2}) = \frac{\pi^2}{20} \approx 0.493$ rad/s
* **Acceleration:** $\ddot{\theta}_1(2.5) = \frac{\pi^3}{100}\cos(\frac{\pi}{2}) = 0$ rad/s$^2$

**Joint 2:**
* **Position:** $\theta_2(2.5) = \frac{\pi}{4}\sin(\frac{\pi}{2}) = \frac{\pi}{4}$ rad $\approx 0.785$ rad
* **Velocity:** $\dot{\theta}_2(2.5) = \frac{\pi^2}{20}\cos(\frac{\pi}{2}) = 0$ rad/s
* **Acceleration:** $\ddot{\theta}_2(2.5) = -\frac{\pi^3}{100}\sin(\frac{\pi}{2}) = -\frac{\pi^3}{100} \approx -0.310$ rad/s $^2$

---

#### Step 3: Compute the Dynamic Matrices and Vectors
The general manipulator equation is:
$$ \tau = M(\theta)\ddot{\theta} + V(\theta, \dot{\theta}) + G(\theta) + F(\dot{\theta}) $$

**A. Inertia Matrix $M(\theta)$**
The $2 \times 2$ inertia matrix for a planar RR robot with point masses expands to:
* $M_{11} = (m_1+m_2)L_1^2 + m_2 L_2^2 + 2m_2 L_1 L_2 \cos\theta_2$
  $M_{11} = (4+2)(1)^2 + 2(1)^2 + 2(2)(1)(1)\cos(\frac{\pi}{4}) = 6 + 2 + 4(\frac{\sqrt{2}}{2}) \approx 10.828$ kg $\cdot$ m $^2$
* $M_{12} = M_{21} = m_2 L_2^2 + m_2 L_1 L_2 \cos\theta_2$
  $M_{12} = 2(1)^2 + 2(1)(1)\cos(\frac{\pi}{4}) = 2 + 2(\frac{\sqrt{2}}{2}) \approx 3.414$ kg $\cdot$ m $^2$
* $M_{22} = m_2 L_2^2$
  $M_{22} = 2(1)^2 = 2.0$ kg $\cdot$ m $^2$

**B. Coriolis and Centrifugal Vector $V(\theta, \dot{\theta})$**
Let $h = -m_2 L_1 L_2 \sin\theta_2$ be the velocity coupling factor component.
$h = -2(1)(1)\sin(\frac{\pi}{4}) = -2(\frac{\sqrt{2}}{2}) \approx -1.414$
* $V_1 = h \cdot (2\dot{\theta}_1\dot{\theta}_2 + \dot{\theta}_2^2)$
  Since the formula contains $\dot{\theta}_2$ in all terms and $\dot{\theta}_2 = 0$, $V_1 = -1.414 \cdot (0 + 0) = 0$ Nm
* $V_2 = -h \cdot \dot{\theta}_1^2$
  $V_2 = -(-1.414)(0.493)^2 = 1.414 \cdot 0.243 \approx 0.344$ Nm

**C. Gravity Vector $G(\theta)$**
The gravitational torques are derived from the potential energy:
* $G_1 = (m_1+m_2)g L_1 \cos\theta_1 + m_2 g L_2 \cos(\theta_1+\theta_2)$
  $G_1 = (6)(9.81)\cos(\frac{\pi}{4}) + (2)(9.81)\cos(\frac{\pi}{2})$
  $G_1 = 58.86(0.707) + 19.62(0) \approx 41.62$ Nm
* $G_2 = m_2 g L_2 \cos(\theta_1+\theta_2)$
  $G_2 = 2(9.81)\cos(\frac{\pi}{4} + \frac{\pi}{4}) = 19.62\cos(\frac{\pi}{2}) = 0$ Nm

**D. Friction Vector $F(\dot{\theta})$**
The frictional force includes both Coulomb ($f_c$) and viscous ($v$) friction modeled together:
* $F_1 = f_c \cdot \text{sgn}(\dot{\theta}_1) + v \cdot \dot{\theta}_1$
  $F_1 = 1.5 \cdot \text{sgn}(0.493) + 0.3(0.493) = 1.5(1) + 0.148 \approx 1.648$ Nm
* $F_2 = f_c \cdot \text{sgn}(\dot{\theta}_2) + v \cdot \dot{\theta}_2$
  Since $\dot{\theta}_2 = 0$, $F_2 = 0$ Nm

---

#### Step 4: Calculate Final Joint Torques
Finally, we substitute all the calculated matrix and vector components back into the manipulator equation for each respective joint.

**For Joint 1:**
$$ \tau_1 = (M_{11}\ddot{\theta}_1 + M_{12}\ddot{\theta}_2) + V_1 + G_1 + F_1 $$
$$ \tau_1 = [10.828(0) + 3.414(-0.310)] + 0 + 41.62 + 1.648 $$
$$ \tau_1 = -1.058 + 41.62 + 1.648 \approx 42.21 \text{ Nm} $$

**For Joint 2:**
$$ \tau_2 = (M_{21}\ddot{\theta}_1 + M_{22}\ddot{\theta}_2) + V_2 + G_2 + F_2 $$
$$ \tau_2 = [3.414(0) + 2.0(-0.310)] + 0.344 + 0 + 0 $$
$$ \tau_2 = -0.620 + 0.344 \approx -0.276 \text{ Nm} $$

**Conclusion for Checkpoint:**
At exactly $2.5$ seconds into the trajectory, Joint 1 must provide roughly $42.21$ Nm of torque. This is large primarily because it is counteracting gravity while heavily extended. Joint 2 requires a small negative torque of $-0.276$ Nm, meaning it is acting as a brake because the dynamic coupling from the robot's motion wants to accelerate it in the reverse direction.

---

### 4. Lab Report Questions
**1. Peak Torque:**  
The torque at Joint 1 is highest around $t=0$ and $t=5$ seconds due to **gravity**. At these positions, the robot arm is closest to horizontal, which maximizes the perpendicular distance of the center of mass from the base joint. Because gravity pulls vertically down, this horizontal alignment requires the absolute maximum holding torque.

**2. Negative Torque:**  
Yes, we encounter negative torque values for Joint 2. A motor needs to provide "negative" torque during an upward lift when inertial coupling or gravity naturally accelerates the joint faster than the trajectory allows. To stick to the mathematically precise "smooth upward" trajectory, the Joint 2 motor must actively brake (apply torque opposite to the motion) to prevent the arm from overshooting or moving too fast.

**3. Coupling Analysis:**  
If the acceleration of Joint 2 ($\ddot{\theta}_2$) is increased to be very high, it significantly affects the required torque at Joint 1, even if Joint 1 is stationary ($\dot{\theta}_1 = 0, \ddot{\theta}_1 = 0$). This occurs due to the **inertial coupling** term $M_{12} \ddot{\theta}_2$. The rapid acceleration of the second link generates a reaction force at the elbow that attempts to whip the first link backwards. Joint 1's motor must compensate simply to hold its position.

---

### 5. Bonus Challenge
If a payload of 2 kg is added to the end-effector, the effective mass $m_2$ increases to 4 kg. 
The Inertia Matrix $M(\theta)$ contains the term $2m_2 L_1 L_2 \cos \theta_2$. 
- When the robot is **fully extended** ($\theta_2 = 0$), $\cos\theta_2 = 1$, maximizing this coupling term. The inertia matrix elements ($M_{11}$) become extremely large, reflecting the high rotational inertia of an elongated arm.
- When the arm is **tucked in** ($\theta_2 = \pm\pi$), $\cos\theta_2 = -1$, which subtracts from the baseline inertia and minimizes $M_{11}$, making the entire arm physically much easier to rotate from the base.

---

## Part B: Resolved-Rate Control
In Part B, we implemented resolved-rate control, utilizing the manipulator Jacobian to convert a desired constant Cartesian end-effector velocity (0.5 m/s upwards) into required joint rates $d\Theta = J^{-1} V_X$. After tracking the trajectory iteratively using numerical differentiation, we computed inverse dynamics for standard steel distributed links.

- **Case A (Gravity Off):** Torque is purely devoted to overcoming the non-linear inertial accelerations $M\ddot{\theta}$ and Coriolis effects $V$ as the arm configuration changes dynamically to maintain constant linear speed.
- **Case B (Gravity On):** The continuous upward demand against gravity places massive, sustained torque requests on Joint 1, dominating the comparatively small inertial components isolated in Case A.
