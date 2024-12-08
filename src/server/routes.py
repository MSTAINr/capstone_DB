from fastapi import APIRouter, Depends, UploadFile
from handler import post_predict_handler, predict_histories
from load_model import load_model

# Router untuk API
router = APIRouter()

# Memuat model secara global
model = None

@router.on_event("startup")
async def startup_event():
    global model
    model = await load_model()

@router.post("/predict")
async def predict(file: UploadFile, model=Depends(lambda: model)):
    return await post_predict_handler(file, model)

@router.get("/predict/histories")
async def get_histories():
    return await predict_histories()
