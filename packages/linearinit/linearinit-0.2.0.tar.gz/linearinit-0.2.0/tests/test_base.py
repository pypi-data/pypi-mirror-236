from linearinit.base import NAME
from linearinit.base import FullyConnectedLayers
from linearinit.base import LinearWithInit
from torch import nn
import torch


def test_base():
    assert NAME == "linearinit"

    x = torch.rand(2, 1)
    fcn = FullyConnectedLayers([1, 2, 3])
    fcn2 = FullyConnectedLayers([1, 2, 3], activation=nn.ReLU(), batchnorm=True)
    fcn3 = FullyConnectedLayers([1, 2, 3], activation=nn.Tanh(), dropout_p=0.5)
    fcn4 = FullyConnectedLayers([1, 2, 3], activation=nn.LeakyReLU(), bias=True)
    fcn5 = FullyConnectedLayers([1, 2, 3], batchnorm=True, dropout_p=0.2, bias=True)
    fcn(x)
    fcn2(x)
    fcn3(x)
    fcn4(x)
    fcn5(x)
