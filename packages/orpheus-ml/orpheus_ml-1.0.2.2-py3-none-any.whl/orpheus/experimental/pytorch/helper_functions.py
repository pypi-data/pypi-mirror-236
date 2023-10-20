"""helperfunctions for experimental module"""

from typing import Any, Literal
import numpy as np
import torch

from orpheus.experimental.pytorch.constants import (
    CLASSIFIER_LOSS_KEYS,
    NUMPY_TO_TORCH_MAPPING,
    OPTIMIZER_KEYS,
    PYTORCH_LOSS_FUNCTIONS,
    PYTORCH_OPTIMIZERS,
    REGRESSOR_LOSS_KEYS,
)
from orpheus.utils.helper_functions import ensure_numpy
from orpheus.utils.type_vars import ArrayLike


def infer_best_dtype(data: np.ndarray):
    """Infer the best torch dtype for a given numpy array."""
    max_val = max(data)
    min_val = min(data)

    # For non-negative integers
    if min_val >= 0:
        if max_val <= 255:
            return torch.uint8
        elif max_val <= 32767:
            return torch.int16
        elif max_val <= 2147483647:
            return torch.int32
        else:
            return torch.int64
    # For possibly negative integers
    else:
        if -128 <= min_val and max_val <= 127:
            return torch.int8
        elif -32768 <= min_val and max_val <= 32767:
            return torch.int16
        elif -2147483648 <= min_val and max_val <= 2147483647:
            return torch.int32
        else:
            return torch.int64


def set_criterion(model: torch.nn.Module, criterion: str, estimator_type: str) -> torch.nn.modules.loss._Loss:
    """Set the criterion for a PyTorch model."""
    if criterion is None:
        if estimator_type == "regressor":
            criterion = "mse"
        elif estimator_type == "classifier":
            criterion = "cross_entropy"
        else:
            raise ValueError(f"estimator_type {estimator_type} not found in {['classifier', 'regressor']}")

    # fetch the loss function from the criterion dict
    if criterion in PYTORCH_LOSS_FUNCTIONS["regressor"]:
        loss_func = PYTORCH_LOSS_FUNCTIONS["regressor"][criterion]["loss"]
    elif criterion in PYTORCH_LOSS_FUNCTIONS["classifier"]:
        loss_func = PYTORCH_LOSS_FUNCTIONS["classifier"][criterion]["loss"]
    else:
        raise ValueError(f"criterion '{criterion}' not found in {REGRESSOR_LOSS_KEYS} or {CLASSIFIER_LOSS_KEYS}")

    # check if minimum output_dim of model is compatible with criterion:
    model_output_dim = get_n_out_features_from_model(model)
    min_criterion_output_dim = PYTORCH_LOSS_FUNCTIONS[estimator_type][criterion]["min_output_dim"]
    if model_output_dim < min_criterion_output_dim:
        raise ValueError(
            f"Criterion '{criterion}' requires an output_dim of at least {min_criterion_output_dim}, "
            f"but the model {type(model)} has an output_dim of {model_output_dim}."
        )

    return loss_func


def set_optimizer(model: torch.nn.Module, optimizer: str, learning_rate: float) -> torch.optim.Optimizer:
    """Set the optimizer for a PyTorch model."""
    if optimizer in PYTORCH_OPTIMIZERS:
        return PYTORCH_OPTIMIZERS[optimizer](model.parameters(), lr=learning_rate)
    else:
        raise ValueError(f"optimizer '{optimizer}' not found in {OPTIMIZER_KEYS}")


def get_n_in_features_from_model(model: torch.nn.Module) -> int:
    """Get the number of input features from a PyTorch model."""
    return next(iter(model._modules.values())).in_features


def get_n_out_features_from_model(model: torch.nn.Module) -> int:
    """Get the number of output features from a PyTorch model."""
    return next(iter(model._modules.values())).out_features


def tensorize_data(data: ArrayLike, device) -> torch.Tensor:
    """
    Convert data for a torch tensor while preserving its datatype.

    Returns:
        torch.Tensor: The converted data as a torch tensor.
    """
    data = ensure_numpy(data)
    dtype = NUMPY_TO_TORCH_MAPPING.get(data.dtype.type, torch.float32)
    tensor_data = torch.tensor(data, dtype=dtype)

    # Moving the data to the device where the model is.
    return tensor_data.to(device)


