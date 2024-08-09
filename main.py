import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from src.models import PredictParams

from ai_models.api_response import predict

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
def _predict(params: PredictParams):
    data = predict(params.text)
    logger.info(f"Request: {params.text} | Response: {data}")
    return ORJSONResponse(content= data)
