# CS342 - Social Network Analysis
## Assignment 12 – Graph Neural Networks
**Date:** 07-Apr-2026

**Computer Science and Engineering Department, SVNIT, Surat**
B. Tech. III, Semester-VI | Academic Year – 2025-26

---

## Objective
To understand the GNN by implementing on a simple graph dataset.

## Tools
- **PyTorch Geometric** → Build Graph Neural Network
- **RDKit** → Handle Molecule Data

---

## Setup

### Installing PyTorch Geometric and RDKit

```python
# Enforce pytorch version 1.6.0
import torch
if torch.__version__ != '1.6.0':
    !pip uninstall torch -y
    !pip uninstall torchvision -y
    !pip install torch==1.6.0
    !pip install torchvision==0.7.0

# Check pytorch version and make sure you use a GPU Kernel
!python -c "import torch; print(torch.__version__)"
!python -c "import torch; print(torch.version.cuda)"
!python --version
!nvidia-smi
```

> Make sure you clicked **"RESTART RUNTIME"** above (if torch version was different)!

### Install RDKit

```python
import sys, os, requests, subprocess, shutil
from logging import getLogger, StreamHandler, INFO

logger = getLogger(__name__)
logger.addHandler(StreamHandler())
logger.setLevel(INFO)

def install(
    chunk_size=4096,
    file_name="Miniconda3-latest-Linux-x86_64.sh",
    url_base="https://repo.continuum.io/miniconda/",
    conda_path=os.path.expanduser(os.path.join("~", "miniconda")),
    rdkit_version=None,
    add_python_path=True,
    force=False):
    """install rdkit from miniconda

    ```
    import rdkit_installer
    rdkit_installer.install()
    ```
    """
    python_path = os.path.join(
        conda_path, "lib",
        "python{0}.{1}".format(*sys.version_info),
        "site-packages",
    )
    if add_python_path and python_path not in sys.path:
        logger.info("add {} to PYTHONPATH".format(python_path))
        sys.path.append(python_path)
    if os.path.isdir(os.path.join(python_path, "rdkit")):
        logger.info("rdkit is already installed")
        if not force:
            return
        logger.info("force re-install")
    url = url_base + file_name
    python_version = "{0}.{1}.{2}".format(*sys.version_info)
    logger.info("python version: {}".format(python_version))
    if os.path.isdir(conda_path):
        logger.warning("remove current miniconda")
        shutil.rmtree(conda_path)
    elif os.path.isfile(conda_path):
        logger.warning("remove {}".format(conda_path))
        os.remove(conda_path)
    logger.info('fetching installer from {}'.format(url))
    res = requests.get(url, stream=True)
    res.raise_for_status()
    with open(file_name, 'wb') as f:
        for chunk in res.iter_content(chunk_size):
            f.write(chunk)
    logger.info('done')
    logger.info('installing miniconda to {}'.format(conda_path))
    subprocess.check_call(["bash", file_name, "-b", "-p", conda_path])
    logger.info('done')
    logger.info("installing rdkit")
    subprocess.check_call([
        os.path.join(conda_path, "bin", "conda"),
        "install", "--yes", "-c", "rdkit",
        "python==3.7.3",
        "rdkit" if rdkit_version is None else "rdkit=={}".format(rdkit_version)])
    logger.info("done")
    import rdkit
    logger.info("rdkit-{} installation finished!".format(rdkit.__version__))

if __name__ == "__main__":
    install()
```

### Install PyTorch Geometric Extensions

```python
import torch
pytorch_version = f"torch-{torch.__version__}.html"

!pip install --no-index torch-scatter  -f https://pytorch-geometric.com/whl/$pytorch_version
!pip install --no-index torch-sparse   -f https://pytorch-geometric.com/whl/$pytorch_version
!pip install --no-index torch-cluster  -f https://pytorch-geometric.com/whl/$pytorch_version
!pip install --no-index torch-spline-conv -f https://pytorch-geometric.com/whl/$pytorch_version
!pip install torch-geometric
```

---

## Dataset

We will use a dataset provided in the dataset collection of PyTorch Geometric. The dataset comes from the **MoleculeNet** collection.

### Machine Learning Task
> How are different molecules dissolving in water?

**ESOL** is a small dataset consisting of water solubility data for **1128 compounds**. The dataset has been used to train models that estimate solubility directly from chemical structures (as encoded in SMILES strings). Note that these structures don't include 3D coordinates, since solubility is a property of a molecule and not of its particular conformers.

### Loading the Dataset

```python
import rdkit
from torch_geometric.datasets import MoleculeNet

# Load the ESOL dataset
data = MoleculeNet(root=".", name="ESOL")
```

### Explore the Dataset
- What is the number of nodes?
- What is the number of node-features?
- What is the number of edges?

### Visualise SMILES Molecules as Graphs

```python
data[0]["smiles"]

from rdkit import Chem
from rdkit.Chem.Draw import IPythonConsole

molecule = Chem.MolFromSmiles(data[0]["smiles"])
molecule
```

---

## Implementation of the Graph Neural Network

Building a Graph Neural Network works the same way as building a Convolutional Neural Network — we simply add some layers.

The **GCNConv** expects:
- `in_channels` = Size of each input sample
- `out_channels` = Size of each output sample

### Requirements
- Apply **three convolutional layers**, which means learn the information about **3 neighbour hops**.
- After that, apply a **pooling layer** to combine the information of the individual nodes, as we want to perform **graph-level prediction**.

> Always keep in mind that different learning problems (node, edge or graph prediction) require different GNN architectures.
> - For **node-level** prediction you will often encounter masks.
> - For **graph-level** predictions you need to combine the node embeddings.

### Training
- Train the GNN for **1500 epochs**.
- **Plot the loss function.**

### Evaluation
- Perform **test set predictions**.

---

## Deliverables

1. One `.ipynb` notebook containing your code.
2. One PDF file with the explanation of problem statement, dataset and code.
3. The PDF file should include the **training loss curve**.
