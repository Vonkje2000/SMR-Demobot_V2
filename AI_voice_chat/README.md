# PromoBot Voice Chat Application
Representing the Smart Manufacturing & Robotics Minor in Delft

This project is a Streamlit-based chatbot that uses Azure Cognitive Services, OpenAI GPT, and Text-to-Speech capabilities to create an interactive AI-driven conversational experience. It supports English and Dutch (Nederlands) languages.

# Features
Interactive Voice Communication: Users can speak to the bot, and it will respond both verbally and textually.
Multilingual Support: Supports English and Dutch languages with language auto-detection.
Azure Text-to-Speech (TTS): Speech synthesis for bot responses.
OpenAI Integration: Uses GPT models for generating chatbot responses.
Streamlit UI: User-friendly interface for seamless interactions.

# Prerequisites
Python 3.8+, (3,9,2 was used)
Azure Subscription with Azure Cognitive Services.
OpenAI API Key.
Required libraries: streamlit, azure-cognitiveservices-speech, openai, streamlit_chat.


# Installation
1. Clone the repository:
git clone https://github.com/yourusername/PromoBot.git
cd PromoBot

2. Install required dependencies:
pip install -r requirements.txt

# Setup Instructions
1. Set Environment Variables: 

AZURE_TTS_KEY: Azure Text-to-Speech API Key.
AZURE_TTS_REGION: Azure service region.
OPENAI_API_KEY: OpenAI GPT API Key.

2. Place your prompt text file at: C:/Users/USERNAME/Desktop/PromoBot/Prompttext.text
3. Place the logo image at: C:/Users/USERNAME/Desktop/PromoBot/CBLogo.png

Update paths in the script if needed.

# Usage
1. Open the Terminal and run: streamlit run c://Users/USERNAME/Desktop/PromoBot/AzureStudioChatGPTVoiceBot-main/Main_AI.py

This will run the streamlit application and open a http://localhost:8501

2. User Flow:
- Select your preferred language: English or Nederlands. (English is currently the default)
- Click the Start Talk button.
- Speak to the bot when prompted, and it will respond with both audio and text.

# File Structure
SMR-DEMOBOT_V2/AI_voice_chat
│-- Main_AI.py              # Main program
│-- Main_AI:GPT_only.py     # Main program using wisper-1 instead of Azuer for Speech to text
│-- Prompttext.text         # System prompt for OpenAI GPT
│-- CBLogo.png              # Logo image
│-- MSCB.mp4                # Video file
│-- README.md               # Project documentation

SMR-DEMOBOT_V2
│-- requirements.txt        # Project dependencies

# How it Works
1. Speech Recognition: Captures user speech using Azure's Speech SDK.
2. Language Detection: Detects whether the user is speaking in English or Dutch.
3. Text Generation: Sends transcribed text to OpenAI's GPT API for generating responses.
4. Text-to-Speech: Synthesizes GPT's response using Azure TTS.
5. Streamlit UI: Displays the conversation as chat bubbles and plays audio responses.

# License
This project is licensed under the MIT License. Feel free to use this code however you like.