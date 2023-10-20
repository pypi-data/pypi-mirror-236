import torch

"""
Support Optimizer List.
- adam
- sgd
- rmsprop
"""

class OptimizerFactory:
    @staticmethod
    def get_optimizer(optimizer_type: str, parameters, lr=0.001, weight_decay=0.0) -> torch.optim.Optimizer:
        if optimizer_type == "adam":
            return torch.optim.Adam(parameters, lr=lr, weight_decay=weight_decay)
        elif optimizer_type == "sgd":
            return torch.optim.SGD(parameters, lr=lr, weight_decay=weight_decay)
        elif optimizer_type == "rmsprop":
            return torch.optim.RMSprop(parameters, lr=lr, weight_decay=weight_decay)
        # you can add more optimizer functions here
        else:
            raise ValueError(f"Unsupported optimizer: {optimizer_type}")

if __name__=='__main__':
    pass
    # Usage
    # optimizer = OptimizerFactory.get_optimizer("rmsprop", model.parameters(), lr=0.001)
