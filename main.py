import logging

import httpx
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from src.config import AI_SERVER_HOST
from src.models import PredictParams

app = FastAPI(
    title="Teknofest - AyataAI API",
    docs_url="/",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(message)s",
    handlers=[logging.FileHandler("logs.log", encoding="utf-8"), logging.StreamHandler()],
)


@app.post("/predict")
def predict(params: PredictParams = Depends()):
    data: dict = httpx.get(AI_SERVER_HOST, params={"query": params.text}, timeout=30).json()
    print(data)
    entities: list = data["response"]["entity_list"]
    for i in data["response"]["results"]:
        entity: dict = i["entity"]
        if not entity in entities:
            entities.append(entity)

    data["response"]["entity_list"] = entities

    logger.info(f"Request: {params.text} | Response: {data['response']}")
    return ORJSONResponse(content=data["response"])
