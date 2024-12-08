from flask import Flask, request
from flask_restful import Api
from handler import post_predict_handler, predict_histories  # Import handler functions

app = Flask(__name__)
api = Api(app)

# Route for prediction
@app.route('/predict', methods=['POST'])
def predict_route():
    """
    Route to handle predictions.
    Allows image upload in 'multipart/form-data'.
    """
    try:
        # Validate content type and size
        if 'image' not in request.files:
            return {
                "status": "error",
                "message": "Image file is required"
            }, 400
        
        image = request.files['image']
        
        # Limit the size of the uploaded file (1MB max)
        if len(image.read()) > 1 * 1024 * 1024:
            return {
                "status": "error",
                "message": "Image file size exceeds 1MB limit"
            }, 400
        
        # Reset file pointer after size validation
        image.seek(0)
        
        # Call the handler for prediction
        return post_predict_handler()
    except Exception as e:
        return {
            "status": "error",
            "message": f"An error occurred: {str(e)}"
        }, 500

# Route for prediction histories
@app.route('/predict/histories', methods=['GET'])
def histories_route():
    """
    Route to fetch prediction histories.
    """
    try:
        # Call the handler for fetching histories
        return predict_histories()
    except Exception as e:
        return {
            "status": "error",
            "message": f"An error occurred: {str(e)}"
        }, 500

if __name__ == '__main__':
    # Start the Flask app
    app.run(debug=True)
