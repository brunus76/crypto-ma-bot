# secrets.py
import os
from google.cloud import secretmanager

def access_secret(secret_id):
    client = secretmanager.SecretManagerServiceClient()
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    return client.access_secret_version(name=name).payload.data.decode("UTF-8")

def get_coinbase_credentials():
    return {
        "api_key": access_secret("coinbase-api-key"),
        "api_secret": access_secret("coinbase-api-secret"),
        "api_passphrase": access_secret("coinbase-api-passphrase"),
    }