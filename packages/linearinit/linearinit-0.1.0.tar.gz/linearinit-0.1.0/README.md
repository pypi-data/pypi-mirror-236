# linearinit

[![codecov](https://codecov.io/gh/nxdens/linearInit/branch/main/graph/badge.svg?token=linearInit_token_here)](https://codecov.io/gh/nxdens/linearInit)
[![CI](https://github.com/nxdens/linearInit/actions/workflows/main.yml/badge.svg)](https://github.com/nxdens/linearInit/actions/workflows/main.yml)

Creates an Fully connect network from nn.linear layers with a given activation. The layer is initialized based on the activation function chosen. 

## Install it from PyPI

```bash
pip install linearinit
```

## Usage

```py
from linearinit.base import FullyConnectedLayers
from linearinit.base import LinearWithInit

fcn = FullyConnectedLayers(layer_sizes=[1, 2, 3], activation=nn.LeakyReLU(), bias=True)
```
