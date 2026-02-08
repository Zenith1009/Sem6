# Assignment 5 | Eigenvector Centrality and PageRank Algo

## Dataset
1. You need to create your own dataset: Web graph of SVNIT (www.svnit.ac.in)
2. Karate Club graph dataset from NetworkX library

## Required Libraries
- NetworkX
- Matplotlib
- BeautifulSoup (or whichever you want to use for the given task)

## Part I — Create Web Graph of SVNIT's Website and Perform Network Analysis

1) Set up the Python environment and install the necessary libraries.
2) Write a Python script to fetch the HTML content of the www.svnit.ac.in website and extract the links.
3) Use BeautifulSoup to parse the HTML and extract the hyperlinks.
4) Visualize the graph using NetworkX and Matplotlib.
5) Analyze and display the following network parameters using the NetworkX library:
	- Number of Nodes
	- Number of Edges
	- Indegree and Outdegree distribution chart
	- Average indegree and outdegree
6) Calculate the Eigenvector centrality of each node and display in a proper format.

---

## Part II — Implement PageRank Algorithm

1) Implement a simple PageRank algorithm.
2) Apply it on the "Karate Club graph dataset".
3) Analyze the graph:
	- a. Which node has the highest PageRank?
	- b. What is the lowest PageRank in the network?
	- c. Any other interesting findings?
	- d. Does this network have a self-loop?
	- e. Display the final PageRank vector.

---

## Deliverables
Write a report summarizing your findings. The report should include:
- Description of the web graph.
- Results of the PageRank algorithm.
- Jupyter Notebook file containing the code; write comments in the code wherever appropriate to make your code more readable and understandable.
- Visualization screenshots (if applicable).
