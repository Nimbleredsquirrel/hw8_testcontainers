"""This is the fraud detector."""
from datetime import datetime
from typing import Any

from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from . import models, schemas
from .database import SessionLocal, engine
from .model_estimate import estimate
from .model_predict import Func

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


def get_db():
    """Give database."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    """Get welcome message."""
    return {"message": "Hello!This is the fraud detector."}


@app.get("/cost/{error_type}")
async def get_error_cost(error_type: schemas.ErrorType):
    """Get error_cost."""
    return {"error_cost": schemas.N[error_type.name]}


@app.get("/loss/{baseline}")
async def get_estimate(baseline: schemas.Baseline):
    """Get estimate."""
    return {"estimate": estimate(Func[baseline.name])}


@app.post("/predict/{baseline}")
async def post_predict(
    baseline: schemas.Baseline,
    buff: schemas.InputFeatures,
    db: Session = Depends(get_db),
) -> dict[str, str] | Any:
    """Get predict."""
    load_dotenv()
    prediction = Func[baseline.name](buff.text)
    new_detect = models.DETECTOR(
        message=buff.text,
        baseline=baseline,
        predicted_target=prediction.result,
        request_time=datetime.now(),
    )
    db.add(new_detect)
    db.commit()
    return prediction


@app.get("/get_latest_entry/{baseline}")
async def get_latest_entry(baseline: schemas.Baseline, db: Session = Depends(get_db)):
    """Get latest entry from this baseline."""
    return (
        db.query(models.DETECTOR)
        .filter(models.DETECTOR.baseline == baseline)
        .order_by(models.DETECTOR.request_time.desc())
        .first()
    )


@app.get("/get_number_of_entries")
async def get_number_of_entries(db: Session = Depends(get_db)):
    """Get number of entries."""
    return {
        schemas.Baseline.CONSTANT_CLEAN: db.query(models.DETECTOR)
        .filter(models.DETECTOR.baseline == schemas.Baseline.CONSTANT_CLEAN)
        .count(),
        schemas.Baseline.CONSTANT_FRAUD: db.query(models.DETECTOR)
        .filter(models.DETECTOR.baseline == schemas.Baseline.CONSTANT_FRAUD)
        .count(),
        schemas.Baseline.FIRST_HYPOTHESIS: db.query(models.DETECTOR)
        .filter(models.DETECTOR.baseline == schemas.Baseline.FIRST_HYPOTHESIS)
        .count(),
    }
