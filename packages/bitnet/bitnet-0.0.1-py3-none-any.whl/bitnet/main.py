import torch 
from torch import nn
import torch.nn.functional as F

def absmax_quantize(x):
    #calculate scale
    scale = 127 / torch.max(torch.abs(x))

    #quantize
    quant = (scale * x).round()

    #dequantize
    dequant = quant / scale


    return quant.to(torch.int8), dequant


class BitLinear(nn.Module):
    def __init__(
        self,
        dim,
    ):
        super().__init__()
        self.dim = dim

        self.norm = nn.LayerNorm(dim)
        self.linear = nn.Linear(dim, dim)
        self.abs_max_quantization = absmax_quantize

    def forward(self, x):
        x = self.norm(x)

        #Binarize the weights
        weight = self.linear.weight
        weight_binarized = torch.sign(weight)

        #Apply the linear operation with the binarized weights
        x = F.linear(x, weight_binarized, self.linear.bias)

        #quantize the output
        x, dequant = self.abs_max_quantization(x)

        #dequant the output
        dequant = dequant * torch.norm(weight) / (self.dim ** -0.5)

        return x, dequant
    

#example
x = torch.randn(10, 512)
layer = BitLinear(512)
y, dequant = layer(x)
print(y, dequant)