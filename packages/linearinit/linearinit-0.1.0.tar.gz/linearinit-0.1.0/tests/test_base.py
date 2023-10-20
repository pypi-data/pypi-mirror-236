from linearinit.base import NAME
from linearinit.base import FullyConnectedLayers
from linearinit.base import LinearWithInit
from torch import nn
import torch


def test_base():
    assert NAME == "linearinit"

    x = torch.rand(1)
    fcn = FullyConnectedLayers([1, 2, 3])
    fcn2 = FullyConnectedLayers([1, 2, 3], activation=nn.ReLU())
    fcn3 = FullyConnectedLayers([1, 2, 3], activation=nn.Tanh())
    fcn4 = FullyConnectedLayers([1, 2, 3], activation=nn.LeakyReLU(), bias=True)
    fcn(x)
    fcn2(x)
    fcn3(x)
    fcn4(x)
