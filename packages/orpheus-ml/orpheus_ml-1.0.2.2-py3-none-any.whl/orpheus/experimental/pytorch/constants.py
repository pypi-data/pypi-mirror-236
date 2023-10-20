"""Constants for the PyTorch backend."""

import numpy as np
import torch
import torch.optim as optim
import torch.nn as nn
from typing import Literal

# map numpy dtypes to torch dtypes
NUMPY_TO_TORCH_MAPPING = {
    np.float16: torch.float,
    np.float32: torch.float,
    np.float64: torch.float,
    np.int8: torch.long,
    np.int16: torch.long,
    np.int32: torch.long,
    np.int64: torch.long,
    np.uint8: torch.long,
    np.bool_: torch.bool,
    np.complex64: torch.float,
    np.complex128: torch.float,
}

PYTORCH_OPTIMIZERS = {
    "Adam": optim.Adam,
    "SGD": optim.SGD,
    "Adagrad": optim.Adagrad,
    "Adadelta": optim.Adadelta,
    "AdamW": optim.AdamW,
    "Adamax": optim.Adamax,
    "ASGD": optim.ASGD,
    "RMSprop": optim.RMSprop,
    "Rprop": optim.Rprop,
    "LBFGS": optim.LBFGS,
}

PYTORCH_LOSS_FUNCTIONS = {
    "regressor": {
        "mse": {"loss": nn.MSELoss(), "min_output_dim": 1},
        "smooth_l1_loss": {"loss": nn.SmoothL1Loss(), "min_output_dim": 1},
        "poisson_nll_loss": {"loss": nn.PoissonNLLLoss(), "min_output_dim": 1},
        "l1_loss": {"loss": nn.L1Loss(), "min_output_dim": 1},
        "cosine_similarity": {"loss": nn.CosineSimilarity(), "min_output_dim": 1},
        "kldiv_loss": {"loss": nn.KLDivLoss(), "min_output_dim": 1},
        "huber_loss": {"loss": nn.HuberLoss(), "min_output_dim": 1},
    },
    "classifier": {
        "cross_entropy": {"loss": nn.CrossEntropyLoss(), "min_output_dim": 2},  # expects raw scores for each class
        "nll_loss": {"loss": nn.NLLLoss(), "min_output_dim": 2},  # expects log probabilities for each class
        "bce_loss": {"loss": nn.BCELoss(), "min_output_dim": 1},  # expects a probability (between 0 and 1)
        "bce_with_logits": {"loss": nn.BCEWithLogitsLoss(), "min_output_dim": 1},  # expects raw score (logit)
        "multi_label_margin_loss": {"loss": nn.MultiLabelMarginLoss(), "min_output_dim": 2},
        "hinge_embedding_loss": {"loss": nn.HingeEmbeddingLoss(), "min_output_dim": 1},
        "multi_label_soft_margin_loss": {"loss": nn.MultiLabelSoftMarginLoss(), "min_output_dim": 2},
        "margin_ranking_loss": {"loss": nn.MarginRankingLoss(), "min_output_dim": 1},
        "multi_margin_loss": {"loss": nn.MultiMarginLoss(), "min_output_dim": 2},
        "triplet_margin_loss": {"loss": nn.TripletMarginLoss(), "min_output_dim": 1},
        "kl_div": {"loss": nn.KLDivLoss(), "min_output_dim": 2},
        "cosine_embedding_loss": {"loss": nn.CosineEmbeddingLoss(), "min_output_dim": 1},
        "log_softmax": {"loss": nn.LogSoftmax(), "min_output_dim": 2},
        "softmax": {"loss": nn.Softmax(), "min_output_dim": 2},
    },
}

OPTIMIZER_KEYS = list(PYTORCH_OPTIMIZERS.keys())
REGRESSOR_LOSS_KEYS = list(PYTORCH_LOSS_FUNCTIONS["regressor"].keys())
CLASSIFIER_LOSS_KEYS = list(PYTORCH_LOSS_FUNCTIONS["classifier"].keys())

RegressorLossType = Literal[tuple(CLASSIFIER_LOSS_KEYS)]  # type: ignore
ClassifierLossType = Literal[tuple(CLASSIFIER_LOSS_KEYS)]  # type: ignore
OptimizerType = Literal[tuple(OPTIMIZER_KEYS)]  # type: ignore
