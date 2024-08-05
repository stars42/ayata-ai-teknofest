from typing import Dict
from pydantic import BaseModel


class PredictParams(BaseModel):
    query: str
