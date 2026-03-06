# Semester 6 - College Work

One place to jump to all Semester 6 materials quickly.

## ⚡ Quick Access
- [DC](DC/) | [Labs](DC/Labs/) | [PPTs](DC/PPTs/)
- [SNA](SNA/) | [Labs](SNA/Labs/) | [PPTs](SNA/PPTs/)
- [SS](SS/) | [Labs](SS/Labs/) | 
- [RaIA](RaIA/) | [Labs](RaIA/Labs/) | [PPTs](RaIA/PPTs/) | [NPTEL_PPTs](RaIA/NPTEL_PPTs/)
- [IIE](IIE/) | [pdfs](IIE/pdfs/) 

## Subjects

### DC - Distributed Computing

**Study Material**
- Topics/Notes: [PPTs](DC/PPTs/), [Labs](DC/Labs/)

**Labs**
- Lab 1: Introduction & Examples ([Lab1](DC/Labs/Lab1/))
- Lab 2: Echo Client-Server Implementation ([Lab2](DC/Labs/Lab2/))
- Lab 3: Broadcast Chat & P2P Chat ([Lab3](DC/Labs/Lab3/))
- Lab 4: RPC using C / ONC-RPC files ([Lab4](DC/Labs/Lab4/))
- Lab 5: Docker Compose Client/Server ([Lab5](DC/Labs/Lab5/))
- Lab 6: Docker Compose Advanced Setup ([Lab6](DC/Labs/Lab6/))

<details>
<summary><strong>Syllabus Tracker</strong></summary>

- [x] Introduction to Distributed Systems (06 Hours)
  - Review of Networking Protocols
  - Point-to-Point Communication
  - Operating Systems
  - Concurrent Programming
  - Characteristics and Properties of Distributed Systems
  - Goals of Distributed Systems
  - Multiprocessor and Multicomputer Systems
  - Distributed Operating Systems
  - Network Operating Systems
  - Middleware Concept
  - The Client–Server Model
  - Design Approaches
    - Kernel-Based
    - Virtual Machine-Based
  - Application Layering

- [ ] Communication in Distributed Systems (04 Hours)
  - Layered Protocols
  - Message Passing
  - Remote Procedure Calls (RPC)
  - Remote Object Invocation
  - Message-Oriented Communication
  - Stream-Oriented Communication
  - Case Studies

- [ ] Process Management (05 Hours)
  - Concept of Threads and Processes
  - Processor Allocation
  - Process Migration and Related Issues
  - Software Agents
  - Scheduling in Distributed Systems
  - Load Balancing and Sharing Approaches
  - Fault Tolerance
  - Real-Time Distributed Systems

- [ ] Synchronization (06 Hours)
  - Clock Synchronization
  - Logical Clocks
  - Global State
  - Election Algorithms
    - Bully Algorithm
    - Ring Algorithm
  - Mutual Exclusion
    - Centralized Algorithm
    - Distributed Algorithm
    - Token Ring Algorithm
  - Distributed Transactions

- [ ] Consistency and Replication (06 Hours)
  - Introduction to Replication
  - Object Replication
  - Replication as a Scaling Technique
  - Data-Centric Consistency Models
    - Strict Consistency
    - Linearizability
    - Sequential Consistency
    - Causal Consistency
    - FIFO Consistency
    - Weak Consistency
    - Release Consistency
    - Entry Consistency
  - Client-Centric Consistency Models
    - Eventual Consistency
    - Monotonic Reads
    - Monotonic Writes
    - Read-Your-Writes
    - Writes-Follow-Reads
  - Implementation Issues
    - Distribution Protocols
    - Replica Placement
    - Update Propagation
    - Epidemic Protocols
    - Consistency Protocols

- [ ] Fault Tolerance (04 Hours)
  - Introduction
  - Failure Models
  - Failure Masking
  - Process Resilience
  - Agreement in Faulty Systems
  - Reliable Client–Server Communication
  - Group Communication
  - Distributed Commit
  - Recovery

- [ ] Distributed Object-Based Systems (06 Hours)
  - Introduction to Distributed Objects
  - Compile-Time vs Run-Time Objects
  - Persistent and Transient Objects
  - Enterprise Java Beans (EJB)
  - Stateful and Stateless Sessions
  - Global Distributed Shared Objects
  - Object Servers
  - Object Adaptors
  - Implementation of Object References
  - Static and Dynamic Remote Method Invocations
  - Replica Framework

