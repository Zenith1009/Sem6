Study Guide: Fundamentals of Distributed Systems (Lecture 1)

1. Evolution and Definition of Distributed Systems

Context and Strategic Importance

The landscape of computing underwent a seismic shift in the mid-1980s. Before this era, computers were room-sized, expensive mainframes functioning as standalone islands of logic. The advent of powerful microprocessors—evolving from 8-bit to 64-bit and multicore designs—and high-speed networking (LANs and the Internet) changed the fundamental "unit" of computing. This evolution moved us from a single-machine paradigm to a networked architecture, which is the foundation for all modern internet-scale computing.

The Standalone vs. Distributed Era

Between 1945 and 1985, computers were centralized assets. Modern machines now rival those mainframes at a fraction of the cost, often taking the form of smartphones or "plug computers." The primary catalysts for the distributed era were:

* Multicore CPUs: Providing massive local processing power at the edge.
* High-Speed Networks: Providing the "glue" that allows geographically dispersed nodes to communicate via Ethernet, fiber, or wireless (Wi-Fi/Cellular).

The Formal Definition

A Distributed System is a collection of autonomous computing elements that appears to its users as a single coherent system.

Technical Deep Dive: Autonomous Nodes

To be truly distributed, a system must manage three competing characteristics:

1. Independence: Each node has its own processor, local memory, and operating system. There is no shared physical memory.
2. Message Passing: Because nodes are independent, they communicate exclusively through explicit message exchange.
3. The "No Global Clock" Problem: Without a shared clock, time synchronization is difficult. The architectural consequence is that events cannot be totally ordered easily—a frequent focal point in distributed theory exams.

Management Tasks: Autonomous nodes require the system to manage Group Membership (tracking who is in the system), Admission Control (defining open vs. closed systems), and Authentication/Trust among nodes.

Exam Alert: Overlay Networks

Distributed systems utilize Overlay Networks, which are logical communication structures built on top of physical networks.

Feature	Structured Overlays	Unstructured Overlays
Organization	Strictly organized (Trees, Rings, Distributed Hash Tables (DHTs)).	Random or ad-hoc neighbor connections.
Logic	Predetermined paths for data retrieval.	Dynamic and flexible; common in P2P.
Example	Chord (DHT), File trees.	Gnutella, early BitTorrent.

Common Mistake: Students often confuse "distributed" with "parallel/multiprocessor." In a multiprocessor system, CPUs share physical memory. In a distributed (multicomputer) system, the lack of shared physical memory is the key differentiator.


--------------------------------------------------------------------------------


2. Design Goals: Resource Access and Distribution Transparency

Context and Strategic Importance

A distributed system's value is derived from its ability to make distance and complexity invisible to the user. If the "gears" of the network are visible, the system has failed its primary design goal.

Resource Access

The motivation for sharing resources is both economic and collaborative:

* Economic: Sharing expensive high-end peripherals or storage is cheaper than replication.
* Collaborative: P2P systems and global shared folders (e.g., cloud storage) allow dispersed teams to work on synchronized data.

The Transparency Matrix

Distribution transparency aims to hide where processes and resources (objects) are located.


