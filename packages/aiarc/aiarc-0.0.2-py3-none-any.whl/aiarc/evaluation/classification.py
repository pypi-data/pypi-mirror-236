"""
Evaulation object for classification
"""
from typing import Type

import torch
from aiarc.evaluation.base import Evaluation
from aiarc.loader.load_data import DatasetObject


class ClassificationEvaluation(Evaluation):
    def __repr__(self) -> str:
        return "Classification Evaluation Object"
