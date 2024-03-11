"""All schemas."""


from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class InputFeatures(BaseModel):
    """Input features."""

    place: str = ""
    year: str = ""
