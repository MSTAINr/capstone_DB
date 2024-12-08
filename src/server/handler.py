import uuid
from datetime import datetime
from fastapi import HTTPException, UploadFile
from inference_service import predict_classification
from store_data import store_data
from google.cloud import firestore

async def post_predict_handler(file: UploadFile, model):
    try:
        # Membaca gambar dari file upload
        image_bytes = await file.read()
        
        # Prediksi menggunakan model
        prediction = await predict_classification(model, image_bytes)
        confidence_score = prediction["confidenceScore"]
        label = prediction["label"]
        suggestion = prediction["suggestion"]

        # Membuat data hasil prediksi
        id = str(uuid.uuid4())
        created_at = datetime.utcnow().isoformat()

        data = {
            "id": id,
            "result": label,
            "suggestion": suggestion,
            "createdAt": created_at,
        }

        # Simpan data ke Firestore (opsional, aktifkan jika diperlukan)
        await store_data(id, data)

        return {
            "status": "success",
            "message": "Model is predicted successfully",
            "data": data,
        }

    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

async def predict_histories():
    try:
        # Inisialisasi Firestore
        # ganti project id
        db = firestore.Client(project="project_id")
        predict_collection = db.collection("predictions")
        snapshot = predict_collection.stream()

        # Membaca data dari Firestore
        result = []
        for doc in snapshot:
            data = doc.to_dict()
            result.append({
                "id": doc.id,
                "history": {
                    "result": data.get("result"),
                    "createdAt": data.get("createdAt"),
                    "suggestion": data.get("suggestion"),
                    "id": data.get("id"),
                },
            })

        return {
            "status": "success",
            "data": result,
        }

    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
