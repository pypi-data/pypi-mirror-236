# PyMulSim

**PyMulSim** is a Python library for pairwise node similarity between multilayer networks. Embeddings are computed by using a model based on Graph Neural Network (GNN).

It was also released on PyPi: https://pypi.org/project/pymulsim

## Table of Contents

- [Installation](#installation)
- [Getting Started](#getting-started)
- [Usage](#usage)
  - [Computing Similarities from File](#computing-similarities-from-file-data)
  - [Computing Similarities from NetworkX Graphs](#computing-similarities-from-networkx-graphs)
- [Usage](#usage)

## Installation <a name="installation"></a>

To get started with **PyMulSim**, you have to install it via pip:

```
pip install pymulsim
```

## Getting Started <a name="getting-started"></a>

To begin using PyMulSim, follow these steps:

1. Import the **PyMulSim** class in your Python script:

```
from pymulsim import PyMulSim
```

2. Create an instance of the **PyMulSim** class:

```
pymulsim = PyMulSim()
```

3. Use the available methods for computing node similarities between two given multilayer networks.


## Usage <a name="usage"></a>

**PyMulSim** allows computing node similarities between two given multilayer networks by using both data from files and NetworkX objects.

You can choose the method that best suits your data and use case.

### Computing Similarities from File <a name="computing-similarities-from-file-data"></a>

To compute node similarities from data stored in files, prepare two sets of graph data files: one for the source multilayer network, and one for the target multilayer network.

Note that we made available a (toy) dataset (folder: 'dataset')and a related example code (file: 'example.py'), for demonstration purpose only.

```
node_similarities = pymulsim.compute_similarities_from_file( source_path:(str), target_path:(str), layer_ids:(list), interlayer_ids:(list) )
```

## Computing Similarities from NetworkX Graphs <a name="computing-similarities-from-networkx-graphs"></a>

Alternatively, you can compute node similarities by using two multilayer networks modelled as a set of NetworkX (nx) objects.

```
similarities = pymulsim.compute_similarities_from_nx( nx_set1:(list:nx.Graph), nx_set2(list:nx.Graph), layer_ids:(list), interlayer_ids:(list) )
```

### License

MIT License - Copyright (c) 2023 Pietro Cinaglia

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.