import tensorflow as tf

def load_model():
    """
    Load a TensorFlow model from a given URL.

    Returns:
        tf.keras.Model: The loaded TensorFlow model.
    """
    try:
        model_url = 'https://storage.googleapis.com/path_model'
        model = tf.keras.models.load_model(model_url)
        print("Model loaded successfully.")
        return model
    except Exception as e:
        print(f"An error occurred while loading the model: {e}")
        return None

