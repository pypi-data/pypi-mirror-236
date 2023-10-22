![LangTorch Logo](langtorch_logo.png) 
# LangTorch

LangTorch is a Python package designed to simplify the development of LLM applications by leveraging familiar PyTorch concepts.

## Installation

```bash
pip install langtorch
```

## Overview

LangTorch provides a structured approach to LLM applications, offering:

- **TextTensors**: A unified way to handle prompt templates, completion dictionaries, and chat histories.
- **TextModules**: Building blocks, derived from torch.nn.Module, specifically tailored for text operations and LLM calls both locally and via an API.
- other things that are also better than langchain
## Examples

### TextTensors

Creating and manipulating textual data as tensors:

```python
template = TextTensor([["Summarize {theory} in terms of {framework}"],
                       ["Argue that {framework} can prove {theory}" ]])

template * TextTensor({"theory": "causal inference", 
                    "framework": "thermodynamics" })

# Outputs: [[Summarize causal inference in terms of thermodynamics]
#           [Argue that thermodynamics can prove causal inference ]] 
```

### TextModules

Building sequences of operations on text data:

```python
chain = torch.nn.Sequential(
    TextModule("Calculate this equation: {}"),
    langtorch.methods.CoT,
    GPT4
    TextModule("Is this reasoning correct? {}", activation = GPT4)
)

output = chain(TextTensor(["170*32 =", "4*20 =", "123*45/10 =", "2**10*5 ="]))
```

### Cosine Similarities

Compute similarities between entries:

```python
from langtorch.tt import CosineSimilarity

cos = CosineSimilarity()
similarities = cos(TextTensor([["Yes"], ["No"]]), TextTensor(["1", "0", "Noo", "Yees"]))
```

## Contribute

Your feedback and contributions are valued. Feel free to check out our [contribution guidelines](#).

## License

LangTorch is MIT licensed. See the [LICENSE](#) file for details.
