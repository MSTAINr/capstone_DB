import uuid
from datetime import datetime
from flask import Flask, request, jsonify
from google.cloud import firestore
from predict_classification import predict_classification  # Assume this is your predict function

app = Flask(__name__)

# Initialize Firestore client
db = firestore.Client(project="project_id")

@app.route('/predict', methods=['POST'])
def post_predict_handler():
    """
    Handle prediction request and store the result in Firestore.
    """
    try:
        # Extract image from request payload
        image = request.files['image'].read()

        # Load model from app context (assume it is loaded on app startup)
        model = app.config['MODEL']

        # Perform prediction
        prediction_result = predict_classification(model, image)
        confidence_score = prediction_result['confidenceScore']
        label = prediction_result['label']
        suggestion = prediction_result['suggestion']

        # Generate unique ID and timestamp
        prediction_id = str(uuid.uuid4())
        created_at = datetime.utcnow().isoformat()

        # Prepare data for Firestore
        data = {
            "id": prediction_id,
            "result": label,
            "suggestion": suggestion,
            "createdAt": created_at,
        }

        # Store data in Firestore
        # Uncomment below to enable storing predictions
        # db.collection("predictions").document(prediction_id).set(data)

        # Respond with prediction result
        return jsonify({
            "status": "success",
            "message": "Model is predicted successfully",
            "data": data
        }), 201
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Prediction failed: {str(e)}"
        }), 500

@app.route('/histories', methods=['GET'])
def predict_histories():
    """
    Retrieve prediction history from Firestore.
    """
    try:
        # Fetch all documents from the "predictions" collection
        predict_collection = db.collection("predictions")
        snapshot = predict_collection.get()

        # Format the response
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

        # Respond with the history
        return jsonify({
            "status": "success",
            "data": result
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Failed to retrieve histories: {str(e)}"
        }), 500

if __name__ == "__main__":
    # Load your TensorFlow model into Flask app context
    # from tensorflow.keras.models import load_model
    # app.config['MODEL'] = load_model('path/to/your/model.h5')

    app.run(debug=True)