- [ ] Distributed File Systems (04 Hours)
  - Introduction
  - Architecture
  - Mechanisms
    - Mounting
    - Caching
    - Hints
    - Bulk Data Transfer
    - Encryption
  - Design Issues
    - Naming and Name Resolution
    - Caches on Disk or Main Memory
    - Writing Policy
    - Cache Consistency
    - Availability
    - Scalability
    - Semantics
  - Case Studies
  - Log Structured File Systems

- [ ] Distributed Web-Based Systems (04 Hours)
  - Architecture
  - Processes
  - Communication
  - Naming
  - Synchronization
  - Web Proxy Caching
  - Replication of Web Hosting Systems
  - Replication of Web Applications

</details>

### SNA - Social Network Analysis

**Study Material**
- Topics/Notes: [PPTs](SNA/PPTs/), [Lab_Questions](SNA/Labs/Questions/), [Lab_Solutions](SNA/Labs/Solutions/)

**Labs**
- Lab 1: Basic Concepts and Exploration of NetworkX in Python ([Lab1.md](SNA/Labs/Questions/Lab1.md), [Lab1](SNA/Labs/Solutions/CS014_Naishadh_L1.ipynb))
- Lab 2: Network Measures (Degree, Clustering, Diameter, Density) ([Lab2.md](SNA/Labs/Questions/Lab2.md), [Lab2](SNA/Labs/Solutions/CS014_Naishadh_Lab2.ipynb))
- Lab 3: Centrality Analysis (Closeness & Betweenness) ([Lab3.md](SNA/Labs/Questions/Lab3.md), [Lab3](SNA/Labs/Solutions/U23CS014_Naishadh_Lab3.ipynb))
- Lab 4: Ego Facebook Network Dataset Analysis (SNAP) ([Lab4.md](SNA/Labs/Questions/Lab4.md), [Lab4](SNA/Labs/Solutions/U23CS014_Naishadh_Lab4.ipynb))
- Lab 5: Eigenvector Centrality and PageRank ([Lab5.md](SNA/Labs/Questions/Lab5.md), [Lab5](SNA/Labs/Solutions/U23CS014_Naishadh_Lab5.ipynb))
- Lab 6: Updated PageRank Algorithm (Teleportation) ([Lab6.md](SNA/Labs/Questions/Lab6.md), [Lab6](SNA/Labs/Solutions/U23CS014_Naishadh_Lab6.ipynb))
- Lab 7: HITS (Hyperlink-Induced Topic Search) Algorithm ([Lab7.md](SNA/Labs/Questions/Lab7.md), [Lab7](SNA/Labs/Solutions/U23CS014_Naishadh_Lab7.ipynb))
- Lab 8: Citation Network Creation and Analysis ([Lab8.md](SNA/Labs/Questions/Lab8.md), [Lab8](SNA/Labs/Solutions/U23CS014_Naishadh_Lab8.ipynb))

<details>
<summary><strong>Syllabus Tracker</strong></summary>

- [ ] Introduction to Social Networks and Applications (03 Hours)
  - Social Networks – Types, Structure and Representation
  - Different Types of Graphs
  - Levels of Analysis
    - Microscopic
    - Mesoscopic
    - Macroscopic
  - Dyadic Level
  - Triadic Level
  - Introduction to Graph Visualization Tools

- [ ] Network Measures (08 Hours)
  - Degree Distribution
  - Clustering Coefficient
  - Centrality Measures
    - Degree
    - Closeness
    - Betweenness
    - Eigenvector Centrality
  - Path and Diameter
  - Edge Density
  - Reciprocity and Assortativity
  - Connected Components
  - Giant Components
  - Group Centralities

- [ ] Network Growth Models (07 Hours)
  - Need for Synthetic Network Models
  - Real Network Properties
    - Small World
    - Scale-Free
    - High Average Clustering Coefficient
  - Erdős–Rényi Random Model
  - Watts–Strogatz Model
  - Barabási–Albert Preferential Attachment Model

- [ ] Link Prediction in Social Networks (07 Hours)
  - Signed Network and Link Analysis
  - Balance Theory
  - Status Theory
  - Strong and Weak Ties
  - Strength of Weak Ties
  - Local Bridges
  - Neighbourhood Overlap
  - Triadic Closure
  - Embeddedness
  - PageRank and Random Surfer Model
  - Similarity Rank
  - Path-Based Similarity of Nodes

- [ ] Community Detection in Social Networks (06 Hours)
  - Homophily
  - Emergence of Community in Social Networks
  - Link Partition
  - Algorithms for Community Detection

- [ ] Information Diffusion and Cascade Behaviour in Social Networks (05 Hours)
  - Information Diffusion in Social Networks
  - Cascade Models
  - Probabilistic Cascades
  - Epidemic Models
  - Cascade Prediction

