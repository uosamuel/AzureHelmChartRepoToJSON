from flask import Flask, jsonify
from azure.storage.blob import BlobServiceClient
import os

app = Flask(__name__)

def get_blob_contents(account_name, account_key, container_name):
    blob_service_client = BlobServiceClient(account_url=f"https://{account_name}.blob.core.windows.net", credential=account_key)
    container_client = blob_service_client.get_container_client(container_name)

    blob_list = []
    for blob in container_client.list_blobs():
        blob_list.append(blob.name)

    return blob_list

@app.route('/')
def index():
    account_name = os.getenv('AZURE_STORAGE_ACCOUNT_NAME')
    account_key = os.getenv('AZURE_STORAGE_ACCOUNT_KEY')
    container_name = os.getenv('AZURE_STORAGE_CONTAINER_NAME')
    
    if not account_name or not account_key or not container_name:
        return "Azure Blob Storage credentials not provided.", 500
    
    blob_contents = get_blob_contents(account_name, account_key, container_name)
    return jsonify(blob_contents)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
