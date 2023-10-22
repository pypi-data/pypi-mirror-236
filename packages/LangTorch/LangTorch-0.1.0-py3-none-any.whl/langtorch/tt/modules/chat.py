from typing import Optional, Union, List
from langtorch import TextTensor, ChatTensor
import langtorch.torch_utils
import langtorch.utils
from langtorch.utils import iter_subarrays
import torch
from langtorch.embedding import get_embedding


class ChatModule(TextModule):
    def __init__(self, content = "", activation=lambda x:x, key=None):
        super().__init__(content, activation, key)
        self.content = ChatTensor(self.content)