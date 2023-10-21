# PyTorch Model Parser

A library to parse PyTorch CNN models and retrieve layer details.


## Usage

```python
import pprint
from pytorch_model_parser import parse_model
import torchvision.models as models

# Load a pre-trained model
model = models.resnet18(pretrained=True)

# Parse the model
layer_details = parse_model(model)

pprint.pprint(layer_details)



## Installation

To install the library, use the following command:

```bash
pip install pytorch-model-parser


