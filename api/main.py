from fastapi import APIRouter, Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from src.models import PredictParams

app = FastAPI(
    title="AyataAI - API",
    docs_url="/",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["*"],
)

router = APIRouter(prefix="/api", tags=["API"])


@router.post("/predict")
def predict(params: PredictParams = Depends()):
    # TODO - Buraya AI ile ilgili işlemler gelecek
    return {"query": params.query}


app.include_router(router, default_response_class=ORJSONResponse)

__all__ = ["app"]
