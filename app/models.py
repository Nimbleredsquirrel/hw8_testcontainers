"""This program create template from database."""

from sqlalchemy import Column, DateTime, Integer, String

from .database import Base


class Trees(Base):  # pylint: disable=R0903
    """Template from database."""

    __tablename__ = "Trees"

    id = Column(Integer, primary_key=True)
    place = Column(String, default="")
    year = Column(String, default="")
    amount = Column(String, default="")
    request_time = Column(DateTime)
