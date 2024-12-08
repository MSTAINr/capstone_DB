import tensorflow as tf
import numpy as np
from PIL import Image
from io import BytesIO
from input_error import InputError  # Sesuaikan dengan nama file Python

async def predict_classification(model, image_bytes):
    try:
        # Decode image
        image = Image.open(BytesIO(image_bytes)).resize((224, 224))
        tensor = tf.convert_to_tensor(np.array(image), dtype=tf.float32)
        tensor = tf.expand_dims(tensor, axis=0)  # Add batch dimension

        # Predict
        prediction = model(tensor)
        score = prediction.numpy()[0]
        confidence_score = float(np.max(score) * 100)

        print("score:", score)
        print("confidence_score:", confidence_score)

        # Tentukan label dan saran
        label = "Cancer" if confidence_score > 50 else "Non-cancer"
        suggestion = "Segera periksa ke dokter!" if label == "Cancer" else "Penyakit kanker tidak terdeteksi."

        return {
            "confidenceScore": confidence_score,
            "label": label,
            "suggestion": suggestion,
        }

    except Exception as error:
        raise InputError("Terjadi kesalahan dalam melakukan prediksi") from error