| Type | Precise Exam Definition | Real-World Example |
|------|------------------------|-------------------|
| Access | Hide differences in data representation and access methods. | Uniform file interfaces across different OSs. |
| Location | Hide where an object is physically located. | URLs (masking the server's IP). |
| Relocation | Hide that an object moved while in use. | Seamless handover in mobile networks. |
| Migration | Hide that an object can move by user request (not necessarily during use). | Moving a VM to another server for maintenance. |
| Replication | Hide that multiple copies of data exist. | CDNs serving files from the nearest edge server. |
| Concurrency | Hide that resources are shared by several users. | Multiple users editing one database simultaneously. |
| Failure | Hide the failure and recovery of an object. | Automatic failover to a backup server. |


Mnemonic Technique: To remember the 7 types, use: **A** **L**ittle **R**at **M**ight **R**uin **C**at **F**ood (Access, Location, Relocation, Migration, Replication, Concurrency, Failure).

Critique of Full Transparency

Architectural Consequence: Full transparency is often counterproductive due to the speed-of-light limitation and network latency.

* RPC vs. Messaging: Remote Procedure Calls (RPC) attempt to make network calls look like local calls. However, message-based communication is often preferred because it makes delays and failures explicit, which is easier to handle in complex logic.
* Copy-before-use: Instead of full transparency, systems often use this principle where data is copied locally for use, and updates create new versions.

Diagram Instruction: The Middleware Layer Visualize a horizontal box labeled "Distributed-system layer (middleware)" sitting between the "Applications" (top) and multiple "Local Operating Systems" (bottom). This middleware masks the heterogeneity of the underlying hardware and OSs, providing a uniform interface.


--------------------------------------------------------------------------------


3. Openness and the "Policy vs. Mechanism" Principle

Context and Strategic Importance

Standardization allows heterogeneous systems from different developers to function as a unified whole.

Standards and Interfaces

* Syntax: How a service is accessed (message formats, names).
* Semantics: What the service actually does.
* IDLs (Interface Definition Languages): Used to specify syntax precisely to ensure Interoperability (working together) and Portability (running on different systems).
* Standards Criteria: Open standards must be Complete (all info needed to implement is present) and Neutral (they do not favor a specific vendor).

Evolutionary Insight: SOAP vs. REST

* SOAP: Decouples syntax and semantics. Every service has an explicit interface described by WSDL (Web Services Description Language).
* REST: Combines syntax and semantics through a small, fixed set of standard HTTP methods (GET, POST, etc.) that apply to all resources. This uniform interface leads to simpler, more interoperable systems.

Strategic Design: Separating Policy from Mechanism

This is a High-Weightage Topic for long-answer questions.

* Mechanism (The Tool): The technical capability (e.g., a "Smart Door Lock" hardware that can retract a bolt).
* Policy (The Rule): The logic deciding when to use the tool (e.g., "Lock the door at 10 PM").

Architectural Consequence: This leads to "pluggable" systems where policies (like a Web Cache using LRU vs. FIFO) can be swapped without rewriting the mechanism code.

* Trade-off: Total separation causes "Configuration Fatigue." The solution is providing Sensible Defaults for 90% of users while allowing experts to customize.


--------------------------------------------------------------------------------


4. Dimensions and Techniques of Scalability

Context and Strategic Importance

Scalability is the ultimate survival metric. Modern systems must grow without redesign or performance collapse.

The Three Dimensions

1. Size: Handling more users/resources.
2. Geographical: Operating efficiently across large distances.
3. Administrative: Spanning multiple organizations/domains.

Scalability Bottlenecks

Centralized services create bottlenecks in CPU, I/O, or bandwidth. Queuing Theory dictates that as load increases, response time degradation is exponential.

Latency Hiding Techniques

1. Asynchronous Communication: Using message queues so the client doesn't block.
2. Overlapping Computation/Communication: Downloading one file chunk while processing another.
3. Edge Processing: Moving computation (e.g., form validation) closer to the user to reduce round-trips.

Scaling through Partitioning: DNS Case Study

The Domain Name System (DNS) partitions its namespace into hierarchical zones:

* Root Name Servers: The top level; they redirect queries to TLD servers.
* TLD Servers: Manage extensions like .com and .org; they point to authoritative servers.
* Authoritative Servers: Store the actual records; they return the final IP.
* Recursive Resolvers: Act for the client, querying the hierarchy and caching responses.

Diagram Instruction: DNS Hierarchy Illustrate a tree structure: "Root" at the top, branching to "TLD Servers" (.com, .edu), then to "Authoritative Servers" (amazon.com, nyu.edu). Show the Recursive Resolver as an intermediary between the client and this hierarchy.


--------------------------------------------------------------------------------


5. Classification: Computing, Information, and Pervasive Systems

Distributed Computing Systems

* Cluster Computing: Uses commodity PCs and high-speed LANs to create a Single-System Image (SSI).
  * MOSIX: A Linux-based management system that provides automatic and transparent process migration to balance workloads across nodes.
* Grid Computing: A federation of heterogeneous "Virtual Organizations."
  1. Fabric Layer: Direct access to local resources (CPU, storage).
  2. Connectivity Layer: Security and authentication protocols.
  3. Resource Layer: Allocation and monitoring of individual resources.
  4. Collective Layer: Coordination, directory services, and load balancing.
* Cloud Computing: A "Utility" model (IaaS, PaaS, SaaS) with four layers: Hardware, Infrastructure, Platform, and Application.

The "Abandoned" Technology: Distributed Shared Memory (DSM) was an attempt to provide the illusion of shared memory on multicomputers. It was abandoned due to high communication latency, frequent page faults ("false sharing"), and poor scalability.

Distributed Information Systems

Focused on data integrity across enterprises using Enterprise Application Integration (EAI).

* ACID Properties (High Weightage): Atomicity (all-or-nothing), Consistency (valid state to valid state), Isolation (no interference), Durability (changes persist).
* EAI Approaches:
  1. File Transfer: Simple, but requires agreement on formats and naming.
  2. Shared Database: Easy data sharing, but risks schema complexity and performance bottlenecks.
  3. RPC/Messaging: Facilitated by TP Monitors to coordinate transactions.

Pervasive Systems

Embedded in the physical environment.

* Ubiquitous Computing Requirements: Unobtrusive Interaction (implicit input), Context Awareness (adapting to location/time), Autonomy (self-management), and Intelligence.
* Sensor Networks: Energy efficiency is the critical constraint. They use In-Network Data Processing (aggregating data within the network) to reduce transmission costs.


--------------------------------------------------------------------------------


6. Comprehensive Glossary and Exam Summary

Glossary

* Autonomous: Nodes that operate independently with their own OS and memory.
* Middleware: Software layer masking heterogeneity and providing a uniform interface.
* ACID: Requirements for reliable transactions (Atomicity, Consistency, Isolation, Durability).
* IDL (Interface Definition Language): Describes a service's syntax for interoperability.
* Interoperability: Ability of different implementations to work together.
* Portability: Ability of an application to run on different systems without modification.
* Virtual Organization: A group of organizations sharing resources in a Grid Computing environment.

Final Exam Checklist

1. The 7 Transparency Types: Distinguish between Relocation (active) and Migration (on request).
2. Policy vs. Mechanism: Explain how this separation creates "pluggable" systems.
3. Scalability Techniques: Define Latency Hiding, Partitioning, and Replication.
4. DNS Hierarchy: Identify the roles of Root, TLD, and Authoritative servers.
5. Grid Layers: Memorize the Fabric, Connectivity, Resource, and Collective layers.

Common Mistakes Summary

* Assuming Shared Memory: Distributed nodes communicate only via message passing.
* Transparency Over-Optimization: Full transparency can crush performance due to latency.
* Interoperability vs. Portability: Interoperability is about working together; Portability is about moving code between systems.
* Ignoring Administrative Scalability: This is often the hardest dimension as it involves conflicting organizational policies and trust.


---

***

### Broad Classification (2–5 Marks)
Examiners often ask for a quick categorization before diving deep. Always start your answers with this three-tier classification to show structural clarity:

1. **Distributed Computing Systems**: Focus on sharing computational power for massive, compute-intensive tasks (e.g., Clusters, Grids, Clouds).
2. **Distributed Information Systems**: Focus on data sharing, interoperability, and transactions across autonomous sources (e.g., Enterprise Application Integration).
3. **Pervasive Systems**: Focus on seamless integration of computation into the physical environment via sensors and mobile devices.

---

### TOPIC 1: Distributed Computing Systems (High-Weightage: 10–15 Marks)

This is a guaranteed long-answer question. You will likely be asked to differentiate between Cluster, Grid, and Cloud computing, or explain their architectures.

#### 1. Parallel Processing Models (Foundation for 5 Marks)
Before explaining clusters, clearly define the base hardware models.

-   **Multiprocessor Systems**: Multiple CPUs sharing a single physical memory.
-   **Multicomputer Systems**: Independent computers, each with private memory, communicating over a network.
-   *Note on Distributed Shared Memory (DSM)*: It was an attempt to create a global virtual address space over multicomputers but failed due to high communication latency and false sharing.
-   **Diagram Strategy**: Draw two side-by-side blocks. For multiprocessors, draw Processors (P) connecting to a shared Interconnect, which connects to shared Memory (M) blocks. For multicomputers, bind one P and one M together, then connect these combined units to the Interconnect.

#### 2. Cluster Computing
*   **Definition**: A combination of multiple independent computers built using commodity PCs and high-speed LANs, designed for parallel execution of compute-intensive programs.
*   **Key Concept - Single-System Image (SSI)**: The ultimate goal of a cluster is to make the entire system appear as a single machine to the user. It offers transparent process execution and a unified file system. 
*   **Beowulf Architecture**: The most famous Linux-based cluster design.
    *   *Master Node*: Handles job submission, scheduling, resource allocation, and user access.
    *   *Compute Nodes*: Execute the actual parallel application components.
*   **MOSIX System**: A Linux cluster management system providing SSI through automatic, transparent process migration and dynamic load balancing to less-loaded nodes.
*   **Diagram Strategy**: Draw a Beowulf cluster block diagram. Leftmost block is the "Master node" (Management app, Parallel libs, Local OS). Connect it via a high-speed network to multiple "Compute nodes" (Parallel app component, Local OS).
*   **Real-World Example**: University supercomputing labs built from standard lab computers networked together.

#### 3. Grid Computing
*   **Definition**: A federation of heterogeneous computing systems spanning multiple administrative domains with no assumptions about hardware, OS, or networks.
*   **Key Concept - Virtual Organizations (VOs)**: Resources are shared across physical organizations to form a VO, where access rights are defined per organization.
*   **Layered Architecture (Crucial for Exams - 5 Marks)**:
    1.  **Fabric Layer**: Direct access to local resources (CPUs, storage).
    2.  **Connectivity Layer**: Handles communication and security (authentication).
    3.  **Resource Layer**: Manages individual resources (allocation, control).
    4.  **Collective Layer**: Coordinates multiple resources (scheduling, directory services).
    5.  **Application Layer**: User applications utilising the grid.
*   **Diagram Strategy**: Draw a top-down flowchart: Applications $\rightarrow$ Collective layer $\rightarrow$ (splits into) Connectivity & Resource layers $\rightarrow$ Fabric layer.
*   **Mnemonic for Grid Layers**: **A**ll **C**ats **R**un **C**atching **F**ish $\rightarrow$ **A**pplication, **C**ollective, **R**esource, **C**onnectivity, **F**abric.

#### 4. Cloud Computing
*   **Definition**: An evolution of utility computing providing a virtualized resource pool that is allocated dynamically on a pay-per-use model, governed by SLAs.
*   **Cloud Architecture Layers**:
    *   *Hardware Layer*: Physical data centres.
    *   *Infrastructure Layer*: Virtual machines, storage pools.
    *   *Platform Layer*: Development frameworks, middleware.
    *   *Application Layer*: End-user on-demand services.
*   **Cloud Service Models (Guaranteed Short Note)**:
    *   **IaaS (Infrastructure as a Service)**: Provides virtualized computing resources (e.g., AWS EC2).
    *   **PaaS (Platform as a Service)**: Provides development environments (e.g., Google App Engine).
    *   **SaaS (Software as a Service)**: Delivers complete web applications (e.g., Gmail, Google Docs).
*   **Mnemonic for Cloud Models**: **SPI** (SaaS, PaaS, IaaS). 

> **⚠️ Common Exam Mistake**: Students often confuse Grid and Cluster computing. **Remember the keyword distinction**: Clusters are *homogeneous* commodity PCs in a *single* administrative domain. Grids are *heterogeneous* systems spanning *multiple* administrative domains (Virtual Organizations).

---

### TOPIC 2: Distributed Information Systems (Medium-Weightage: 5–10 Marks)

This topic is highly scoring if you use the correct middleware terminology.

#### 1. Distributed Transactions
*   **Definition**: Database operations executed as an all-or-nothing execution, controlled using transaction primitives (BEGIN, END, ABORT, READ, WRITE).
*   **ACID Properties (Must Write in Exams)**:
    *   **A - Atomicity**: Executed entirely or not at all.
    *   **C - Consistency**: Transforms system from one valid state to another.
    *   **I - Isolation**: Concurrent transactions execute without interference.
    *   **D - Durability**: Committed effects persist despite crashes.
*   **Nested Transactions**: A top-level transaction composed of parallel subtransactions. The key rule: *Only the top-level commit is permanent*.
*   **Transaction Processing (TP) Monitor**: Middleware that coordinates distributed transactions and implements distributed commit protocols. 
*   **Diagram Strategy**: For a TP Monitor, draw a "Client application" sending a transaction request to a central "TP Monitor" block. The TP Monitor then sends sub-requests to multiple "Server" blocks connected to their respective databases.

#### 2. Enterprise Application Integration (EAI)
*   **Concept**: Integrating independent enterprise applications using middleware to facilitate direct communication.
*   **4 EAI Approaches (High Probability for 10 Marks)**:
    1.  **File Transfer**: Apps exchange shared files. *Limitation*: Requires agreement on naming and formats.
    2.  **Shared Database**: All apps access a common database schema. *Limitation*: Performance bottlenecks.
    3.  **Remote Procedure Call (RPC)**: Apps invoke operations of other apps directly. *Limitation*: Both parties must be active simultaneously.
    4.  **Messaging**: Apps exchange messages asynchronously via middleware. Allows system decoupling.
*   **Mnemonic for EAI Approaches**: **F**ast **S**ystems **R**equire **M**essaging (File, Shared DB, RPC, Messaging).
*   **Real-World Example**: A bank using a TP monitor to ensure that an ATM withdrawal (subtransaction 1) and account deduction (subtransaction 2) happen atomically.

> **⚠️ Common Exam Mistake**: Do not just list the EAI approaches. To get full marks, you *must* mention the limitation/trade-off of each approach, as evaluators look for critical analysis.

---

### TOPIC 3: Pervasive Systems (Short Notes: 5 Marks)

This is a theoretical section. Focus on precise definitions and characteristics.

#### 1. Core Concept

Pervasive systems blur the separation between users and system components. Computation is seamlessly embedded into the environment, interacting via sensors and actuators.

#### 2. Three Types of Pervasive Systems

*   **Ubiquitous Computing**: Invisible computing integrated into everyday activities.
*   **Mobile Computing**: Systems supporting mobility via wireless disruption-tolerant networking.
*   **Sensor Networks**: Large collections of battery-powered, resource-constrained nodes used for environmental monitoring.

#### 3. Core Requirements of Ubiquitous Systems (Learn these 5 keywords):
1.  **Distribution**: Networked devices cooperating transparently.
2.  **Unobtrusive Interaction**: Minimal explicit user input.
3.  **Context Awareness**: Adapting to identity, location, time.
4.  **Autonomy**: Self-configuration and self-management without human help.
5.  **Intelligence**: AI techniques to handle dynamic/incomplete inputs.
*   **Mnemonic**: **DUC AI** (Distribution, Unobtrusive, Context, Autonomy, Intelligence).

#### 4. Sensor Network Execution Strategy

Instead of sending all raw data to a central operator (which drains battery), sensor networks use **In-Network Data Processing**. Nodes aggregate and process data locally, only sending the final answers/queries to the operator to save energy.

-   **Diagram Strategy**: Draw two clouds of sensors. In "Bad Design", draw arrows from all sensors to the operator. In "Good Design (In-Network)", draw cylinders inside the cloud representing local processing, and only one arrow pointing out to the operator labelled "Answers".

---

### COMPREHENSIVE GLOSSARY OF KEY TERMS (Exam Quick-Revision)

*   **ACID**: Atomicity, Consistency, Isolation, and Durability; the four mandatory properties of a reliable distributed transaction.
*   **Beowulf Cluster**: A popular, commodity hardware-based cluster architecture featuring a master management node and multiple compute nodes.
*   **Disruption-Tolerant Networking**: Networking architecture used in mobile computing that can withstand changing locations and intermittent connectivity.
*   **Grid Computing**: A distributed system that acts as a federation of heterogeneous resources spanning multiple administrative domains via Virtual Organizations.
*   **IaaS / PaaS / SaaS**: Infrastructure, Platform, and Software as a Service. The three primary service models of Cloud Computing.
*   **In-Network Data Processing**: An energy-saving technique in sensor networks where data is aggregated and processed locally by nodes rather than being sent to a central server.
*   **Middleware**: A software layer above operating systems that masks hardware/network heterogeneity and provides uniform interfaces for distributed applications.
*   **MOSIX**: A Linux-based cluster system providing a Single-System Image through transparent process migration and load balancing.
*   **Multicomputer**: A parallel processing model where independent computers with private memory communicate over a network.
*   **Single-System Image (SSI)**: The illusion provided by cluster middleware that makes multiple distinct machines appear and operate as one unified computer.
*   **TP Monitor (Transaction Processing Monitor)**: Middleware responsible for coordinating distributed subtransactions and implementing distributed commit protocols to ensure ACID properties.
*   **Virtual Organization (VO)**: A logical entity in Grid computing representing a coalition of geographically distributed individuals and institutions sharing resources under specific access rules.

Study these structures, memorize the mnemonics, practice the block diagrams, and you are guaranteed to score maximum marks in this module. Good luck!

---

## Exam Booster: Expected Questions + Memory System (SVNIT/Indian University Pattern)

> **Note:** Public web scraping for live question-paper portals may fail due anti-bot checks, so this section is based on recurring patterns across Indian university Distributed Systems papers and your Lecture-1 syllabus coverage.

### A. Most Expected Questions (Topic-Wise)

#### 2–3 Marks (Very Frequent)
1. Define a Distributed System. Why is there no global clock problem?
2. Differentiate multiprocessor vs multicomputer systems.
3. List any 4 types of distribution transparency.
4. What is middleware? Give any 2 services it provides.
5. Define interoperability vs portability.
6. What is a Virtual Organization in Grid computing?
7. What is Single-System Image (SSI) in clusters?
8. Expand ACID and define any one property.
9. What is in-network data processing in sensor networks?
10. Differentiate relocation transparency vs migration transparency.

#### 5 Marks (Highly Probable)
1. Explain all types of distribution transparency with examples.
2. Explain policy vs mechanism with one technical example.
3. Discuss three dimensions of scalability with bottlenecks.
4. Explain DNS partitioning and role of Root, TLD, Authoritative, Resolver.
5. Explain Beowulf cluster architecture and SSI.
6. Explain Grid layered architecture.
7. Explain cloud layers and service models (IaaS/PaaS/SaaS).
8. Explain EAI approaches and their trade-offs.

#### 10–15 Marks (Long Answers)
1. Compare Cluster vs Grid vs Cloud (architecture, administration, heterogeneity, use cases).
2. Discuss distribution transparency and why full transparency is impractical.
3. Explain distributed information systems: ACID, nested transactions, TP monitor, EAI methods.
4. Explain pervasive systems: ubiquitous/mobile/sensor systems + requirements + in-network processing.

### B. “Answer Frame” to Maximize Marks

Use this 5-step structure for any 5/10-mark answer:
1. **Definition (1–2 lines)**
2. **Core points in bullets** (3–7 bullets)
3. **One labeled diagram**
4. **One real-world example**
5. **One limitation/trade-off line**

If time permits, close with one-line conclusion: “Hence, ____ improves ____ but trades off ____.”

### C. High-Yield Mnemonics (Easy Recall)

1. **Transparency types:** **A L R M R C F**  
  “**A** Little **R**at **M**ight **R**uin **C**at **F**ood”

2. **Design goals:** **R T O S**  
  “**R**esources, **T**ransparency, **O**penness, **S**calability”

3. **Grid layers (top→down):** **A C R C F**  
  “**A**ll **C**ats **R**un **C**atching **F**ish”

4. **Cloud service models:** **S P I**  
  SaaS → PaaS → IaaS

5. **ACID:**  
  “**A**ll **C**onsistent **I**solated **D**ata”

6. **Scalability dimensions:** **S G A**  
  “**S**ize, **G**eography, **A**dministration”

7. **EAI approaches:** **F S R M**  
  File, Shared DB, RPC, Messaging

8. **Ubiquitous requirements:** **D U C A I**  
  Distribution, Unobtrusive, Context-aware, Autonomy, Intelligence

### D. Confusion Traps (Examiner Favorites)

1. **Relocation vs Migration:**
  - Relocation = moves while in use (system-driven, transparent).
  - Migration = moved on request.

2. **Cluster vs Grid:**
  - Cluster = mostly homogeneous, single admin domain.
  - Grid = heterogeneous, multi-domain VO model.

3. **Interoperability vs Portability:**
  - Interoperability = systems work together.
  - Portability = app runs unchanged elsewhere.

4. **Replication/Caching vs Consistency:**
  - More copies improve latency/availability.
  - Strong consistency can hurt scalability.

### E. Diagram-First Revision List (Guaranteed Return)

Practice these 8 diagrams once daily:
1. Middleware layer between apps and local OS
2. Multiprocessor vs multicomputer
3. Transparency types chart
4. DNS hierarchy partitioning
5. Beowulf cluster architecture
6. Grid layered architecture
7. Cloud 4-layer architecture
8. Sensor network: centralized vs in-network processing

### F. 3-Day Rapid Revision Plan

**Day 1:** Definitions + transparency + openness + policy/mechanism  
**Day 2:** Scalability + DNS + cluster/grid/cloud comparison  
**Day 3:** ACID/EAI + pervasive systems + full mock writing

For each day:  
- 45 min concept read  
- 45 min active recall (no notes)  
- 30 min diagram redraw  
- 30 min 5-mark answer writing

### G. Last-Night Strategy (Highest ROI)

1. Memorize 10 one-line definitions (DS, middleware, SSI, VO, ACID, TP monitor, etc.).
2. Practice 3 long answers fully written.
3. Redraw all key diagrams from memory.
4. Revise confusion pairs (Relocation/Migration, Cluster/Grid, Interoperability/Portability).
5. Keep one “cheat sheet” page of mnemonics and trade-offs only.