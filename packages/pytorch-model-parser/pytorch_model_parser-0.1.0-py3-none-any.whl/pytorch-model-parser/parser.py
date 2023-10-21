import torch.nn as nn


def parse_model(model):
    layer_details = []

    for name, module in model.named_modules():
        if isinstance(module, nn.Conv2d):
            details = {
                "name": name,
                "type": "Conv2d",
                "out_channels": module.out_channels
            }
            layer_details.append(details)
        # Add other layer types as needed

        elif isinstance(module, nn.Dense):
            details = {
                "name": name,
                "type": "Fully Connected",
                "out_channels": module.out_channels
            }
            layer_details.append(details)

    return layer_details
