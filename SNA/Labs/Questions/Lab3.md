## Assignment 3 - Network Measures

**Dataset: Karate club graph dataset will be utilized which is available in the network library.**

*Following tasks need to be performed:*

1. Create the following network:
   ``` mermaid
   graph LR
       1((1)) --- 3((3))
       1((1)) --- 2((2))
       2((2)) --- 3((3))
       2((2)) --- 5((5))
       3((3)) --- 5((5))
       3((3)) --- 4((4))
       4((4)) --- 5((5))
    ```
2. Calculate the closeness centrality of each node in the above network
3. Calculate the betweenness centrality of each node in the above network
4. Display the “Karate club” network
5. Calculate the closeness centrality of each node in the “Karate club” network
6. Calculate the betweenness centrality of each node in the “Karate club” network
7. Identify the most important node in the “Karate club” network according to closeness centrality and betweenness centrality

**Deliverable:**
A single Jupyter Notebook file containing the code for all 7 tasks. Each task (1–7) should be clearly labeled using code comments or Markdown cells.