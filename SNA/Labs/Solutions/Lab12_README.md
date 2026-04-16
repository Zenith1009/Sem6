# Lab 12 – Graph Neural Networks (GNN)
**CS342 Social Network Analysis | U23CS014 – Naishadh Rana**

---

## Overview

This lab implements a **Graph Convolutional Network (GCN)** for **graph-level regression** using PyTorch Geometric. The task is to predict the **water solubility** of organic molecules from their molecular graph structure (the ESOL dataset from MoleculeNet).

| Component | Library |
|---|---|
| Graph Neural Network | **PyTorch Geometric** (`torch_geometric`) |
| Molecule handling & visualisation | **RDKit** (`rdkit`) |

---

## Cell-by-Cell Explanation

### Cell 1 – Environment Setup
Imports `torch`, then tries to import `torch_geometric` and `rdkit`. If either is missing, `pip install` is called automatically. This makes the notebook portable between Colab (where you often need to install these) and a local environment where they may already be present.

The assignment originally prescribes pinning PyTorch 1.6 and installing via Miniconda — that workflow is Colab-specific and outdated. The approach used here (`pip install torch-geometric rdkit`) works on modern Python (≥3.9) and current PyTorch (≥2.x).

---

### Cell 2 – Load and Explore the ESOL Dataset
`MoleculeNet(root=".", name="ESOL")` downloads and caches the ESOL dataset:

- **1 128 molecules**, each represented as a graph.
- **Nodes** = atoms; **Edges** = chemical bonds.
- **Node features** (9-dimensional) encode atom type, degree, formal charge, hybridisation, aromaticity, etc.
- **Target `y`** = measured log-solubility in water (continuous value → regression).

We print dataset-level statistics: number of graphs, feature dimension, and label count.

---

### Cell 3 – Inspect a Single Graph
Prints detailed properties of the *first* graph: SMILES string, node/edge counts, feature dimension, target value, and structural flags (isolated nodes, self-loops, directedness). This confirms the data is loaded correctly and gives intuition about graph sizes.

---

### Cell 4 – Visualise Molecules with RDKit
Converts the stored SMILES strings back into RDKit molecule objects via `Chem.MolFromSmiles()`, then renders the first 8 molecules in a 2×4 grid using `Draw.MolsToGridImage()`. The legend under each molecule shows the true solubility `y`. This step bridges the abstract "graph" representation back to the chemical structure a human can recognise.

---

### Cell 5 – Train / Test Split
`data.shuffle()` randomly permutes the dataset, then we take the first 80 % as training and the remaining 20 % as test. Both subsets are wrapped in `DataLoader` with `batch_size=64`. PyTorch Geometric's `DataLoader` automatically **batches multiple graphs** into a single disconnected super-graph by remapping node indices and maintaining a `batch` vector that maps each node back to its source graph.

---

### Cell 6 – Build the GCN Model
The `GCN` class extends `torch.nn.Module`:

| Layer | Purpose |
|---|---|
| `GCNConv(in, 64)` | First hop – each node aggregates its direct neighbours |
| `GCNConv(64, 64)` | Second hop – 2-neighbourhood |
| `GCNConv(64, 64)` | Third hop – 3-neighbourhood |
| `global_mean_pool` | Averages all node embeddings into one graph-level vector |
| `Dropout(0.5)` | Regularisation to reduce overfitting |
| `Linear(64, 1)` | Outputs a single scalar = predicted solubility |

**Key design choice:** this is a *graph-level* regression task, so `global_mean_pool` is essential — it collapses variable-sized node representations into a fixed-length graph embedding. Node- or edge-level tasks would omit this step.

Each `GCNConv` layer applies the rule from Kipf & Welling (2017):
$$h_v^{(\ell+1)} = \sigma\!\left(\sum_{u \in \mathcal{N}(v) \cup \{v\}} \frac{1}{\sqrt{\deg(u)\,\deg(v)}} \; W^{(\ell)} h_u^{(\ell)}\right)$$
where the symmetric normalisation automatically weights neighbour contributions.

---

### Cell 7 – Training Loop (1 500 Epochs)
- **Optimiser:** Adam with `lr=0.0007` (a moderate learning rate that balances convergence speed and stability on this small dataset).
- **Loss:** `MSELoss` (mean squared error), the standard choice for regression.
- Each epoch iterates over all mini-batches; the per-epoch loss is the size-weighted average.
- Loss is printed every 100 epochs for monitoring.

---

### Cell 8 – Training Loss Curve
Plots `losses` (recorded in Cell 7) against epoch number. A healthy curve should decrease steeply in the first ~200 epochs and then plateau. Persistent oscillation would suggest the learning rate is too high.

---

### Cell 9 – Test Evaluation
The `evaluate()` function:
1. Sets the model to `eval()` mode (disables dropout).
2. Runs a forward pass on every test batch inside a `torch.no_grad()` context (saves memory, prevents gradient tracking).
3. Collects predictions and targets, then computes **MSE**, **RMSE**, and **MAE**.

These three metrics together give a complete picture of predictive accuracy.

---

### Cell 10 – Predicted vs Actual Scatter Plot
A 45° reference line shows perfect prediction; points clustered around this line indicate a good model. The RMSE is annotated in the title for easy reference.

---

## Dependencies

```
torch
torch-geometric
rdkit
matplotlib
numpy
```

Install with:
```bash
pip install torch torch-geometric rdkit matplotlib numpy
```
