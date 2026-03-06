# Assignment 7 Viva Notes | HITS Algorithm

## 1) What this lab does
- Implemented **HITS (Hyperlink-Induced Topic Search)**.
- Ran it on:
  1. Karate Club graph (NetworkX dataset)
  2. Extended SVNIT web graph (crawled from https://www.svnit.ac.in/)
- Reported highest/lowest **hub** and **authority** nodes.
- Visualized node sizes based on hub and authority scores.

---

## 2) Core idea of HITS
Each node gets 2 scores:
- **Hub score**: high if it points to high-authority nodes.
- **Authority score**: high if pointed to by high-hub nodes.

### Update equations
$$a(v) = \sum_{u\rightarrow v} h(u)$$
$$h(v) = \sum_{v\rightarrow w} a(w)$$

where:
- $a(v)$: authority score of node $v$
- $h(v)$: hub score of node $v$
- $u\rightarrow v$: nodes $u$ that point to $v$
- $v\rightarrow w$: nodes $w$ that $v$ points to


After each iteration, normalize both vectors (L2 norm):
$$\|a\|_2 = \sqrt{\sum_i a_i^2},\quad \|h\|_2 = \sqrt{\sum_i h_i^2}$$

Stop when total change is very small (convergence).

---

## 3) Final results from the run

## Karate Club
- Highest hub: node **33** (0.373363)
- Highest authority: node **33** (0.373363)
- Lowest hub: node **16** (0.023636)
- Lowest authority: node **16** (0.023636)
- Top 5 hubs/authorities: **33, 0, 2, 32, 1**

## Extended SVNIT web graph
- Nodes: **535**
- Edges: **5753**
- Highest hub URL: **https://www.svnit.ac.in/** (0.111765)
- Highest authority URL: **https://help.ccc.svnit.ac.in** (0.128290)
- Lowest hub URL: **https://mis.svnit.ac.in/SVNIT/** (0.000000)
- Lowest authority URL: **https://mis.svnit.ac.in/mispay/default.aspx** (0.000000)

---

## 4) Key interpretation points for viva
- Hubs are usually pages that **link out to many important pages**.
- Authorities are pages that are **endorsed by many strong hubs**.
- In web graphs, hub and authority often differ strongly.
- In smaller/social graphs, top hub and authority can overlap.

---

## 5) Common viva questions (quick answers)

### Q1. Difference between PageRank and HITS?
- **PageRank** gives one global importance score.
- **HITS** gives two scores: hub and authority.

### Q2. Why normalize every iteration?
- Without normalization, values keep growing and become unstable.

### Q3. Why directed graph is important for HITS?
- HITS depends on edge direction ($u\rightarrow v$) to define endorsement.

### Q4. What is a good hub in SVNIT dataset?
- A page like homepage/notice/department index pages that point to many relevant internal pages.

### Q5. What is a good authority in SVNIT dataset?
- A page that receives many links from major hub-like pages.

---

## 6) One-line conclusion
HITS successfully identified link-provider pages (hubs) and trusted target pages (authorities), and results were more differentiated in the extended SVNIT web graph than in Karate Club.
