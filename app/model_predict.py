"""Model predictions."""


from re import search

from .schemas import ModelPrediction


def constant_fraud(message: str) -> ModelPrediction:
    """Return fraud."""
    if len(message) > 0:
        result = ModelPrediction(result="fraud")
    else:
        result = ModelPrediction(result="fraud")
    return result


def constant_clean(message: str) -> ModelPrediction:
    """Return clean."""
    if message:
        result = ModelPrediction(result="clean")
    else:
        result = ModelPrediction(result="clean")
    return result


def first_hypothesis(message: str) -> ModelPrediction:
    """Return prediction based on rule."""
    if search(r"[ТтTt][^\s]*[ЛлLl][^\s]*[ГгGg][^\s]*", message) or search(
        r"[^\s]*[Тт][^\s]*[Мм][^\s]*[^\s]*[Нн][^\s]*", message
    ):
        result = ModelPrediction(result="fraud")
    else:
        result = ModelPrediction(result="clean")
    return result


Func = {
    "CONSTANT_FRAUD": constant_fraud,
    "CONSTANT_CLEAN": constant_clean,
    "FIRST_HYPOTHESIS": first_hypothesis,
}
