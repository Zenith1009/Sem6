# Social Network Analysis — Assignment 3 Viva Notes

## What the assignment covers
- Build and visualize a small custom undirected, unweighted graph.
- Compute and interpret closeness centrality on the custom graph.
- Compute and interpret betweenness centrality on the custom graph.
- Load and visualize the Zachary Karate Club network.
- Compute closeness and betweenness centralities on the Karate Club network.
- Identify the most central nodes by both measures and reason about why.

## Core formulas and concepts
- Graph setup: simple, undirected, unweighted graphs. Shortest path distance between nodes \(u\) and \(v\) is \(d(u,v)\) measured in hops.
- Closeness centrality of node \(u\):
  \[
  C_{\text{close}}(u) = \frac{n-1}{\sum_{v \neq u} d(u,v)}
  \]
  where \(n\) is the number of nodes. Intuition: nodes with smaller total distance to everyone else can reach the network quickly (good broadcasters).
- Betweenness centrality of node \(u\):
  \[
  C_{\text{bet}}(u) = \sum_{s \neq u \neq t} \frac{\sigma_{st}(u)}{\sigma_{st}}
  \]
  where \(\sigma_{st}\) is the number of shortest paths from \(s\) to \(t\), and \(\sigma_{st}(u)\) is those paths that pass through \(u\). Intuition: nodes that sit on many shortest routes act as brokers or bridges.
- Both measures here use the normalized versions returned by NetworkX for undirected graphs.

**Readable equations (block form)**

$$
 C_{\text{close}}(u) = \frac{n - 1}{\sum_{v \ne u} d(u,v)}
$$

$$
 C_{\text{bet}}(u) = \sum_{s \ne u \ne t} \frac{\sigma_{st}(u)}{\sigma_{st}}
$$

where:
- \(n\): total nodes
- \(d(u,v)\): shortest-path distance (hops)
- \(\sigma_{st}\): number of shortest paths from \(s\) to \(t\)
- \(\sigma_{st}(u)\): those shortest paths that pass through \(u\)

## Task-by-task reasoning

### Task 1 — Create the custom network
- Edges defined: \((1,3), (1,2), (2,3), (2,5), (3,5), (3,4), (4,5)\).
- Constructed an undirected graph and drew it with labels. Purpose: have a small, interpretable network to practice centrality.
- Quick structural intuition: nodes 2,3,5 have higher degree; node 4 connects mainly via 3 and 5, suggesting possible brokerage roles for 3 or 5.

### Task 2 — Closeness centrality on the custom network
- Used `nx.closeness_centrality(CGraph)` which applies the closeness formula above.
- Expectation: nodes that minimize total distance to others score higher. Here nodes 2, 3, and 5 are each within 1–2 hops of everyone, so they should be top.
- Interpretation: a higher closeness node can reach others faster (useful for fast dissemination).

### Task 3 — Betweenness centrality on the custom network
- Used `nx.betweenness_centrality(CGraph)` with default normalization.
- Expectation: node 3 (and possibly 5) sit on many of the shortest paths connecting 1,2,4,5, so they should have the highest betweenness. Node 1 should be low because it is peripheral.
- Interpretation: a higher betweenness node controls flow between subparts (good brokers).

### Task 4 — Display the Karate Club network
- Loaded via `nx.karate_club_graph()`. This classic 34-node network captures friendships in a karate club before it split.
- Drew with spring layout, scaling node sizes by degree to visually hint at centrality. Purpose: contextualize where central nodes sit.

### Task 5 — Closeness centrality on Karate Club
- Computed `nx.closeness_centrality(karate)`.
- Intuition: central club members (notably nodes 0 and 33 in the NetworkX labeling) should have the highest closeness because they are close to most others.
- Use: identifies who can quickly reach the whole club if they spread information.

### Task 6 — Betweenness centrality on Karate Club
- Computed `nx.betweenness_centrality(karate)`.
- Intuition: the same key members (nodes 0 and 33) are expected to broker many shortest paths between subgroups, giving them top betweenness.
- Use: highlights potential bridge actors whose removal could fragment communication.

### Task 7 — Identify most important nodes
- Helper `top_nodes` extracts the maximum value(s) from each centrality dictionary.
- Reported top nodes for both metrics. In the Karate Club graph, nodes 0 and 33 typically emerge as highest for both closeness and betweenness, reflecting their hub/bridge roles between factions.
- Insight: agreement between closeness and betweenness indicates nodes that are both well-positioned globally (short reach) and structurally critical (broker paths).

## General reasoning and checks
- Chose undirected, unweighted centralities to match the provided graphs (no direction or weights specified).
- Normalization in NetworkX keeps scores comparable across graphs.
- Visual checks (degree-sized nodes in the plot) align with the computed centralities: high-degree hubs often have higher closeness and betweenness, but betweenness also depends on path structure, not just degree.

## How to discuss results in a viva
- Define each metric succinctly and give its formula.
- Explain what “high” means for each metric (reach vs brokerage).
- Use the custom graph as a toy example: describe why node 3 (and 5) are brokers and why peripheral nodes score lower.
- For the Karate Club, link high scores of nodes 0 and 33 to their known real-world roles in the club split (they connect many members and factions).
- Mention limitations: unweighted, undirected assumptions; centrality can shift if weights/directions change.
