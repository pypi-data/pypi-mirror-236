"""
linearinit base module.

This is the principal module of the linearinit project.
here you put your main classes and objects.

Be creative! do whatever you want!

If you want to replace this with a Flask application run:

    $ make init

and then choose `flask` as template.
"""

# example constant variable
NAME = "linearinit"
from torch import nn
from typing import Any, List


class FullyConnectedLayers(nn.Module):
    """Wrapper for nn.linear that creates a fully connected network with the given layer sizes. The
    layers are initiated with different algorithms depending on the non-linear activation.
    """

    def __init__(self, layer_sizes: List, activation=nn.GELU(), bias=False):
        """Creates a fully connected network with the given layer sizes. The layers are initiated with nn.GELU() by default.

        Args:
            layer_sizes (List): List of ints representing the layer sizes
            activation (nn.Module, optional): Non-linear activation function. Defaults to nn.GELU().
        """
        super().__init__()
        layers = []
        self.activation = activation
        self.bias = bias
        for i in range(len(layer_sizes) - 1):
            layers.append(
                LinearWithInit(
                    layer_sizes[i],
                    layer_sizes[i + 1],
                    activation=self.activation,
                    bias=self.bias,
                )
            )
        self.net = nn.Sequential(*layers)

    def forward(self, x):
        """Perform a single forward pass through the network.

        Args:
            param x: The input tensor.
            return: A tensor of predictions.
        """
        return self.net(x)


class LinearWithInit(nn.Module):
    """creates a linearn layer with a given activation function. The layer is initiated with different algorithms depending on the non-linear activation."""

    def __init__(
        self,
        in_features: int,
        out_features: int,
        bias: bool = False,
        activation: Any = nn.GELU(),
    ):
        """initializes a linear layer with a given activation function. The layer is initiated with different algorithms depending on the non-linear activation.

        Args:
            in_features (int): number of input neurons
            out_features (int): number of output neurons
            bias (bool, optional): Boolean for whether to use bias paramter. Defaults to False.
            activation (Any, optional): specifies the activation function to be used. Defaults to nn.GELU().
        """
        super().__init__()
        self.act_func = activation
        self.linear = nn.Linear(in_features, out_features, bias=bias)
        self._weight_initialization(self.linear, self.act_func)
        self.sequential = nn.Sequential(self.linear, self.act_func)

    def _weight_initialization(self, linear_layer, act_func):
        if isinstance(linear_layer, nn.Linear):
            if isinstance(act_func, nn.Tanh):
                nn.init.xavier_uniform_(linear_layer.weight.data)
            elif isinstance(act_func, nn.ReLU):
                nn.init.kaiming_normal_(
                    linear_layer.weight.data, nonlinearity="relu"
                )
            elif isinstance(act_func, nn.LeakyReLU):
                nn.init.kaiming_normal_(
                    linear_layer.weight.data, nonlinearity="leaky_relu"
                )
            else:
                nn.init.xavier_normal_(linear_layer.weight.data)
            if linear_layer.bias is not None:
                linear_layer.bias.data.zero_()

    def forward(self, x):
        return self.sequential(x)
