from fastapi import Depends, FastAPI, APIRouter

from src.models import PredictParams

__all__ = ["app"]

if __name__ == "__main__":
    print("Do not run this file directly. Use 'python .' instead.")
    exit(1)

app = FastAPI(
    title="AyataAI - API",
    docs_url="/",
)

router = APIRouter(
    prefix="/api",
    tags=["API"]
)


@router.post("/predict")
def predict(params: PredictParams = Depends()):
    return {"query": params.query}

app.include_router(router)