- [ ] Graph Representational Learning (06 Hours)
  - Machine Learning Pipeline
  - Objectives and Benefits of Representational Learning
  - Methods for Graph Representational Learning

</details>

### SS - System Software

**Study Material**
- Topics/Notes: [SS/PDFs](SS/PDFs/)

**Labs**
- Lab 1: Regex to DFA, Lexical Analyzer, String Recognizer ([Lab1](SS/Labs/Lab1/))
- Lab 2: Arithmetic Expression, Comment Identifier, Assembler ([Lab2](SS/Labs/Lab2/))
- Lab 3: Recursive Descent Parser ([Lab3](SS/Labs/Lab3/))
- Lab 4: Grammar Programs ([Lab4](SS/Labs/Lab4/))
- Lab 5: LL(1) Parser ([Lab5](SS/Labs/Lab5/))
- Lab 6: RDP Lab ([Lab6](SS/Labs/Lab6/))

<details>
<summary><strong>Syllabus Tracker</strong></summary>

- [ ] Introduction (05 Hours)
  - Introduction to System Software
  - Utility Software
  - Systems Programming
  - Recent Trends in Software Development
  - Programming Languages and Language Processors
  - Data Structures for Language Processing

- [ ] Assemblers (06 Hours)
  - Overview of the Assembly Process
  - Cross Assembler
  - Micro Assembler
  - Meta Assembler
  - Single Pass Assembler
  - Two Pass Assembler
  - Design of Operation Code Table
  - Symbol Table
  - Literal Table
  - Advanced Assembly Process

- [ ] Macro Processors (06 Hours)
  - Introduction of Macros
  - Macro Processor Design
  - Forward Reference
  - Backward Reference
  - Positional Parameters
  - Keyword Parameters
  - Conditional Assembly
  - Macro Calls within Macros
  - Implementation of Macros Within Assembler
  - Designing Macro Name Table
  - Macro Definition Table
  - Keyword Parameter Table
  - Actual Parameter Table
  - Expansion Time Variable Storage

- [ ] Compilers (16 Hours)
  - Phases of Compiler
  - Analysis–Synthesis Model of Compilation
  - Interface with Input, Parser and Symbol Table
  - Token, Lexeme, Patterns and Error Reporting in Lexical Analysis
  - Programming Language Grammars
  - Classification of Grammar
  - Ambiguity in Grammatical Specification
  - Top Down Parsing
  - Recursive Descent Parsing
  - Transformation on the Grammars
  - Predictive Parsing
  - Bottom Up Parsing
  - Operator Precedence Parsing
  - LR Parsers
  - Language Processor Development Tools – **LEX & YACC**
  - Semantic Gap
  - Binding and Binding Times
  - Memory Allocation
  - Compilation of Expression
  - Intermediate Representations
  - Basic Code Optimization

- [ ] Linkers and Loaders (06 Hours)
  - Design of a Linker
  - Program Relocation
  - Linking of Overlay Structured Programs
  - Dynamic Linking
  - General Loader Schemes
  - Absolute Loader
  - Relocating Loader
  - Dynamic Loader
  - Bootstrap Loader
  - Linking Loader
  - Other Loading Schemes
  - Linkers vs Loaders

- [ ] Interpreters & Debuggers (06 Hours)
  - Overview of Interpretation and Debugging Process
  - Types of Errors
  - Classification of Debuggers
  - Dynamic / Interactive Debugger
  - The Java Language Environment
  - Java Virtual Machine
  - Recent Developments

</details>

### RaIA - Robotics and Its Applications

**Study Material**
- Topics/Notes: [PPTs](RaIA/PPTs/), [NPTEL](RaIA/NPTEL_PPTs/)

**Labs**
- Lab 1: Robot Anatomy and Terminologies ([/Lab1](RaIA/Labs/Lab1/))
- Lab 2: Python and Workspace Analysis ([/Lab2](RaIA/Labs/Lab2/))
- Lab 3: Workspace Analysis for Different Coordinate Systems ([/Lab3](RaIA/Labs/Lab3/))
- Lab 4: Forward and Inverse Kinematics for Planar Robot Arm ([/Lab4](RaIA/Labs/Lab4/))
- Lab 5: Forward and Inverse Kinematics with Trajectory Generation ([/Lab5](RaIA/Labs/Lab5/))

<details>
<summary><strong>Syllabus Tracker</strong></summary>

