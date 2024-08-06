from fastapi import Depends, FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from src.models import PredictParams

if __name__ == "__main__":
    print("Do not run this file directly. Use 'python .' instead.")
    exit(1)

app = FastAPI(
    title="AyataAI - API",
    docs_url="/",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter(
    prefix="/api",
    tags=["API"]
)

@router.post("/predict")
def predict(params: PredictParams = Depends()):
    return {"query": params.query}

app.include_router(router)
