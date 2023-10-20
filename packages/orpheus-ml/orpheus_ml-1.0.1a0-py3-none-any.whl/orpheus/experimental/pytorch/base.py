"""
PyTorch wrapper for Orpheus. Use PyTorchSklearnAdapter.convert() to convert a PyTorch model to 
make it compatible with Orpheus according to the scikit-learn API.
"""

import inspect
import re
from typing import Literal, Optional

import numpy as np
import torch
from sklearn.base import BaseEstimator, ClassifierMixin, RegressorMixin
from sklearn.exceptions import NotFittedError
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, TensorDataset

from orpheus.experimental.pytorch.constants import OptimizerType
from orpheus.experimental.pytorch.helper_functions import (
    concat_pytorch_path,
    set_criterion,
    set_optimizer,
    tensorize_data,
    validate_init_params_pytorch_base,
)
from orpheus.utils.helper_functions import target_is_classifier
from orpheus.utils.type_vars import ArrayLike


class PyTorchBase(torch.nn.Module, BaseEstimator):
    """
    base wrapper-class for all PyTorch models.
    """

    def __init_subclass__(cls, **kwargs):
        """Check that the subclass has a valid __init__ method"""

        super().__init_subclass__(**kwargs)

        child_init_signature = inspect.signature(cls.__init__)
        child_init_source = inspect.getsource(cls.__init__)
        init_signature = inspect.signature(PyTorchBase.__init__)
        init_signature_params = {param for param, val in init_signature.parameters.items() if not param == "self"}

        if "super().__init__(" not in child_init_source:
            raise TypeError(f"__init__ method in {cls.__name__} must call super().__init__()")
        super_init_string = child_init_source.split("super().__init__(")[1].split(")")[0]

        for param, val in child_init_signature.parameters.items():
            if param == "self":
                continue
            if val.default is inspect.Parameter.empty:
                raise ValueError(f"Parameter {param} in {cls.__name__} must have a default value")

            if param in init_signature_params:
                if re.search(re.escape(param) + r"\s*=", super_init_string) is None:
                    raise TypeError(f"Parameter {param} in {cls.__name__} must be passed to super().__init__()")

            elif re.search(r"self\." + re.escape(param) + r"\s*=", child_init_source) is None:
                raise TypeError(f"Parameter {param} in {cls.__name__} must be an instance attribute")

    def __init__(
        self,
        input_dim: int = None,
        output_dim: int = None,
        epochs: int = None,
        learning_rate: float = None,
        batch_size: int = None,
        criterion: Optional[str] = None,
        optimizer: OptimizerType = "Adam",
        early_stopping: bool = False,
        patience: int = 50,
        validation_size: Optional[float] = None,
        device: Literal["cpu", "cuda"] = "cpu",
        verbose: bool = False,
    ):
        """
        parameters:
        ----------
        model: Callable[..., torch.nn.Module]
            The model class with a predefined NN-architecture.
        epochs: int, optional
            The number of epochs to train the model, by default 10.
        learning_rate: float, optional
            The learning rate for the optimizer, by default 0.001.
        criterion: str, optional
            The loss function to use for training, by default None.
            If None, the loss function is chosen based on the type of estimator.
        optimizer: Literal["Adam", "SGD"], optional
            The optimizer to use for training, by default "Adam".
        early_stopping: bool, optional
            Whether to use early stopping, by default False.
        patience: int, optional
            The number of epochs with no improvement after which training will be stopped if early stopping is used, by default 50.
        verbose: bool, optional
            Whether to print the loss for each epoch, by default False.
        validation_size: float, optional
            The proportion of the data to use for validation if early stopping is used, by default None.
            If None, the validation data is not used. Else, must be range (0, 1).
        """
        validate_init_params_pytorch_base(
            self,
            input_dim=input_dim,
            output_dim=output_dim,
            epochs=epochs,
            learning_rate=learning_rate,
            batch_size=batch_size,
            validation_size=validation_size,
            patience=patience,
            device=device,
        )

        super().__init__()
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.epochs = epochs
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        self.criterion = criterion
        self.optimizer = optimizer
        self.early_stopping = early_stopping
        self.patience = patience
        self.validation_size = validation_size
        self.verbose = verbose
        self.device = device

        self.losses: list[float] = []
        self._is_fitted = False
        self._device: torch.device = torch.device(self.device)
        self._optimizer: Optional[torch.optim.Optimizer] = None
        self._criterion: Optional[torch.nn.Module] = None

        if issubclass(type(self), ClassifierMixin):
            self._estimator_type = "classifier"
        elif issubclass(type(self), RegressorMixin):
            self._estimator_type = "regressor"
        else:
            self._estimator_type = None

    def fit(self, X: ArrayLike, y: ArrayLike) -> "PyTorchBase":
        """
        Fit the model to the training data

        Creates attributes
        -------------------
        _optimizer: torch.optim.Optimizer
            The instantiated optimizer
        _criterion: torch.nn.Module
            The instantiated criterion
        losses: list[float]
            The losses for each epoch. Can be used for plotting the loss curve.

        parameters:
        ----------
        X: ArrayLike
            The training data
        y: ArrayLike
            The training targets
        X_val: Optional[ArrayLike], optional
            The validation data, by default None
        y_val: Optional[ArrayLike], optional
            The validation targets, by default None

        Returns:
        --------
        self: PyTorchBase
        """
        if self.input_dim != X.shape[1]:
            raise ValueError(
                f"'input_dim' of model {type(self).__name__} ({self.input_dim}) does not match number of features ({X.shape[1]})"
            )
        self._set_attributes_in_fit(y)
        self.to(self._device)

        X = tensorize_data(X, self._device)
        y = tensorize_data(y, self._device)

        # If validation_size is provided, split the dataset into training and validation
        if self.validation_size is not None:
            X, X_val, y, y_val = train_test_split(X, y, test_size=self.validation_size, shuffle=False)
            val_loader = DataLoader(TensorDataset(X_val, y_val), batch_size=self.batch_size)

        train_loader = DataLoader(TensorDataset(X, y), batch_size=self.batch_size)

        best_loss = current_loss = float("inf")
        patience_counter = 0

        self.pre_train()

        for epoch, _ in enumerate(range(self.epochs), start=1):
            self.pre_epoch()

            for X_batch, y_batch in train_loader:
                self._optimizer.zero_grad()
                output = self(X_batch)
                loss = self._criterion(output, y_batch)
                loss.backward()
                self._optimizer.step()
                current_loss = loss.item()
                self.losses.append(current_loss)

                if self.verbose:
                    print(f"model_id: {id(self)}, Epoch {epoch}/{self.epochs}, Loss: {current_loss:.4f}")

            if self.validation_size is not None:
                current_loss = self._evaluate_validation_loss(val_loader)
                if self.verbose:
                    print(f"model_id: {id(self)}, Validation Loss: {current_loss:.4f}")

            self.post_epoch()

            # Early stopping logic
            if self.early_stopping:
                if current_loss < best_loss:
                    best_loss = current_loss
                    patience_counter = 0
                else:
                    patience_counter += 1
                    if patience_counter >= self.patience:
                        if self.verbose:
                            print(f"model_id: {id(self)}, Early stopping at epoch {epoch}, best loss was {best_loss}.")
                        break

        self.post_train()
        self._is_fitted = True

        return self

    def predict(self, X: ArrayLike) -> np.ndarray:
        """Predict the target values for the given data"""
        if not self._is_fitted:
            raise NotFittedError("Model must be fitted before calling predict")
        X = tensorize_data(X, self._device)
        self.eval()
        with torch.no_grad():
            predictions = self(X)

        predictions_numpy = predictions.to("cpu").numpy()
        predictions_numpy = self._get_pred(predictions_numpy)

        return predictions_numpy

    def predict_proba(self, X: ArrayLike) -> np.ndarray:
        """
        Predict the probability distributions for the given data.
        Only valid for classifiers.
        """
        if self._estimator_type != "classifier":
            raise ValueError("predict_proba is only available for classifiers")

        X = tensorize_data(X, self._device)
        self.eval()
        with torch.no_grad():
            probabilities = torch.nn.functional.softmax(self(X), dim=-1)
        return probabilities.to("cpu").numpy()

    def forward(self, X: torch.Tensor) -> torch.Tensor:
        """
        Forward method for PyTorch models. This must be implemented in each child class.
        """
        raise NotImplementedError("forward method must be implemented in PyTorch models")

    def pre_train(self) -> None:
        """
        Override this function in PyTorch class to Implement a hook if you want to do something before training starts.
        """

    def post_train(self) -> None:
        """
        Override this function in PyTorch class to implement a hook if you want to do something after training ends.
        """

    def pre_epoch(self) -> None:
        """
        Override this function in PyTorch class to implement a hook if you want to do something before each epoch.
        """

    def post_epoch(self) -> None:
        """
        Override this function in PyTorch class to implement a hook if you want to do something after each epoch.
        """

    def save_model(self, path: str) -> None:
        """
        Save the model state.

        Parameters:
        path (str): Path where the model state will be saved.
        """
        path = concat_pytorch_path(path)
        torch.save(self.state_dict(), path)

    def load_model(self, path: str) -> torch.nn.Module:
        """
        Load the model state and update the parameters of an existing model.

        Parameters:
        path (str): Path where the model state is located.

        Returns:
        torch.nn.Module: The model with the updated parameters.
        """
        path = concat_pytorch_path(path)
        self.load_state_dict(torch.load(path))
        return self

    def _set_attributes_in_fit(self, y: ArrayLike) -> None:
        """
        Set attributes in fit method.
        Because some attributes are inferred from the target, they can only be set after the target is known.
        """
        # pylint: disable=W0201
        if self._estimator_type is None:
            self._estimator_type = "classifier" if target_is_classifier(y) else "regressor"

            # dynamically add regressor or classifiermxin from sklearn:
            self._mixin_on_demand(self._estimator_type)

        if self._criterion is None:
            self._criterion = set_criterion(self, self.criterion, self._estimator_type)

        if self._optimizer is None:
            self._optimizer = set_optimizer(self, self.optimizer, self.learning_rate)

    def _evaluate_validation_loss(self, val_loader: DataLoader) -> float:
        self.eval()
        with torch.no_grad():
            loss_val_sum = 0
            for X_val_batch, y_val_batch in val_loader:
                output_val = self(X_val_batch)
                loss_val = self._criterion(output_val, y_val_batch)
                loss_val_sum += loss_val.item()
        self.train()
        return loss_val_sum / len(val_loader)

    def _get_pred(self, predictions_numpy: np.ndarray) -> np.ndarray:
        if self._estimator_type is None:
            raise ValueError("_estimator_type must be set in fit method, but is None")
        if self._estimator_type == "classifier":
            predictions_numpy = np.argmax(predictions_numpy, axis=-1)
        elif self._estimator_type == "regressor":
            predictions_numpy = predictions_numpy.squeeze()
        else:
            raise ValueError(f"estimator_type {self._estimator_type} not found in {['classifier', 'regressor']}")
        return predictions_numpy

    def _apply_mixin(self, mixin_base: RegressorMixin | ClassifierMixin) -> None:
        """Add attributes/methods from mixin to instance's class and add mixin to instance's bases"""
        for name, method in mixin_base.__dict__.items():
            if not name.startswith("__"):
                setattr(self.__class__, name, method)
        new_bases = list(self.__class__.__bases__) + [
            mixin_base,
        ]
        self.__class__.__bases__ = tuple(new_bases)

    def _mixin_on_demand(self, estimator_type: str) -> None:
        """Dynamicly add mixin to self as subclass"""
        if estimator_type == "classifier":
            mixin_base = ClassifierMixin
        elif estimator_type == "regressor":
            mixin_base = RegressorMixin
        else:
            raise ValueError(f"Unknown estimator type: {estimator_type}")

        if not issubclass(self.__class__, mixin_base):
            self._apply_mixin(mixin_base)
