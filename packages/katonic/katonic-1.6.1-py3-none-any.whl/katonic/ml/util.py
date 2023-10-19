#!/usr/bin/env python
#
# Copyright (c) 2023 Katonic Pty Ltd. All rights reserved.
#
import os
from typing import Optional

import mlflow
import numpy as np
import pandas as pd


mlflow.set_tracking_uri(os.environ["MLFLOW_BASE_URL"])
client = mlflow.tracking.MlflowClient(os.environ["MLFLOW_BASE_URL"])


def get_exp(exp_name: str):
    """
    Retrieve an experiment by experiment name from the backend store.

    Args:
        exp_name (str): The case senstive experiment name.
    """
    exp_details = mlflow.get_experiment_by_name(exp_name)
    if exp_details is None:
        raise ValueError(f"Given experiment name '{exp_name}' is not available.")

    result = {
        "experiment_name": exp_details.name,
        "location": exp_details.artifact_location,
        "experiment_id": exp_details.experiment_id,
        "experiment_stage": exp_details.lifecycle_stage,
        "tags": exp_details.tags,
    }

    return pd.DataFrame.from_dict(result, orient="index", columns=["parameters"])


def previous_version(model_name: str):
    """
    Return list of all previous versions.

    Args:
        model_name (str): name of the model.
    """
    filter_string = f"name='{model_name}'"
    all_versions = [
        int(dict(x)["version"]) for x in client.search_model_versions(filter_string)
    ]

    all_versions.sort()
    # previous_versions
    return list(map(lambda x: str(x), all_versions))[:-1]


# A decorator function to alter doc strings
def add_doc(value):
    def _doc(func):
        func.__doc__ = func.__doc__ + value
        return func

    return _doc


def input_validation(
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    y_train: pd.Series,
    y_test: pd.Series,
    experiment_name: str,
    multiclass: Optional[bool] = False,
    average: Optional[str] = None,
) -> None:
    """
    Args:
        X_train (pandas.DataFrame): Shape (n_samples, n_features), where n_samples is the number of samples and
            n_features is the number of features for train dataset.

        X_test (pandas.DataFrame): Shape (n_samples, n_features), where n_samples is the number of samples and
            n_features is the number of features for test dataset.

        y_train (pandas.Series): Shape (n_samples, 1), where n_samples is the number of samples for train dataset.

        y_test (pandas.Series): Shape (n_samples, 1), where n_samples is the number of samples for test dataset.

        experiment_name (str): Name of the experiment for logging.

        multiclass (Optional[bool]): True if data is multi class else False.

        average (Optional[string], [None, ``binary`` (default), ``micro``, ``macro``, ``samples``, ``weighted``]):
            This parameter is required for multiclass/multilabel targets.
            If None, the scores for each class are returned. Otherwise, this determines the type of averaging performed on the data.
    """
    if not (isinstance(X_train, (pd.Series, pd.DataFrame, np.ndarray))):
        raise TypeError(
            "X_train passed must be of type pandas.Series, pandas.DataFrame or numpy.ndarray"
        )
    if X_train.shape[0] == 0:
        raise ValueError("X_train passed must be a positive dataframe")

    if not (isinstance(X_test, (pd.Series, pd.DataFrame, np.ndarray))):
        raise TypeError(
            "X_test passed must be of type pandas.Series, pandas.DataFrame or numpy.ndarray"
        )
    if X_test.shape[0] == 0:
        raise ValueError("X_test passed must be a positive dataframe")

    if not (isinstance(y_train, (pd.Series, pd.DataFrame, np.ndarray))):
        raise TypeError(
            "y_train passed must be of type pandas.Series, pandas.DataFrame or numpy.ndarray"
        )
    if y_train.shape[0] == 0:
        raise ValueError("y_train passed must be a positive Series")

    if not (isinstance(y_test, (pd.Series, pd.DataFrame, np.ndarray))):
        raise TypeError(
            "y_test passed must be of type pandas.Series, pandas.DataFrame or numpy.ndarray"
        )
    if y_test.shape[0] == 0:
        raise ValueError("y_test passed must be a positive Series")

    if X_train.shape[0] != len(y_train):
        raise ValueError(
            "Length of Train set and its respective Target variable should be of equal length"
        )
    if X_test.shape[0] != len(y_test):
        raise ValueError(
            "Length of Test set and its respective Target variable should be of equal length"
        )

    if not isinstance(experiment_name, str):
        raise ValueError("experiment_name must be string")
    if not experiment_name:
        raise ValueError("experiment_name cannot be null or empty string")
    if multiclass and not isinstance(multiclass, bool):
        raise ValueError("multiclass must be boolean")
    if average and not isinstance(average, str):
        raise ValueError("average must be string")

    if multiclass and average not in [
        "micro",
        "macro",
        "samples",
        "weighted",
    ]:
        raise ValueError(
            f"Target is multiclass but average='{average}'. Please choose another average setting, one of ['micro', 'macro', 'samples', 'weighted']."
        )
