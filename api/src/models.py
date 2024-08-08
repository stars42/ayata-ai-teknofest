from fastapi import Query
from pydantic import BaseModel

from src.config import MAX_CHARACTER_LENGTH


class PredictParams(BaseModel):
    query: str = Query(
        ...,
        title="Query",
        description="The query to predict",
        max_length=MAX_CHARACTER_LENGTH
    )
