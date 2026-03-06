# Assignment 6 | Updated PageRank Algorithm

## Dataset
1. Extended web graph of SVNIT (www.svnit.ac.in) - extend from previous lab
2. Karate Club graph dataset from NetworkX library

## Required Libraries
- NetworkX
- Matplotlib
- BeautifulSoup (or whichever you want to use for the given task)

## How to Extend the SVNIT Web Graph

In the previous lab, you fetched HTML from www.svnit.ac.in and extracted links. Now, repeat the same process for one-hop neighbors of www.svnit.ac.in to create an extended graph.

---

## Part I — Implement Updated PageRank Algorithm

1) Implement updated PageRank algorithm that avoids spider trap using teleportation matrix (damping factor = 0.85).
2) Apply it on the Karate Club graph dataset.
3) Apply it on the Extended Web graph of SVNIT.

---

## Part II — Analyze and Compare Results

Analyze both graphs:
- a. Which node has the highest PageRank?
- b. What is the lowest PageRank in the network?
- c. Any other interesting findings?
- d. Display the final PageRank vector.
- e. Compare results with the simple PageRank algorithm from Lab 5.

---

## Deliverables
Write a report summarizing your findings. The report should include:
- Description and visualization of the extended web graph.
- Results of the updated PageRank algorithm.
- Jupyter Notebook file containing the code with comments for readability.
- Visualization screenshots (if applicable).
