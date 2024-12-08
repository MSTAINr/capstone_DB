from google.cloud import firestore
import json

def store_data(id, data):
    try:
        # Konfigurasi path ke credential
        path_key = "./submissionmlgc-moestain-e814072b58d0.json"
        with open(path_key, "r") as file:
            credentials = json.load(file)

        # Inisialisasi Firestore
        db = firestore.Client.from_service_account_json(path_key)

        # Simpan data ke koleksi Firestore
        predict_collection = db.collection("predictions")
        predict_collection.document(id).set(data)
        print("Data berhasil disimpan.")
    except Exception as error:
        print(f"Gagal menyimpan data: {error}")
