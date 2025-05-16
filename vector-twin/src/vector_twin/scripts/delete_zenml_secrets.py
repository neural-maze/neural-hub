from zenml.client import Client

client = Client()

try:
    client.delete_secret(
        name_id_or_prefix="qdrant"
    )
except KeyError:
    print("Secret not found. Skipping deletion ...")
