from fastapi import Query
from pydantic import BaseModel


class PredictParams(BaseModel):
    query: str = Query(
        ...,
        title="Query",
        description="The query to predict"
    )
