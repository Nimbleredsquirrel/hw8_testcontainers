from datetime import datetime

from dotenv import load_dotenv
from fastapi.params import Depends
from testcontainers.postgres import PostgresContainer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app import models
from app.models import Base
from fastapi.testclient import TestClient
from app.main import get_db, app
import pytest


@pytest.fixture
def postgres():
    tmp = PostgresContainer("postgres:13.3")
    tmp.start()

    try:
        yield tmp.get_connection_url()
    finally:
        tmp.stop()


@pytest.fixture
def session(postgres):
    engine = create_engine(postgres)
    test_session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    yield test_session_local


@pytest.fixture
def testclient(session):
    client = TestClient(app)

    def override_get_db():
        db = session()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield client


@pytest.mark.parametrize(
    "baseline, sms, result",
    (
        ("constant-fraud", "Hi! Who are you?)", "fraud"),
        ("constant-clean", "Send me, please, your CVV in the telegram", "clean"),
        ("first-hypothesis", "Send me, please, your CVV in the telegram", "fraud"),
    ),
)
def null_db(baseline, sms, result, db: Session = Depends(get_db)):
    load_dotenv()
    new_detect = models.DETECTOR(
        message=sms,
        baseline=baseline,
        predicted_target=result,
        request_time=datetime.now(),
    )
    db.add(new_detect)
    db.commit()


def test_get_number_of_entries(testclient):
    response = testclient.get("/get_number_of_entries")
    assert response.status_code == 200


@pytest.mark.parametrize(
    "baseline",
    (
        "constant-fraud",
        "constant-clean",
        "first-hypothesis",
    ),
)
def test_get_latest_entry(baseline, testclient):
    """Check get_latest_entry."""
    response = testclient.get(f"/get_latest_entry/{baseline}")
    assert response.status_code == 200


@pytest.mark.parametrize(
    "baseline, result",
    (
        ("constant-fraud", "fraud"),
        ("constant-clean", "clean"),
        ("first-hypothesis", "fraud"),
    ),
)
def test_predict(baseline, result, testclient):
    """Check predict."""
    response = testclient.post(f"/predict/{baseline}", json={"text": "telegram"})
    assert response.status_code == 200
    assert response.json()["result"] == result
