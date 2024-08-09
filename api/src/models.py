from fastapi import Query
from pydantic import BaseModel, Field

from src.config import MAX_CHARACTER_LENGTH


class PredictParams(BaseModel):
    text: str = Field(
        ...,
        title="Query",
        description="Query to predict sentiment for.",
        max_length=MAX_CHARACTER_LENGTH
    )
