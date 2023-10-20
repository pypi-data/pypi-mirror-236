import tensorflow as tf


class TensorFlowMixin:
    """Mixin for TensorFlow models."""

    def __init__(self, device: str = "GPU:0" if tf.config.experimental.list_physical_devices("GPU") else "CPU:0"):
        self.device = device

    def call(self, inputs: tf.Tensor) -> tf.Tensor:
        """
        call method for TensorFlow models. This must be implemented in each child class.
        """
        raise NotImplementedError("call method must be implemented in TensorFlow models")

    def pre_epoch(self) -> None:
        """
        Implement a hook here if you want to do something before each epoch.
        """

    def post_epoch(self) -> None:
        """
        Implement a hook here if you want to do something after each epoch.
        """

    def save_model(self, path: str) -> None:
        """
        Save the model state.

        Parameters:
        path (str): Path where the model state will be saved.
        """
        path = self._concat_tensorflow_path(path)
        self.save_weights(path)

    def load_model(self, path: str) -> tf.keras.Model:
        """
        Load the model state and update the parameters of an existing model.

        Parameters:
        path (str): Path where the model state is located.

        Returns:
        tf.keras.Model: The model with the updated parameters.
        """
        path = self._concat_tensorflow_path(path)
        self.load_weights(path)
        return self

    def _concat_tensorflow_path(self, path: str) -> str:
        if not path.endswith(".h5"):
            return f"{path}.h5"
        return path
