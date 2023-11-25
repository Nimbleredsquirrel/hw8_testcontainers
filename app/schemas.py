"""All schemas."""


import os
import pathlib
from enum import Enum
from typing import Literal

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class N(float, Enum):
    """Constants."""

    FPC = float(str(os.getenv("FPC")))
    FNC = float(str(os.getenv("FNC")))
    DP = float(str(os.getenv("DP")))
    FS = float(str(os.getenv("FS")))


class ErrorType(str, Enum):
    """Two error types."""

    FPC = "false-positive"
    FNC = "false-negative"


class Baseline(str, Enum):
    """Baseline."""

    CONSTANT_FRAUD = "constant-fraud"
    CONSTANT_CLEAN = "constant-clean"
    FIRST_HYPOTHESIS = "first-hypothesis"


class ModelPrediction(BaseModel):
    """Two types if predictions."""

    result: Literal["clean", "fraud"]


class InputFeatures(BaseModel):
    """Input features."""

    text: str = ""


PathTo = {
    "clean": pathlib.Path(str(os.getenv("CLEAN_DATA"))),
    "fraud": pathlib.Path(str(os.getenv("FRAUD_DATA"))),
}
