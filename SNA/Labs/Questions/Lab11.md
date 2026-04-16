# CS342 – Social Network Analysis  
**Assignment 11 – Graph Generation Models**  
**Date:** 24-Mar-2026  

---

## Objective
To understand the structural properties of different graph models by generating and analyzing networks using the **NetworkX** library.

---

## Tasks

1. Generate a random graph using the **Erdős–Rényi model** with:
   - \( n = 500 \) nodes  
   - Edge probability \( p = 0.05 \)

2. Generate a graph using the **Watts–Strogatz model** with:
   - \( n = 500 \) nodes  
   - Each node connected to \( k = 10 \) neighbors  
   - Rewiring probability \( \beta = 0.1 \)

3. Generate a graph using the **Barabási–Albert model** with:
   - \( n = 500 \) nodes  
   - \( m = 5 \) edges added for each new node  

4. Use the following NetworkX functions:
   - `nx.erdos_renyi_graph()`  
   - `nx.watts_strogatz_graph()`  
   - `nx.barabasi_albert_graph()`  

5. Save all three graphs in a **Gephi-compatible format**.

6. Create aesthetic visualizations of the graphs in **Gephi**.

---

## Deliverables

Students must submit a report/notebook containing:

### 1. Visualizations
- A plot for each of the three graphs.  
- *Hint:* For \( n = 500 \), use a small node size (e.g., `node_size = 10`).

---

### 2. Comparative Table

| Metric                        | Erdős–Rényi | Watts–Strogatz | Barabási–Albert |
|-----------------------------|------------|---------------|----------------|
| Average Degree              |            |               |                |
| Average Clustering Coefficient |        |               |                |
| Average Shortest Path Length |           |               |                |
| Diameter                    |            |               |                |

---

### 3. Degree Distribution Plots
- Three histograms (one per model) showing the frequency of node degrees.

---

### 4. Discussion
Write a brief paragraph explaining why the **Barabási–Albert model** is often considered more *realistic* for social networks or the internet compared to the **Erdős–Rényi model**.

---

### 5. Gephi Visualizations
- Include visual representations of all graphs created in Gephi.

---

## Note
- The degree distribution can be visualized using:
  - `matplotlib.pyplot.hist()`  
  - A **log-log plot** for the Barabási–Albert model to observe the **power-law distribution**.