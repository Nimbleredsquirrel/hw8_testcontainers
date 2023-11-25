"""This program create template from database."""

from sqlalchemy import Column, DateTime, Integer, String

from .database import Base


class DETECTOR(Base):  # pylint: disable=R0903
    """Template from database."""

    __tablename__ = "flowers"

    id = Column(Integer, primary_key=True)
    message = Column(String, default="")
    baseline = Column(String, default="constant-clean")
    predicted_target = Column(Integer)
    request_time = Column(DateTime)
