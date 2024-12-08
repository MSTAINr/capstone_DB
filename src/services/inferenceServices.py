import tensorflow as tf
import numpy as np

class InputError(Exception):
    """Custom exception for input errors."""
    def __init__(self, message):
        super().__init__(message)

def predict_classification(model, image):
    """
    Perform classification prediction on an image using a TensorFlow model.

    Args:
        model (tf.keras.Model): The loaded TensorFlow model.
        image (bytes): The image data in bytes.

    Returns:
        dict: A dictionary containing the confidence score, label, and suggestion.
    """
    try:
        # Decode and preprocess the image
        tensor = tf.image.decode_image(image, channels=3)  # Ensure 3 color channels (RGB)
        tensor = tf.image.resize(tensor, [224, 224])      # Resize to 224x224
        tensor = tf.expand_dims(tensor, axis=0)           # Add batch dimension
        tensor = tf.cast(tensor, tf.float32) / 255.0      # Normalize to [0, 1]

        # Perform prediction
        prediction = model(tensor)
        score = prediction.numpy()[0]
        confidence_score = max(score) * 100

        print("score:", score)
        print("confidenceScore:", confidence_score)

        # Determine label and suggestion
        label = "Cancer" if confidence_score > 50 else "Non-cancer"

        suggestion = (
            "Segera periksa ke dokter!" if label == "Cancer" 
            else "Penyakit kanker tidak terdeteksi."
        )

        return {
            "confidenceScore": confidence_score,
            "label": label,
            "suggestion": suggestion,
        }
    except Exception as e:
        raise InputError("Terjadi kesalahan dalam melakukan prediksi") from e