import requests

def get_azure_voices(subscription_key, region):
    # Construct the endpoint URL
    endpoint = f"https://westeurope.tts.speech.microsoft.com/cognitiveservices/voices/list"
    
    # Set up headers
    headers = {
        "Ocp-Apim-Subscription-Key": subscription_key,
    }

    # Make the request
    response = requests.get(endpoint, headers=headers)

    # Check the response status code
    if response.status_code == 200:
        voices = response.json()
        return voices
    else:
        print(f"Error: Unable to get voices list, status code: {response.status_code}")
        return None

# Use your Azure Speech service subscription key and region
subscription_key = "8uGTioY7On1Su5J6YSnk6fE44Srs77TKQsfYwYqbmpzdCK9WRr7OJQQJ99ALAC5RqLJXJ3w3AAAYACOGzAnq"
region = "westeurope"  # You can change this to your specific Azure region

voices = get_azure_voices(subscription_key, region)

# Print the available voices
if voices:
    for voice in voices:
        print(f"Name: {voice['Name']}, Locale: {voice['Locale']}, Gender: {voice['Gender']}, Voice Type: {voice['VoiceType']}")
