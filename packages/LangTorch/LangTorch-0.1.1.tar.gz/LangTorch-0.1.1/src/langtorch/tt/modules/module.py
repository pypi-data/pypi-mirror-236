import time
from typing import Optional, Union, List
from langtorch import TextTensor
import langtorch.torch_utils
import langtorch.utils
from langtorch.utils import iter_subarrays
import torch
from langtorch.embedding import get_embedding

class TextModule(torch.nn.Module):
    def __init__(self,
                 content: Optional[Union[str, 'TextTensor']] = "",
                 activation=lambda x: x,
                 key=None,
                 memoize=False, *args, **kwargs):
        super(TextModule, self).__init__(*args, **kwargs)
        self._content = TextTensor(content) if not isinstance(content, TextTensor) else content
        self.unformatted_content = TextTensor(content)
        self.activation = activation  # An identity function if nothing is passed
        self.memo = {} if memoize else None
        self.target_embedding = None
        self.key = key

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, content):
        self._content = content.content if isinstance(content, TextModule) else content if isinstance(content, TextTensor) else TextTensor(content)
        assert self._content is not None
        self.unformatted_content = TextTensor(self._content.content)

    def forward(self, input, **kwargs) -> TextTensor:
        if len(kwargs.keys()) > 0:
            for k, v in kwargs.items():
                self._content.content = self._content.format(**{k: v}).content
        if self.memo is None:
            output = self._forward(input)
            self.reset_formatting()
            return output if self.key is None else output.set_key(self.key)
        # Memoization
        input_tuple = langtorch.tensor_or_tensors_to_tuple(input)
        if input_tuple in self.memo:
            return self.memo[input_tuple]


        assert isinstance(input, TextTensor)
        output = self._forward(input)
        self.memo[input_tuple] = output
        self.reset_formatting()
        return output if self.key is None else output.set_key(self.key)

    def _forward(self, input) -> TextTensor:
        return self.activation(self.content * input.content)

    def reset_formatting(self):  # maybe to this with .grad, riski with no_grad()
        self._content.content = self.unformatted_content.content

    def __str__(self):
        return str(self.content)

    def __repr__(self):
        return str(self.content)

    def __len__(self):
        return len(self.content)

    def __contains__(self, item):
        return item in self.content

    def embed(self):
        self.embedding = get_embedding(self.content)
