"""This is the fraud detector."""
from datetime import datetime
from typing import Any

from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from sqlalchemy import func
from sqlalchemy.orm import Session

from . import models, schemas
from .database import SessionLocal, engine
from .model_predict import tree_count

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
    """Hello message."""
    return {"message": "Hello!This is an information application about trees."}


@app.post("/information")
async def post_information(
    buff: schemas.InputFeatures, db: Session = Depends(get_db)
) -> int | Any:
    """Get info."""
    load_dotenv()
    info = tree_count(buff.place, buff.year)
    new_detect = models.Trees(
        place=buff.place,
        year=buff.year,
        amount=info,
        request_time=datetime.now(),
    )
    db.add(new_detect)
    db.commit()
    return info


@app.get("/get_most_popular")
async def get_most_popular(db: Session = Depends(get_db)):
    """Get most popular place."""
    return (
        db.query(models.Trees)  # type: ignore
        .group_by(models.Trees.place)
        .order_by(func.count(models.Trees.place).desc())  # pylint: disable=E1102
        .first()
        .place
    )
