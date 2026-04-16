# Lab 11 – Graph Generation Models
**CS342 Social Network Analysis | U23CS014 – Naishadh Rana**

---

## Overview

This lab explores three classical models for generating synthetic networks and compares their structural properties.

| Model | NetworkX Function | Parameters |
|---|---|---|
| Erdős–Rényi (ER) | `nx.erdos_renyi_graph()` | n=500, p=0.05 |
| Watts–Strogatz (WS) | `nx.watts_strogatz_graph()` | n=500, k=10, β=0.1 |
| Barabási–Albert (BA) | `nx.barabasi_albert_graph()` | n=500, m=5 |

---

## Cell-by-Cell Explanation

### Cell 1 – Imports
Loads `networkx` (graph construction & analysis), `matplotlib.pyplot` (plotting), `numpy` (numerical ops), and `collections.Counter` (degree-frequency counting for the log-log plot).

---

### Cell 2 – Erdős–Rényi Graph
`nx.erdos_renyi_graph(n=500, p=0.05, seed=42)` creates a random graph where every possible edge between 500 nodes is included independently with probability **p = 0.05**. The expected average degree is `(n-1) × p ≈ 24.95`. The `seed` ensures reproducibility.

---

### Cell 3 – Watts–Strogatz Graph
`nx.watts_strogatz_graph(n=500, k=10, p=0.1, seed=42)` builds a ring lattice where each node first connects to its **k/2 = 5 nearest neighbours** on each side, then every edge is **rewired** with probability **β = 0.1**. A low β retains high clustering; a higher β adds the short path lengths characteristic of small-world networks.

---

### Cell 4 – Barabási–Albert Graph
`nx.barabasi_albert_graph(n=500, m=5, seed=42)` grows the network incrementally: each new node adds **m = 5 edges**, preferentially attaching to nodes with higher degree. This **preferential attachment** rule produces a **power-law** (scale-free) degree distribution.

---

### Cell 5 – Visualizations
Three side-by-side spring-layout plots (node size 10) give a visual intuition of network structure:
- **ER** – fairly uniform, no clear hub structure.
- **WS** – ring-like clusters with some shortcuts.
- **BA** – star-shaped hubs visible in the centre.

Each graph is rendered with `nx.draw_networkx()` using distinct colours for quick identification.

---

### Cell 6 – Comparative Metrics (`get_metrics` function)
Four structural statistics are computed for each model:

| Metric | What it measures |
|---|---|
| **Average Degree** | Mean number of edges per node; controls overall connectivity density. |
| **Average Clustering Coefficient** | Tendency for a node's neighbours to also be connected to each other; measures local cohesion. |
| **Average Shortest Path Length** | Mean number of hops to travel between any two nodes; measures global navigation efficiency. |
| **Diameter** | Longest shortest path in the graph; the worst-case separation. |

Because the ER graph with p=0.05 may have isolated nodes, the function checks connectivity and falls back to the **Largest Connected Component (LCC)** for path-based metrics.

---

### Cell 7 – Degree Distribution Plots
A 2×2 subplot grid:
- **Top-left / top-right / bottom-left:** Linear-scale histograms for ER, WS, and BA respectively.
  - ER shows a symmetric Poisson-like bell curve.
  - WS shows a narrow spike (most nodes have exactly k=10 neighbours after mild rewiring).
  - BA shows a right-skewed distribution with a long tail.
- **Bottom-right:** Log-log scatter plot for the BA model. A straight line on a log-log plot is the hallmark of a **power law** — confirming scale-free behaviour.

---

### Cell 8 – Save as GEXF (Gephi format)
`nx.write_gexf()` serialises each graph to a `.gexf` XML file. Open these files in [Gephi](https://gephi.org/) to apply ForceAtlas2 layouts, colour nodes by degree, and export publication-quality images via the **Preview** tab.

---

### Cell 9 – Gephi Visualizations *(placeholder)*
After creating PNG exports in Gephi, embed them here using Markdown:
```markdown
![ER Gephi](path/to/er_gephi.png)
```

---

### Cell 10 – Discussion
This cell is a written analysis. Key points:

- **BA is more realistic** because most real networks (internet, social media, citation networks) exhibit a **power-law degree distribution** — a small number of hubs attract the majority of connections.
- The underlying mechanism is **preferential attachment**: new entrants connect to already-popular nodes, amplifying existing inequalities ("rich get richer").
- The ER model lacks this growth rule; its random edges produce a bell-shaped degree distribution that rarely matched empirical data from real-world networks.
- The WS model captures **high clustering** and **short path lengths** (small-world property) but not the power-law degree distribution.

---

## Dependencies

```
networkx
matplotlib
numpy
```

Install with:
```bash
pip install networkx matplotlib numpy
```
