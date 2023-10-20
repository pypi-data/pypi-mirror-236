# -*- coding: utf-8 -*-
from dataclasses import dataclass
import numpy as np
import random
import os
from pathlib import Path


def seed_everything(seed: int):
    """
    Machine Learning (ML) models seed

    Seed Models
    -----------
    If you use ML models with sklearn API, always set the random_state.
    from sklearn.ensemble import RandomForestClassifier
    model = RandomForestClassifier(..., random_state=42)

    Order Matters
    -------------
    Multiple calls to random number generators potentially output differently if the orders are not fixed
    (in fact many ML models call random generators frequently). It deserves to check some containers (e.g. set, dict)
    in use, especially if your models are stored/related to these containers. Python orders may be altered after
    (unwanted/unrealized) modifications, or simply the orders rely on system implementation. If we are not so worried
    about the memory usage or performance, converting a set to sorted(list(...)) could make sure it is always called
    in the same sequence and meanwhile facilitate debugging.

    snippet from github
    ------------
        https://gist.github.com/ihoromi4/b681a9088f348942b01711f251e5f964
    """
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    np.random.seed(seed)

    try:
        import torch

        torch.manual_seed(seed)
        torch.cuda.manual_seed(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = True
    except ImportError:
        pass

    return seed


@dataclass(frozen=True)
class ModelHyper:
    random_state: int
    model_default_params: dict()
    model_cv_params: dict()

    def __post_init__(self):
        # call global seed
        seed_everything(self.random_state)
        # add sklearn - random state
        self.model_default_params.update({"random_state": self.random_state})
        # TODO: any other packages using random seed


@dataclass(frozen=True)
class ModelSpec:
    """ML model specification"""
    # name of machine learning model
    model_name: str
    # hyperparameters of machine learning model
    model_hyperparameters: ModelHyper
    # list of features before feature selection. If the model doesn't have `feature selection` module, then it will be
    # same as the feature names
    candidate_features: list
    # data to describe the model if any
    metadata: dict
    # directory to save the model
    root_path: str

    @property
    def model_path(self):
        """
        directory to save model and model metadata
            - <root_path>/<model name>
        """
        directory = Path(self.root_path, self.model_name)
        return directory


@dataclass(frozen=True)
class MLModel(ModelSpec):
    estimator: object
    feature_names: list


def get_model_object_by_name(model_name: str):
    """
    Load estimator object by name
    """
    if model_name.upper() == "LGBM":
        from lightgbm import LGBMRegressor
        return LGBMRegressor
    else:
        raise ValueError("Unknown model name.")
