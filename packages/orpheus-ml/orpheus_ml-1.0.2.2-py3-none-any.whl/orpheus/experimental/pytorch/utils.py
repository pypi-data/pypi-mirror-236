import inspect
from functools import wraps
from typing import Any, Type

import numpy as np
import pandas as pd

from orpheus.experimental.pytorch.base import PyTorchBase
from orpheus.utils.helper_functions import get_obj_name
from orpheus.utils.logger import logger


def change_default_value_init(cls: Type, param_name: str, new_value: Any) -> Type:
    """
    change default value of a parameter in a class's __init__ method

    parameters
    ----------
    cls: Type
        the class to change the default value of a parameter in its __init__ method
    param_name: str
        the name of the parameter to change the default value of
    new_value: Any
        the new default value of the parameter

    returns
    -------
    Type
        the class with the changed default value of the parameter in its __init__ method
    """
    original_init = cls.__init__
    original_signature = inspect.signature(original_init)

    new_params = [
        param.replace(default=new_value) if param.name == param_name else param
        for param in original_signature.parameters.values()
    ]
    new_signature = original_signature.replace(parameters=new_params)

    def new_init(self, *args, **kwargs):
        bound_args = new_signature.bind(self, *args, **kwargs)
        bound_args.apply_defaults()
        original_init(*bound_args.args, **bound_args.kwargs)

    new_init.__signature__ = new_signature
    cls.__init__ = new_init
    return cls


pytorch_classes = {}


def pytorch_to_component_adapter(cls):
    """
    This decorator is used to adapt a PyTorch estimator to a component.
    It is used to inject the input_dim parameter in the estimator's init method so that
    it matches the number of features in the training data.
    """
    original_init = cls.__init__

    @wraps(original_init)
    def new_init(self, *args, **kwargs):
        estimator_list = kwargs.get("estimator_list", None)
        if estimator_list is None:
            raise ValueError(f"No estimator_list was passed to {cls.__name__}")
        X_train = kwargs.get("X_train", args[0] if args else None)
        if X_train is None:
            raise ValueError(f"X_train is None in {cls.__name__}, indicating that it was not passed to the constructor")
        if not isinstance(X_train, (pd.DataFrame, np.ndarray, pd.Series)):
            raise ValueError(f"X_train is not an ArrayLike, but is {type(X_train)}")

        # Get the shape of X_train
        n_features_X_train = X_train.shape[1]
        new_estimator_list = []

        for estimator_cls in estimator_list:
            if hasattr(estimator_cls, "func"):
                estimator_cls = estimator_cls.func
            # Check if the estimator is a PyTorch estimator.
            # we need to do it like this unusual way because sourcefiles might differ
            inherits_from_pytorch_base = get_obj_name(PyTorchBase) in (
                get_obj_name(obj) for obj in estimator_cls.__bases__
            )
            if inherits_from_pytorch_base:
                # Wrap the estimator's init method to inject the new input_dim
                global pytorch_classes
                estimator_cls_name = get_obj_name(estimator_cls)
                if estimator_cls_name not in pytorch_classes:
                    pytorch_classes[estimator_cls_name] = estimator_cls
                original_estimator_cls = pytorch_classes[estimator_cls_name]

                est_cls_init_signature = inspect.signature(original_estimator_cls.__init__)
                if "input_dim" not in est_cls_init_signature.parameters:
                    raise ValueError(
                        f"{estimator_cls.__name__} does not have an 'input_dim' parameter in its __init__ method. Current __init__ signature: {est_cls_init_signature}"
                    )

                input_dim_est_cls_value = est_cls_init_signature.parameters["input_dim"].default
                if input_dim_est_cls_value == n_features_X_train:
                    logger.info(
                        f"Skipping injection of 'input_dim' in {estimator_cls.__name__} before instantiation of component {cls.__name__} because the input_dim({input_dim_est_cls_value}) is already equal to n_features of X_train({n_features_X_train})"
                    )
                    new_estimator_list.append(estimator_cls)
                    continue
                else:
                    logger.info(
                        f"Injecting 'input_dim' in {estimator_cls_name} before instantiation of component {cls.__name__} because the input_dim({input_dim_est_cls_value}) is not equal to n_features of X_train({n_features_X_train})"
                    )

                    # Inject the input_dim parameter in the estimator's init method
                    estimator_cls = change_default_value_init(estimator_cls, "input_dim", n_features_X_train)

                    # Check if the injection was successful
                    est_instance = estimator_cls()
                    if est_instance.input_dim != n_features_X_train:
                        raise ValueError(
                            f"'input_dim' was not injected in the constructor of {estimator_cls_name}, is {est_instance.input_dim} but should be {n_features_X_train}. Current __init__ signature: {est_cls_init_signature}"
                        )
                    new_estimator_list.append(estimator_cls)
            else:
                new_estimator_list.append(estimator_cls)

        if len(new_estimator_list) != len(estimator_list):
            raise ValueError(
                f"new_estimator_list has a different length than estimator_list. new_estimator_list: {new_estimator_list}, estimator_list: {estimator_list}"
            )
        kwargs["estimator_list"] = new_estimator_list
        original_init(self, *args, **kwargs)

    cls.__init__ = new_init
    return cls