def concat_pytorch_path(path: str) -> str:
    """Concatenate the .pt file ending to a path if it is not already present."""
    if not path.endswith(".pt"):
        return f"{path}.pt"
    return path


DEFAULT_EPOCHS = 100
DEFAULT_LR = 0.01
DEFAULT_BATCH_SIZE = 256


def validate_param(
    param: Any,
    param_name: str,
    expected_type: Any,
    model_name: str,
    default_suggestion: Any,
    class_example1: str,
    class_example2: str,
    min_value=None,
):
    """Validate a parameter of a model which inherits from PyTorchBase"""

    if param is None:
        raise ValueError(
            f"'{param_name}' must be specified in the signature of super().__init__ in the constructor of {model_name}!\n"
            f"\nExample 1, initialize the parameters with default values in the signature to tune them during R2 and R3 in HyperTuner.fit():\n{class_example1}\n"
            f"\nExample 2, initialize the parameters in super()__init__ to exclude them for tuning. initialize other parameters in constructor signature to tune them during R2 and R3 in HyperTuner.fit():\n{class_example2}"
        )

    if not isinstance(param, expected_type):
        raise TypeError(f"{param_name} must be of type {expected_type.__name__}! {default_suggestion}")

    if min_value is not None and param < min_value:
        raise ValueError(f"{param_name} must be >= {min_value}! {default_suggestion}")


def validate_init_params_pytorch_base(
    model: torch.nn.Module,
    input_dim: int,
    output_dim: int,
    epochs: int,
    learning_rate: float,
    batch_size: int,
    validation_size: float,
    patience: int,
    device: Literal["cpu", "cuda"],
):
    """Validate the init parameters of a model which inherits from PyTorchBase"""
    model_name = type(model).__name__

    # Construct the example strings just once
    class_example1 = f"""class {model_name}(PyTorchBase):
    def __init__(self, epochs={DEFAULT_EPOCHS}, learning_rate={DEFAULT_LR}, batch_size={DEFAULT_BATCH_SIZE}):
        super().__init__(
            input_dim=X.shape[1],
            output_dim=y.shape[1],
            epochs=epochs,
            learning_rate=,
            batch_size=batch_size,
        )"""

    class_example2 = f"""class {model_name}(PyTorchBase):
    def __init__(self, param1=10, param2=20):
        super().__init__(
            input_dim=X.shape[1],
            output_dim=y.shape[1],
            epochs={DEFAULT_EPOCHS},
            learning_rate={DEFAULT_LR},
            batch_size={DEFAULT_BATCH_SIZE},
        self.param1 = param1
        self.param2 = param2
        )"""

    # Pass the examples to the validate_param function
    validate_param(
        input_dim,
        "input_dim",
        int,
        model_name,
        "try setting the number of features as the default value",
        class_example1,
        class_example2,
        1,
    )
    validate_param(
        output_dim,
        "output_dim",
        int,
        model_name,
        "maybe try setting the number of targets as the default value",
        class_example1,
        class_example2,
        1,
    )
    validate_param(
        epochs,
        "epochs",
        int,
        model_name,
        f"maybe try a default value of epochs={DEFAULT_EPOCHS}",
        class_example1,
        class_example2,
        1,
    )
    validate_param(
        learning_rate,
        "learning_rate",
        (float, int),
        model_name,
        f"maybe try a default value of learning_rate={DEFAULT_LR}",
        class_example1,
        class_example2,
        0,
    )
    validate_param(
        batch_size,
        "batch_size",
        int,
        model_name,
        f"maybe try a default value of batch_size={DEFAULT_BATCH_SIZE}",
        class_example1,
        class_example2,
        1,
    )

    if not isinstance(validation_size, float):
        raise TypeError(f"validation_size must be of type float, but got {type(validation_size)}")
    if not 0 < validation_size < 1:
        raise ValueError(f"validation_size must be between 0 and 1, but got {validation_size}")

    if not isinstance(patience, int):
        raise TypeError(f"patience must be of type int, but got {type(patience)}")
    if patience < 0:
        raise ValueError(f"patience must be >= 0!, but got {patience}")

    if not isinstance(device, str):
        raise TypeError(f"device must be of type str, but got {type(device)}")
    if device not in {"cpu", "cuda"}:
        raise ValueError(f"device must be either 'cpu' or 'cuda', but got {device}")
