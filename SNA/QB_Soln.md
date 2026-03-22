# Week 1 – Introduction to Social Network Analysis

### 1. Why does attribute-based analysis fail to explain decentralized rumor spread?

**Answer:**

* Traditional analysis focuses on **individual attributes** (wealth, influence, authority).
* In network phenomena, outcomes depend on **relationships and connectivity between nodes**.
* Rumor cascades occur due to **local clustering and repeated forwarding**, not because of a central leader.
* Therefore the **network structure, not the individual sender**, explains the spread.
  (SNA studies nodes and links to analyze such structures.) ([Wikipedia][1])

---

### 2. How can absence of corrective ties amplify misinformation cascades?

**Answer:**

* Corrective ties are connections that bring **contradictory or verified information**.
* If these links are absent, the message circulates only among **similar belief clusters**.
* Repeated reinforcement increases perceived credibility.
* This results in **uncontrolled cascades of misinformation**.

---

### 3. Why is identifying the original sender insufficient?

**Answer:**

* Diffusion occurs through **many intermediate nodes**, not just the origin.
* Messages propagate via **local forwarding chains**.
* Structural properties such as **cluster density and bridges** determine spread

---

# Week 3 – Network Structure and Centrality

### 1. Why may removing high-degree nodes fail to collapse a covert network?

**Answer:**

* High-degree nodes may be **visible but replaceable actors**.
* Real control often lies with **low-degree brokers connecting groups**.
* Removing only popular nodes does not break **critical communication paths**.
* Removing high-betweenness nodes fragments the network.

---

### 2. Why can a moderate-degree node with high betweenness be more important?

**Answer:**

* Betweenness centrality measures how often a node lies on **shortest paths between others**.
* Such nodes act as **bridges connecting communities**.
* Removing them **disconnects clusters**.
* Hence they control **information flow between groups**. ([Cambridge Intelligence][2])

---

### 3. Why do targeted attacks on hubs collapse scale-free networks?

**Answer:**

* Scale-free networks have **few highly connected hubs and many small nodes**.
* Hubs carry a large fraction of network connectivity.
* Random failures usually hit low-degree nodes.
* Targeted removal of hubs causes **rapid fragmentation**.

---

# Week 4 – Diffusion Structure and Trust

### 1. Why can information flow without adoption?

**Answer:**

* Exposure does not guarantee belief
* If edges have **low credibility**, influence fails.
* Hence information can **reach individuals but not change behavior**.

---

### 2. How does homophily create echo chambers?

**Answer:**

* Homophily means people prefer to connect with **similar individuals**.
* This produces clusters of **like-minded users**.
* Information circulates mainly within these clusters.
* As a result **echo chambers form**, reinforcing existing beliefs. ([ScienceDirect][3])

---

### 3. Why can symbolic messages spread faster than factual information?

**Answer:**

* Messages aligned with **identity or beliefs** spread more easily.
* People share content that reinforces **group identity and emotions**.
* Diffusion depends on **network trust and alignment**, not only accuracy.
* Thus symbolic messages trigger stronger cascades.

---

# Week 5 – Information Diffusion Models

### 1. Differentiate information flow, influence, and adoption.

**Answer:**

| Concept          | Meaning                                   |
| ---------------- | ----------------------------------------- |
| Information flow | Message exposure through network          |
| Influence        | Change in belief or attitude              |
| Adoption         | Observable action (purchase, vote, share) |

Adoption is the **strongest measurable outcome**.

---

### 2. Why does the SI model overestimate persistence?

**Answer:**

* SI assumes **no recovery or forgetting**.
* Once infected, nodes remain permanently active.
* Real social behavior includes **attention decay and loss of interest**.
* Hence SI predicts unrealistically **permanent diffusion**.

---

### 3. Why do threshold models capture peer pressure better?

**Answer:**

* Adoption occurs only when **enough neighbors adopt**.
* Individuals require **social reinforcement**.
* This models behaviors like **protests or technology adoption**.
* Diffusion depends on **collective influence rather than single exposure**.

---

# Week 6 – Behavioral Assumptions and Diffusion

### 1. How can the same topology produce different outcomes?

**Answer:**

* Network structure remains constant.
* Diffusion outcome depends on **behavioral rules**.
* SI → continuous spread
* SIR → rise and decline
* Threshold → cascade or no spread
  Different assumptions lead to **different dynamics**.

---

### 2. Why do threshold models produce “all-or-nothing” cascades?

**Answer:**

* Adoption requires reaching a **critical proportion of neighbors**.
* If threshold is not reached, diffusion stops.
* Once critical mass is reached, rapid cascade occurs.
* Hence diffusion is **nonlinear and sudden**. ([Wikipedia][4])

---

### 3. Significance of (R_0 = \beta / \gamma)

**Answer:**

* ( \beta ) = transmission probability
* ( \gamma ) = recovery probability
* If ( R_0 > 1 ) → infection spreads exponentially.
* If ( R_0 < 1 ) → diffusion dies out.

---

# Week 7 – Echo Chambers and Diffusion Models

### 1. Why does repeated exposure increase adoption probability?

**Answer:**

* Multiple exposures provide **social reinforcement**.
* Individuals perceive **consensus among peers**.
* This reduces skepticism.
* Threshold for adoption is eventually crossed.

---

### 2. Why does cross-community diffusion remain weak?

**Answer:**

* Few connections exist between communities.
* Inter-group edges often have **low trust**
* Therefore diffusion rarely crosses clusters.

---

### 3. Compare SI, SIS, and SIR models.

| Model | Recovery                       | Long-term behavior           |
| ----- | ------------------------------ | ---------------------------- |
| SI    | No recovery                    | Everyone eventually infected |
| SIS   | Recovery but susceptible again | Infection persists           |
| SIR   | Recovery with immunity         | Spread eventually stops      |

---

# Week 8 – Diffusion Metrics and Interventions

### 1. Infection size vs cascade depth

| Metric         | Meaning                           |
| -------------- | --------------------------------- |
| Infection size | Total number of nodes influenced  

Both measure **reach and penetration** of diffusion.

---

### 2. Why is targeted immunization more effective?

**Answer:**

* Hubs have **many connections**.
* Infection through hubs spreads to large portions of the network.
* Vaccinating hubs blocks **multiple transmission paths**.
* Therefore targeted immunization is **far more efficient than random removal**.

---

### 3. Why does removing bridge edges contain diffusion?

**Answer:**

* Bridges connect **otherwise separate communities**.
* Removing them eliminates **cross-community paths**.
* Diffusion remains trapped inside local clusters.
* This prevents **global network cascades**.
