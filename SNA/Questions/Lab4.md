# Assignment 4 — Analysis of Ego Facebook Network Dataset

## Dataset
- Ego-Facebook dataset from the Stanford Large Network Dataset Collection (SNAP).

## Required libraries
- NetworkX
- snap-stanford
- Matplotlib

## Part I — Analysis of Facebook dataset using SNAP
1) Set up the Python environment with the required libraries.
2) Download `facebook_combined.txt.gz` from SNAP: https://snap.stanford.edu/data/ego-Facebook.html?form=MG0AV3
3) Load the dataset and create a NetworkX graph.
4) Analyze and display these network parameters with NetworkX:
	- Number of nodes
	- Number of edges
	- Degree distribution chart
	- Average degree
	- Global clustering coefficient
	- Local clustering coefficient (pick one example node, inspect its connections, and verify the local clustering coefficient with the formula)
	- Diameter
	- Density
	- Average path length

## Part II — Ego-centric analysis of Facebook dataset using SNAP
1) Download `facebook.tar.gz` from SNAP.
2) Load the Facebook dataset and create a graph object.
3) Identify the ego nodes (nodes around which ego networks are centered).
4) For each ego node, extract its ego network and analyze: clustering coefficient, number of triangles, average path length, and diameter.
5) Visualize ego networks using NetworkX and Matplotlib.

For both Part I and Part II, submit your Python code file with the tasks completed. Add comments where appropriate for readability.

## Deliverable
Write a report summarizing your findings, including:
- Description of the dataset and the analysis.
- Results of the ego-centric analysis for each ego node.
- Visualization screenshots (if applicable).