- [ ] Introduction (05 Hours)
  - What is a robot?
  - History and evolution of robotics
  - Types of robots: Industrial, service, mobile, etc.
  - Basic components of a robot: Manipulators, actuators, sensors, control systems
  - Applications of robotics in various fields: Manufacturing, healthcare, exploration, etc.
  - Introduction to Robot Operating System (ROS).

- [ ] Robot Kinematics (08 Hours)
  - Coordinate frames and transformations
  - Forward kinematics: Denavit-Hartenberg (DH) parameters
  - Inverse kinematics: Analytical and numerical solutions
  - Jacobian matrix and singularities
  - Mobile robot kinematics: Differential drive, Ackermann steering.

- [ ] Robot Dynamics (07 Hours)
  - Lagrangian mechanics
  - Equations of motion for robots
  - Inertia matrices and dynamic models
  - Force and torque analysis
  - Robot simulation.

- [ ] Robot Control (08 Hours)
  - Control system fundamentals: Feedback control
  - PID control
  - Robot arm control: Joint space control, operational space control
  - Mobile robot control: Path following, trajectory tracking
  - Adaptive control and learning control (brief introduction)

- [ ] Robot Perception (07 Hours)
  - Introduction to computer vision: Image processing, feature extraction
  - 3D vision: Depth sensing, stereo vision
  - Object recognition and tracking
  - Sensor fusion

- [ ] Robot Planning (05 Hours)
  - Path planning: Search algorithms (A*, Dijkstra's), sampling-based methods (RRT)
  - Motion planning: Trajectory generation, obstacle avoidance
  - Task planning: Hierarchical planning, task decomposition

- [ ] AI in Robotics (05 Hours)
  - Introduction to machine learning for robotics
  - Reinforcement learning for robot control and navigation
  - Natural language processing for human-robot interaction
  - Ethical and societal implications of AI in robotics

</details>

### IIE - Innovation, Incubation and Entrepreneurship

**Study Material**
- Topics/Notes: [PDFs](IIE/pdfs/)

<details>
<summary><strong>Syllabus Tracker</strong></summary>

- [ ] Concepts of Entrepreneurship (08 Hours)
  - Scope of Entrepreneurship
  - Definitions of Entrepreneurship and Entrepreneur
  - Entrepreneurial Traits, Characteristics, and Skills
  - Entrepreneurial Development Models and Theories
  - Entrepreneurs vs Managers
  - Classification of Entrepreneurs
  - Major Types of Entrepreneurship
    - Techno Entrepreneurship
    - Women Entrepreneurship
    - Social Entrepreneurship
    - Intrapreneurship (Corporate Entrepreneurship)
    - Rural Entrepreneurship
    - Family Business
  - Problems for Small-Scale Enterprises and Industrial Sickness
  - Entrepreneurial Environment
    - Political
    - Legal
    - Technological
    - Natural
    - Economic
    - Socio-Cultural

- [ ] Functional Management Areas in Entrepreneurship (15 Hours)
  - Marketing Management
    - Basic Concepts of Marketing
    - Development of Marketing Strategy
    - Marketing Plan
  - Operations Management
    - Basic Concepts of Operations Management
    - Location Problem
    - Development of Operations Strategy and Plan
  - Personnel Management
    - Main Operative Functions of a Personnel Manager
    - Development of HR Strategy and Plan
  - Financial Management
    - Basics of Financial Management
    - Ratio Analysis
    - Investment Decisions
    - Capital Budgeting and Risk Analysis
    - Cash Flow Statement
    - Break-Even Analysis

- [ ] Project Planning (09 Hours)
  - Search for Business Idea
  - Product Innovations
  - New Product Development
    - Stages in Product Development
  - Sequential Stages of Project Formulation
  - Feasibility Analysis
    - Technical
    - Market
    - Economic
    - Financial
  - Project Report
  - Project Appraisal
  - Setting up an Industrial Unit
    - Procedures and Formalities
  - Business Plan Development

- [ ] Protection of Innovation Through IPR (02 Hours)
  - Introduction to Intellectual Property Rights (IPR)
  - Patents
  - Trademarks
  - Copyrights

- [ ] Innovation and Incubation (07 Hours)
  - Innovation and Entrepreneurship
  - Creativity
  - Green Technology Innovations
  - Grassroots Innovations
  - Issues and Challenges in Commercialization of Technology Innovations
  - Introduction to Technology Business Incubations
  - Process of Technology Business Incubation

- [ ] Sources of Information and Support for Entrepreneurship (04 Hours)
  - State-Level Institutions
  - Central-Level Institutions
  - Other Agencies

</details>

---
