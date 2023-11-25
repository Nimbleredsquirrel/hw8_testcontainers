"""Estimate function and auxiliary."""


import json
from typing import Callable

import numpy as np  # pylint: disable=E0401
import pandas as pd  # pylint: disable=E0401

from .schemas import ModelPrediction, N, PathTo


def database():
    """Get dataframe from test data."""
    path_to_fraud = PathTo["fraud"]
    path_to_clean = PathTo["clean"]
    with open(path_to_fraud, "r", encoding="utf-8") as handler:
        fraud_messages = json.load(handler)
    with open(path_to_clean, "r", encoding="utf-8") as handler:
        clean_messages = json.load(handler)
    df_fraud = pd.DataFrame({"text": fraud_messages, "target": "fraud"})
    df_clean = pd.DataFrame({"text": clean_messages, "target": "clean"})
    df = pd.concat([df_fraud, df_clean]).reset_index(drop=True)
    return df


def fpr(y_predict, y_true):
    """Get false-positive ratio."""
    fp = np.sum(
        np.where((np.array(y_predict) == "fraud") & (np.array(y_true) == "clean"))
    )
    all_n = np.sum(np.where(np.array(y_true) == "clean"))
    return round(fp / all_n, 3)


def fnr(y_predict, y_true):
    """Get false-negative ratio."""
    fn = np.sum(
        np.where((np.array(y_predict) == "clean") & (np.array(y_true) == "fraud"))
    )
    all_p = np.sum(np.where(np.array(y_true) == "fraud"))
    return round(fn / all_p, 3)


def estimate(rule: Callable[[str], ModelPrediction]) -> float:
    """Get estimate of loss with this role."""
    df = database()
    result = []
    for i in df.text:
        result.append(rule(i).result)
    return (
        fpr(result, df.target) * N.FPC * N.DP * (1 - N.FS)
        + fnr(result, df.target) * N.FNC * N.DP * N.FS
    )
