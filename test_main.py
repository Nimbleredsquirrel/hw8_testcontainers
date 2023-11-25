"""Tests from all function."""

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_hello():
    """Check root enter."""
    response = client.get("/")
    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]
    assert response.json()["message"] == "Hello!This is the fraud detector."


@pytest.mark.parametrize(
    "error_type, result",
    (
        ("false-positive", 10000),
        ("false-negative", 75000),
    ),
)
def test_get_error_cost(error_type, result):
    """Check get_error_cost."""
    response = client.get(f"/cost/{error_type}")
    assert response.status_code == 200
    assert response.json()["error_cost"] == result


@pytest.mark.parametrize(
    "baseline, result",
    (
        ("constant-fraud", 1900000000),
        ("constant-clean", 750000000),
        ("first-hypothesis", 558050000),
    ),
)
def test_get_estimate(baseline, result):
    """Check get_estimate."""
    response = client.get(f"/loss/{baseline}")
    assert response.status_code == 200
    assert response.json()["estimate"] == result


@pytest.mark.parametrize(
    "baseline, result",
    (
        ("constant-fraud", "fraud"),
        ("constant-clean", "clean"),
        ("first-hypothesis", "fraud"),
    ),
)
def test_predict(baseline, result):
    """Check predict."""
    response = client.post(f"/predict/{baseline}", json={"text": "telegram"})
    assert response.status_code == 200
    assert response.json()["result"] == result


@pytest.mark.parametrize(
    "baseline",
    (
        "constant-fraud",
        "constant-clean",
        "first-hypothesis",
    ),
)
def test_get_latest_entry(baseline):
    """Check get_latest_entry."""
    response = client.get(f"/get_latest_entry/{baseline}")
    assert response.status_code == 200


def test_get_number_of_entries():
    """Check get_number_of_entries."""
    response = client.get("/get_number_of_entries")
    assert response.status_code == 200
