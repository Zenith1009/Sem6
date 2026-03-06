# Assignment 8 | Citation Network: Creation and Analysis

## Problem Statement
Build and analyze an institute-wise citation/collaboration network.

For case study, consider:
- One department
- One or two professors
- Publications from last 2-3 years

You need to:
- Analyze and visualize the collaboration network among professors and coauthors between **SVNIT** and **Institute_X**.
- Understand research interest groups and community structures inside the network.

## Data to be Used
- Professor names
- Citations
- h-index
- Research interests
- Coauthors

You may use Google Scholar's Python module **scholarly** to collect this data.

Using this data, construct a citation/collaboration network and analyze it with graph-based statistical measures such as:
- Degree centrality
- Influence
- Degree of connectivity

Demonstrate findings with appropriate plots.

---

## Part I — Create Citation/Collaboration Network

1) Select one department and identify one or two professors from SVNIT and Institute_X.
2) Collect last 2-3 years publication and coauthor information.
3) Build a graph where nodes represent authors and edges represent collaboration.
4) Add useful node attributes (institute, citations, h-index, research interests, etc.).
5) Visualize the constructed network.

---

## Part II — Network Analysis

Analyze the network using graph statistics:
- a. Degree centrality and key influential nodes
- b. Connectivity patterns (components, density, average degree)
- c. Community structure / research groups
- d. Other interesting findings from the collaboration graph

---

## Deliverables
Submit your program with necessary explanation. The report should include:
- Description of selected professors/dataset
- Network construction approach
- Graph measures and interpretation
- Visualizations and community analysis
- Key conclusions
