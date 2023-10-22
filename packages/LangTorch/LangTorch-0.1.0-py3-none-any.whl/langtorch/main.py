import sys

import torch.nn

sys.path.append("D:/langtorch/src")

import langtorch
from langtorch.tt import TextModule, ActivationGPT
from langtorch import Text, TextTensor
from api import auth
import torch

auth(key_path = "D:/api_keys.json")


class PrintModule(torch.nn.Module):
    def forward(self, x):
        print(x)
        return x

activation = torch.nn.Sequential(
    PrintModule(),
    ActivationGPT()
)
module = TextModule(["{input}... say the word ŻóŁW", "{input}... say the word 'wżód'"],
                    activation=activation)


input_tensor = TextTensor("{Do the follwoing task :input}")
print(module(input_tensor))
