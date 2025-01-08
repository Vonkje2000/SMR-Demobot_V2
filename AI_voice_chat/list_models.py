import os
from openai import Client

# Create a client instance using the API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

client = Client(api_key=api_key)

def list_available_models():
    """
    List all models accessible by the API key and display their details.
    """
    try:
        # Fetch the list of available models
        models = client.models.list()
        
        print("Available models:\n")
        # Iterate through the models
        for model in models:
            print(f"ID: {model.id}")
            print(f"Owned by: {model.owned_by}")
            print(f"Created: {getattr(model, 'created', 'Unknown')}")
            print("-" * 40)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    list_available_models()
