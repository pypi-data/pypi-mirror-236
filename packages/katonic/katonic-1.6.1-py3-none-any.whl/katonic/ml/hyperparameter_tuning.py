#!/usr/bin/env python
#
# Copyright (c) 2023 Katonic Pty Ltd. All rights reserved.
#
import logging
import os
import traceback
import warnings
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

import mlflow.sklearn
import numpy as np
import optuna
import pandas as pd
from katonic.ml.client import MLClient
from optuna.visualization import plot_parallel_coordinate
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import log_loss
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import precision_score
from sklearn.metrics import r2_score
from sklearn.metrics import recall_score
from sklearn.metrics import roc_auc_score


mlflow.set_tracking_uri(os.environ["MLFLOW_BASE_URL"])
client = mlflow.tracking.MlflowClient(os.environ["MLFLOW_BASE_URL"])
logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)

warnings.filterwarnings("ignore")


class HyperParameterTune(MLClient):
    def __init__(
        self,
        X_train: pd.DataFrame,
        X_test: pd.DataFrame,
        y_train: pd.Series,
        y_test: pd.Series,
        params: Dict[Any, Any],
        experiment_name: str,
        source_name: str,
        features: List[str],
        username: str = "default",
        artifacts: Optional[Dict[str, str]] = None,
        multiclass: bool = False,
        average: str = "binary",
        problem: str = "",
    ):
        """
        A HyperParameterTune Object is used to define, create a Tuning experiment.

        Args:
            X_train (pandas.DataFrame): Shape (n_samples, n_features), where n_samples is the number of samples and
                n_features is the number of features for train dataset.

            X_test (pandas.DataFrame): Shape (n_samples, n_features), where n_samples is the number of samples and
                n_features is the number of features for test dataset.

            y_train (pandas.Series): Shape (n_samples, 1), where n_samples is the number of samples for train dataset.

            y_test (pandas.Series): Shape (n_samples, 1), where n_samples is the number of samples for test dataset.

            params (Dict): The model parameters to be tuned on.

            experiment_name (str): Name of the experiment for logging.

            source_name (str): Name/path of the current notebook or script.

            features (List[str]): List of features(str) of the current experiment/modelling.

            artifacts (Optional[Dict[str, str]]): Optional artifacts as dict e.g. dataset path or images folder of the current experiment.

            multiclass (bool): True if data is multi class else False.

            average (string, [None, ``binary`` (default), ``micro``, ``macro``, ``samples``, ``weighted``]):
                This parameter is required for multiclass/multilabel targets. If None, the scores for each class are returned.
                Otherwise, this determines the type of averaging performed on the data.

            problem (str): This parameter requires to specify the type of problem (``classification`` or ``regression``) is being solved.
        """
        super().__init__(experiment_name, source_name, features, username, artifacts)

        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test
        self.params = params
        self.multiclass = multiclass
        self.average = average
        self.model = None
        self.problem = problem.strip()
        self.source_name = source_name
        self.features = features
        self.artifact_paths = artifacts or {}
        logger.info("HyperParameterTune successfully instantiated")

    def eval_metrics_classification(self, actual, pred):
        """
        Calculates various evaluation parameters like accuracy_score, roc_auc_score, log_loss, recall_score, f1_score, precision_score
        for classification problem.

        Args:
            actual (Any): actual ``y`` value (e.g. pandas.Series or pandas.DataFrame, or numpy array)
            pred (Any): predicted ``y`` value (e.g. pandas.Series or pandas.DataFrame, or numpy array)

        Returns:
            acc_score: Accuracy score
            auc_roc: roc auc Score
            log_los: log_loss
            recall: recall
            f1_scr: F1 Score
            precision_scr: precision Score
        """
        logger.info("Calculating evaluation paramaters")

        acc_score, auc_roc, log_los, recall, f1_scr, precision_scr = (
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        )

        try:
            acc_score = accuracy_score(actual, pred)
        except Exception:
            logger.error("accuracy_score calcuation raised an exception:")
            logger.error(traceback.format_exc())
        try:
            recall = recall_score(actual, pred, average=self.average)
        except Exception:
            logger.error("recall_score calcuation raised an exception:")
            logger.error(traceback.format_exc())
        try:
            precision_scr = precision_score(actual, pred, average=self.average)
        except Exception:
            logger.error("precision_score calcuation raised an exception:")
            logger.error(traceback.format_exc())
        try:
            f1_scr = f1_score(actual, pred, average=self.average)
        except Exception:
            logger.error("f1_score calcuation raised an exception:")
            logger.error(traceback.format_exc())

        if self.multiclass:
            return acc_score, recall, f1_scr, precision_scr
        try:
            auc_roc = roc_auc_score(actual, pred)
        except Exception:
            logger.error("roc_auc_score calcuation raised an exception:")
            logger.error(traceback.format_exc())
        try:
            log_los = log_loss(actual, pred)
        except Exception:
            logger.error("log_loss calcuation raised an exception:")
            logger.error(traceback.format_exc())

        return acc_score, auc_roc, log_los, recall, f1_scr, precision_scr

    def model_fit_log_classification(self, params: Dict[Any, Any]) -> Any:
        """
        Performs the model fitting and model prediction task. It calls the evaluation metrics function and logs the required metrics for the model.

        Args:
            params (dict): Hyperparameters used for tuning model.
        """
        logger.info(f"Training the model {self.run_name}")
        try:
            self.model = self.model_name(**params)
            self.model.fit(self.X_train, self.y_train)  # type: ignore
        except Exception:
            logger.error(f"Fitting the model {self.model} raised an exception:")
            logger.error(traceback.format_exc())

        logger.info("Performing the prediction")

        y_pred = self.model.predict(self.X_test)  # type: ignore

        if self.multiclass:

            (
                acc_score,
                recall,
                f1_scr,
                precision_scr,
            ) = self.eval_metrics_classification(self.y_test, y_pred)
            metrics = {
                "accuracy_score": acc_score,
                "recall": recall,
                "f1_score": f1_scr,
                "precision_score": precision_scr,
            }
        else:
            (
                acc_score,
                auc_roc,
                log_los,
                recall,
                f1_scr,
                precision_scr,
            ) = self.eval_metrics_classification(self.y_test, y_pred)
            metrics = {
                "accuracy_score": acc_score,
                "roc_auc_score": auc_roc,
                "log_loss": log_los,
                "recall": recall,
                "f1_score": f1_scr,
                "precision_score": precision_scr,
            }

        logger.info(f"logged params: {metrics.keys()}")
        try:
            mlflow.log_metrics(metrics)
        except Exception:
            logger.warning("Couldn't perform log_metrics. Exception:")
            logger.warning(traceback.format_exc())

        logger.info("Logging params")
        try:
            for i in params:
                mlflow.log_param(i, params[i])
        except Exception:
            logger.warning("Couldn't perform logging params. Exception:")
            logger.warning(traceback.format_exc())

        logger.info(f"log model {self.run_name}")
        try:
            mlflow.sklearn.log_model(self.model, self.run_name)
        except Exception:
            logger.warning("Couldn't log model. Exception:")
            logger.warning(traceback.format_exc())

        return acc_score if self.multiclass else auc_roc

    def eval_metrics_regression(self, actual, pred) -> Tuple[Any, Any, Any, Any, float]:
        """
        Calculates various evaluation parameters like mse, rmse, mae rmsle for regression problem.

        Args:
            actual (Any): actual testing data (e.g. pandas.Series or pandas.DataFrame, or numpy array)
            pred (Any): predicted testing data (e.g. pandas.Series or pandas.DataFrame, or numpy array)

        Returns:
           mse: mean square error
           rmse: root mean square error
           rmsle: root mean square log error
           mae: mean absolute error
           r2: r2 score
        """
        logger.info("Calculating evaluation paramaters")

        mse, rmse, rmsle, mae, r2 = 0.0, 0.0, 0.0, 0.0, 0.0

        try:
            mse = mean_squared_error(actual, pred)
        except Exception:
            logger.error("mean_squared_error calcuation raised an exception:")
            logger.error(traceback.format_exc())
        try:
            rmse = np.sqrt(mse)
        except Exception:
            logger.error("root_mean_squared_error calcuation raised an exception:")
            logger.error(traceback.format_exc())
        try:
            rmsle = np.log(rmse)
        except Exception:
            logger.error("root_mean_squared_log_error calcuation raised an exception:")
            logger.error(traceback.format_exc())
        try:
            mae = mean_absolute_error(actual, pred)
        except Exception:
            logger.error("mean_absolute_error calcuation raised an exception:")
            logger.error(traceback.format_exc())
        try:
            r2 = r2_score(actual, pred)
        except Exception:
            logger.error("r2 score calcuation raised an exception:")
            logger.error(traceback.format_exc())

        return mse, rmse, rmsle, mae, r2

    def model_fit_log_regression(self, params: Dict[Any, Any]) -> float:
        """
        Performs the model fitting and model prediction task. It calls the evaluation metrics function and logs the required metrics for the model.

        Args:
            params (Dict): The model parameters to be tuned on.
        """
        logger.info("Training the model")
        try:
            self.model = self.model_name(**params)
            self.model.fit(self.X_train, self.y_train)  # type: ignore
        except Exception:
            logger.error(f"Fitting the model {self.run_name} raised an exception:")
            logger.error(traceback.format_exc())

        logger.info("Performing the prediction")

        y_pred = self.model.predict(self.X_test)  # type: ignore
        (mse, rmse, rmsle, mae, r2) = self.eval_metrics_regression(self.y_test, y_pred)

        metrics = {"MSE": mse, "RMSE": rmse, "RMSLE": rmsle, "MAE": mae, "R2": r2}

        logger.info(f"logged params: {metrics.keys()}")
        try:
            mlflow.log_metrics(metrics)
        except Exception:
            logger.warning("Couldn't log metrics. Exception:")
            logger.warning(traceback.format_exc())

        logger.info("Logging params")
        try:
            for i in params:
                mlflow.log_param(i, params[i])
        except Exception:
            logger.warning("Couldn't perform logging params. Exception:")
            logger.warning(traceback.format_exc())

        logger.info(f"logging model {self.run_name}")
        try:
            mlflow.sklearn.log_model(self.model, self.run_name)
        except Exception:
            logger.warning("Couldn't log model. Exception:")
            logger.warning(traceback.format_exc())
        return r2

    def generate_hyperparameter(self, trial):
        params = {}
        logger.info("Starting hyperparameter generation..")
        try:
            for k, v in self.params.items():
                if isinstance(v, dict):
                    types = v["type"]
                    if "low" in v and "high" in v:
                        low = v["low"]
                        high = v["high"]

                    if types == "categorical":
                        value = v["values"]
                        params[k] = trial.suggest_categorical(k, value)
                    elif types == "discrete_uniform":
                        if "q" in v:
                            step = v["q"]
                        params[k] = trial.suggest_discrete_uniform(k, low, high, 0.1)

                    elif types == "float":
                        step = 0.1
                        if "step" in v:
                            step = v["step"]
                        log = False
                        if "log" in v:
                            log = v["log"]
                            if log:
                                step = None  # type: ignore
                        params[k] = trial.suggest_float(
                            k, low, high, step=step, log=log
                        )
                    elif types == "int":
                        step = 1
                        if "step" in v:
                            step = v["step"]
                        params[k] = trial.suggest_int(k, low, high, step)
                    elif types == "loguniform":
                        params[k] = trial.suggest_loguniform(k, low, high)
                    elif types == "uniform":
                        params[k] = trial.suggest_uniform(k, low, high)
                elif isinstance(v, int):
                    params[k] = trial.suggest_int(k, v, v)
                elif isinstance(v, float):
                    params[k] = trial.suggest_float(k, v, v)
                elif isinstance(v, str):
                    params[k] = trial.suggest_categorical(k, [v])
                elif isinstance(v, List):
                    params[k] = trial.suggest_categorical(k, v)
            return params
        except Exception:
            logger.warning("Couldn't generate hyperparameters. Exception:")
            logger.warning(traceback.format_exc())

    def objective(self, trial):

        with mlflow.start_run(run_name=self.run_name, nested=True) as run:
            self.set_model_tags(run.info.run_uuid)
            params = self.generate_hyperparameter(trial)
            if self.problem == "classification":
                value = self.model_fit_log_classification(params)
            elif self.problem == "regression":
                value = self.model_fit_log_regression(params)
            return value

    def print_study(self, study):
        """
        This method takes the study object and prints and plots the best result and parameters

        Args:
            study: create_study object of optuna
        """
        logger.info("Printing results for hyperparameter tuning.")
        try:
            print("Number of finished trials: ", len(study.trials))
            print("Best trial:")
            trial = study.best_trial
            if self.problem == "classification":
                value = "accuracy score" if self.multiclass else "auc_roc_score"
            else:
                value = "R2"
            print(f"  {value}: ", trial.value)
            print("  Params: ")
            for key, value in trial.params.items():
                print(f"    {key}: {value}")
            fig = plot_parallel_coordinate(study)
            fig.show(renderer="iframe")
        except Exception:
            logger.warning("Couldn't print hyperparameter tuning results. Exception:")
            logger.warning(traceback.format_exc())

    def tune(self, model, run_name: str, n_trials: int):
        """
        The method initates the hyperparameter tuning process

        Args:
            model: model that needs to used for tuning
            run_name (str): MLFlow run name
            n_trials (int): number of iterations to run the tuning
        """
        self.run_name = run_name
        self.model_name = model
        try:
            study = optuna.create_study(direction="maximize")
            study.optimize(self.objective, n_trials=n_trials)
            self.print_study(study)
        except Exception:
            logger.warning("Couldn't start hyperparameter optimization. Exception:")
            logger.warning(traceback.format_exc())
