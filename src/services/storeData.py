from google.cloud import firestore
import os

# Path to the service account key file
path_key = os.path.abspath('path_key')

def store_data(doc_id, data):
    """
    Store data in Firestore.

    Args:
        doc_id (str): The document ID.
        data (dict): The data to store.
    """
    try:
        # Initialize Firestore client
        db = firestore.Client.from_service_account_json(path_key)
        
        # Reference the 'predictions' collection
        predictions_collection = db.collection('predictions')
        
        # Add or update the document with the specified ID
        predictions_collection.document(id).set(data)
        
        print(f"Data successfully stored with ID: {id}")
    except Exception as e:
        print(f"An error occurred: {e}")
