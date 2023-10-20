import torch

"""
Support Loss List.
- cross_entropy
- mse
- l1
"""

class LossFunctionFactory:
    @staticmethod
    def get_loss_function(loss_type: str):
        if loss_type == "cross_entropy":
            return torch.nn.CrossEntropyLoss()
        elif loss_type == "mse": 
            return torch.nn.MSELoss()
        elif loss_type == 'l1':
            return torch.nn.L1Loss()
        # you can add more loss functions here
        else:
            raise ValueError(f"Unsupported loss function: {loss_type}")


if __name__=='__main__' :
    # Usage
    loss_function = LossFunctionFactory.get_loss_function("mse")  # MSE loss
