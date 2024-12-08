import tensorflow as tf

async def load_model():
    try:
        model_url = "https://storage.googleapis.com/payl_model"
        model = tf.keras.models.load_model(model_url)  # Ganti sesuai format model jika tidak .h5
        return model
    except Exception as error:
        raise RuntimeError("Gagal memuat model") from error
