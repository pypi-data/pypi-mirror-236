#!/usr/bin/env python
#
# Copyright (c) 2023 Katonic Pty Ltd. All rights reserved.
#
import uuid
from datetime import datetime
from typing import Any
from typing import Dict
from typing import Optional

import kfp
from kfp import auth
from kfp import aws
from kfp import azure
from kfp import cli
from kfp import Client
from kfp import compiler
from kfp import components
from kfp import containers
from kfp import dsl
from kfp import gcp
from kfp import LocalClient
from kfp import notebook
from kfp import onprem
from kfp import pipeline_spec
from kfp import run_pipeline_func_locally
from kfp import run_pipeline_func_on_cluster
from kfp import v2
from kfp.components import ComponentStore
from kfp.components import create_component_from_airflow_op
from kfp.components import create_component_from_func
from kfp.components import create_component_from_func_v2
from kfp.components import create_graph_component_from_pipeline_func
from kfp.components import func_to_component_text
from kfp.components import func_to_container_op
from kfp.components import InputArtifact
from kfp.components import InputBinaryFile
from kfp.components import InputPath
from kfp.components import InputTextFile
from kfp.components import load_component
from kfp.components import load_component_from_file
from kfp.components import load_component_from_text
from kfp.components import load_component_from_url
from kfp.components import modelbase
from kfp.components import OutputArtifact
from kfp.components import OutputBinaryFile
from kfp.components import OutputPath
from kfp.components import OutputTextFile
from kfp.components import structures
from kfp.components import type_annotation_utils
from kfp.components import type_annotation_utils_test
from kfp.v2.dsl import Artifact
from kfp.v2.dsl import ClassificationMetrics
from kfp.v2.dsl import component
from kfp.v2.dsl import Condition
from kfp.v2.dsl import ContainerOp
from kfp.v2.dsl import Dataset
from kfp.v2.dsl import ExitHandler
from kfp.v2.dsl import graph_component
from kfp.v2.dsl import HTML
from kfp.v2.dsl import importer
from kfp.v2.dsl import InputPath  # noqa: F811
from kfp.v2.dsl import Markdown
from kfp.v2.dsl import Metrics
from kfp.v2.dsl import Model
from kfp.v2.dsl import OutputPath  # noqa: F811
from kfp.v2.dsl import ParallelFor
from kfp.v2.dsl import pipeline
from kfp.v2.dsl import SlicedClassificationMetrics

__all__ = [
    "dsl",
    "auth",
    "aws",
    "azure",
    "cli",
    "compiler",
    "components",
    "containers",
    "Client",
    "LocalClient",
    "gcp",
    "notebook",
    "onprem",
    "pipeline_spec",
    "run_pipeline_func_on_cluster",
    "run_pipeline_func_on_cluster",
    "run_pipeline_func_locally",
    "v2",
    "type_annotation_utils",
    "InputArtifact",
    "type_annotation_utils_test",
    "OutputArtifact",
    "InputBinaryFile",
    "OutputBinaryFile",
    "ComponentStore",
    "InputTextFile",
    "OutputTextFile",
    "InputPath",
    "modelbase",
    "OutputPath",
    "structures",
    "create_graph_component_from_pipeline_func",
    "create_component_from_func",
    "create_component_from_airflow_op",
    "create_component_from_func_v2",
    "load_component",
    "load_component_from_file",
    "load_component_from_text",
    "load_component_from_url",
    "func_to_component_text",
    "func_to_container_op",
    "Artifact",
    "ClassificationMetrics",
    "Condition",
    "ContainerOp",
    "SlicedClassificationMetrics",
    "Dataset",
    "ExitHandler",
    "ParallelFor",
    "HTML",
    "InputPath",
    "Markdown",
    "Metrics",
    "Model",
    "OutputPath",
    "graph_component",
    "importer",
    "pipeline",
    "component",
]


class Pipeline:
    def __init__(self, pipeline_name: Any):
        """
        Pipeline class to compile, run pipelines and create experiments.

        Args:
            pipelne_name (Any): Pipeline function definition
        """
        self.pipeline_name = pipeline_name

    def compile_pipeline(self):
        """
        DSL Compiler that compiles pipeline functions into workflow yaml.
        """
        try:
            self.pipeline_filename = (
                f"{self.pipeline_name.__name__}{uuid.uuid1()}.pipeline.yaml"
            )
            kfp.compiler.Compiler().compile(self.pipeline_name, self.pipeline_filename)
        except BaseException as e:
            print(e)

    def create_experiment(self, exp_name: str):
        """
        Create a new experiment and Uploads the pipeline to the Kubeflow Pipelines cluster.

        Args:
            exp_name (str): The name of the experiment
        """
        try:
            self.client = kfp.Client()
            self.experiment = self.client.create_experiment(exp_name)
            self.client.upload_pipeline(self.pipeline_filename)
        except BaseException as e:
            print(e)

    def run_pipeline(self, arguments: Optional[Dict[str, str]] = None):
        """
        Run a specified pipeline.

        Args:
            arguments (dict): A dictionary with key (string) as argument name and value (string) as as argument value.
        """
        if arguments is None:
            arguments = {}
        try:
            run_name = self.pipeline_name.__name__ + str(
                datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
            )
            self.client.run_pipeline(
                self.experiment.id, run_name, self.pipeline_filename, arguments
            )
        except BaseException as e:
            print(e)
