from functools import partial
from typing import Callable, Literal, Optional, Type

import tensorflow as tf
from keras.losses import CategoricalCrossentropy, MeanSquaredError
from keras.optimizers import SGD, Adam
from sklearn.base import BaseEstimator, ClassifierMixin, RegressorMixin
from sklearn.utils import check_array, check_X_y

from orpheus.utils.helper_functions import get_obj_name


class TensorFlowWrapper(BaseEstimator):
    """
    Sklearn Wrapper for TensorFlow
    """

    def __init__(
        self,
        model: Optional[Type[tf.keras.Model]] = None,
        criterion: Optional[str] = None,
        optimizer: Literal["Adam", "SGD"] = "Adam",
        epochs: int = 10,
        learning_rate: float = 0.01,
        batch_size: int = 256,
        verbose: bool = False,
    ):
        self.model = model
        self.criterion = criterion
        self.optimizer = optimizer
        self.epochs = epochs
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        self.verbose = verbose

        self._check_estimator_type()

    def fit(self, X, y):
        # validate data
        X, y = check_X_y(X, y)
        self.n_features_in_ = X.shape[1]

        # instantiate model, optimizer and criterion
        self._instantiate_params(X, y)

        self.model.compile(loss=self.criterion, optimizer=self.optimizer)

        self.model.fit(X, y, epochs=self.epochs, batch_size=self.batch_size, verbose=self.verbose)

        return self

    def predict(self, X):
        X = check_array(X)
        return self.model.predict(X)

    def _instantiate_params(self, X, y):
        if not hasattr(self, "_estimator_type"):
            self._estimator_type = "classifier" if len(set(y)) > 2 else "regressor"

        if self.model is None:
            raise ValueError(f"model is None. Please provide a valid TensorFlow model.")
        else:
            self.model = self.model()

        if self.criterion is None:
            if self._estimator_type == "regressor":
                self.criterion = MeanSquaredError()
            else:
                self.criterion = CategoricalCrossentropy()

        if self.optimizer == "Adam":
            self.optimizer = Adam(learning_rate=self.learning_rate)
        elif self.optimizer == "SGD":
            self.optimizer = SGD(learning_rate=self.learning_rate)

    def _check_estimator_type(self):
        if not (issubclass(self.model, ClassifierMixin) or issubclass(self.model, RegressorMixin)):
            raise ValueError(f"model should be either ClassifierMixin or RegressorMixin subclass")


class TensorFlowSklearnAdapter:
    """
    Factory to create TensorFlowWrapper instances from TensorFlow models.
    """

    @staticmethod
    def convert(
        model: Optional[Type[tf.keras.Model]] = None,
        criterion: Optional[str] = None,
        optimizer: Literal["Adam", "SGD"] = "Adam",
        epochs: int = 10,
        learning_rate: float = 0.01,
        batch_size: int = 256,
        verbose: bool = False,
    ) -> Callable[..., TensorFlowWrapper]:
        TensorFlowSklearnAdapter.check_tensorflow_model(model)

        tensorflow_wrapper = partial(
            TensorFlowWrapper,
            model=model,
            epochs=epochs,
            learning_rate=learning_rate,
            batch_size=batch_size,
            criterion=criterion,
            optimizer=optimizer,
            verbose=verbose,
        )

        return tensorflow_wrapper

    @staticmethod
    def check_tensorflow_model(model: Type[tf.keras.Model]):
        """Check if the provided model class is a valid TensorFlow model."""
        if not isinstance(model, type):
            raise ValueError(f"model must be a class, not {model}")
        if not issubclass(model, tf.keras.Model):
            raise ValueError(f"model {model} must be a baseclass of tf.keras.Model, but is {model.__bases__}")
        if not callable(model):
            raise ValueError(f"Provided model {model} is not callable.")

        # Check that the call method has been overridden in the derived class
        if model.call == tf.keras.Model.call or model.call.__qualname__ != f"{get_obj_name(model)}.call":
            raise ValueError(f"call method must be overridden in the model {model}.")
