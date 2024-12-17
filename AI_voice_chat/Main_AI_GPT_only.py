import os
import base64
import tempfile

import streamlit as st
from streamlit_chat import message
import azure.cognitiveservices.speech as speechsdk
import openai
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

import soundfile as sf  
import sounddevice as sd  

# ================================ #
#          Configuration           #
# ================================ #

def load_prompt_and_logo():
    """Load detailed prompt and encode logo as Base64."""
    prompt_path = "C:/Users/stath/Desktop/PromoBot/AzureStudioChatGPTVoiceBot-main/Prompttext.text"
    logo_path = "C:/Users/stath/Desktop/PromoBot/AzureStudioChatGPTVoiceBot-main/CBLogo.png"
    with open(prompt_path, "r", encoding="utf-8") as file:
        detailed_prompt = file.read()
    with open(logo_path, "rb") as image_file:
        encoded_logo = base64.b64encode(image_file.read()).decode("utf-8")
    return detailed_prompt, encoded_logo


detailed_prompt, encoded_logo = load_prompt_and_logo()

# Language-based text swapping
TEXTS = {
    "English": {
        "header": "Promo Bot",
        "subheader": "Representing the Smart Manufacturing & Robotics minor in Delft.",
        "description": "Press the button below to ask a question, and I will respond.",
        "listening": "I'm now listening",
        "language_button": "Nederlands",
    },
    "Nederlands": {
        "header": "Promo Bot",
        "subheader": "Representerend de minor Slimme Productie & Robotica in Delft.",
        "description": "Druk op de knop hieronder om een vraag te stellen, en ik zal antwoorden.",
        "listening": "Ik luister nu",
        "language_button": "English",
    },
}

# ================================ #
#           Helper Functions       #
# ================================ #

def initialize_speech_config():
    """Initialize Azure speech configuration."""
    azure_api_key = os.getenv("AZURE_TTS_KEY")
    azure_region = os.getenv("AZURE_TTS_REGION")
    if not azure_api_key or not azure_region:
        st.error("Azure TTS API credentials are missing.")
        return None
    return speechsdk.SpeechConfig(subscription=azure_api_key, region=azure_region)

def transcribe_audio(client, temp_audio_path):
    """
    Transcribes audio using OpenAI's Whisper-1 model with support for multilingual transcription.
    Returns:
        - transcribed text (str)
        - detected language (str, e.g., 'en-GB' or 'nl-BE')
    """
    try:
        # Perform Whisper transcription
        with open(temp_audio_path, "rb") as audio_file:
            whisper_response = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
            )   

        transcription = whisper_response.text.strip()

        # Map to Azure-compatible language codes (Defaulting to English if no other context provided)
        detected_language = "en-GB"  # Default language for responses
        if "nl" in transcription.lower():  # Simplistic language check
            detected_language = "nl-BE"

    except Exception as e:
        st.error(f"Error during transcription: {e}")
        return None, None

    return transcription, detected_language



def generate_response(input_text, conversation_history, language_code):
    """
    Generates GPT response using OpenAI based on the detected language.
    """
    messages = [{"role": "system", "content": detailed_prompt}] + conversation_history + [
        {"role": "user", "content": input_text}]
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        st.error("OpenAI API key is missing.")
        return None

    # Set prompt and response language for GPT
    if language_code == "en-GB":
        prompt_language = "Respond in English."
    elif language_code == "nl-BE":
        prompt_language = "Respond in Nederlands."
    else:
        prompt_language = "Respond in the appropriate language."

    # Add language-specific instruction
    messages.insert(0, {"role": "system", "content": prompt_language})

    client = openai.Client()
    response = client.chat.completions.create(
        model="gpt-4o-2024-11-20", messages=messages, max_tokens=200, temperature=0
    )
    return response.choices[0].message.content


def synthesize_speech(speech_config, text, language_code):
    """
    Generates speech audio data using the appropriate voice for the detected language.
    """
    voice_name = "en-GB-RyanNeural" if language_code == "en-GB" else "nl-BE-ArnaudNeural"
    speech_config.speech_synthesis_voice_name = voice_name
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
    result = synthesizer.speak_text_async(text).get()
    return result.audio_data


def play_audio(audio_data):
    """Plays audio via JavaScript without showing file."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio.write(audio_data)
        audio_url = f"http://localhost:8501/{temp_audio.name}"  # Assumes Streamlit serves files locally
        js_code = f"""
        <script>
            var audio = new Audio("{audio_url}");
            audio.play();
        </script>
        """
        st.markdown(js_code, unsafe_allow_html=True)


def render_chat_bubble(text, is_user=True):
    """Render a chat bubble for user or bot."""
    color = "#007BFF" if is_user else "#ADD8E6"
    alignment = "margin-right: auto;" if is_user else "margin-left: auto;"
    border_radius = "15px 15px 15px 5px;" if is_user else "25px 25px 5px 25px;"
    st.markdown(
        f"""
        <div style="
            background-color: {color};
            color: {'white' if is_user else 'black'};
            padding: 15px;
            border-radius: {border_radius};
            margin: 10px 0;
            max-width: 70%;
            width: fit-content;
            text-align: left;
            {alignment}
        ">
            {text}
        </div>
        """, unsafe_allow_html=True
    )

def get_texts(language):
    """
    Retrieve the appropriate text content for the selected language.
    """
    return TEXTS.get(language, TEXTS["English"])


def render_header(encoded_logo, texts):
    """
    Dynamically render the header with language-specific text.
    """
    st.markdown(
        f"""
        <div class="header-container">
            <button class="back-button" onclick="location.reload()">Back to Home</button>
            <div class="container">
                <div class="logo-section">
                    <img src="data:image/png;base64,{encoded_logo}" style="width:150px;height:150px;">
                </div>
                <div class="text-section">
                    <h1>{texts['header']}</h1>
                    <h5>{texts['subheader']}</h5>
                    <hr style="border: none; border-top: 1px solid #ccc; margin: 10px 0;">
                    <p>{texts['description']}</p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Callback functions to enforce mutual exclusivity
def select_english():
    st.session_state.language = "English"
    st.session_state.english = True
    st.session_state.nederlands = False  # Unselect Nederlands

def select_nederlands():
    st.session_state.language = "Nederlands"
    st.session_state.nederlands = True
    st.session_state.english = False  # Unselect English
    
# Initialize checkbox states
if "english" not in st.session_state:
    st.session_state.english = True  # Default to English
if "nederlands" not in st.session_state:
    st.session_state.nederlands = False

def record_audio(temp_audio_path, duration=10, samplerate=44100):
    """
    Records audio from the default microphone and saves it in a supported format.
    """
    try:
        st.text("🎤 Recording... Speak now.")
        # Record audio
        audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
        sd.wait()  # Wait until recording is finished

        # Save the recording to a wav file
        sf.write(temp_audio_path, audio_data, samplerate)
        st.text("🎤 Recording complete.")
    except Exception as e:
        st.error(f"Error during audio recording: {e}")
        return None



# ================================ #
#          Main Application        #
# ================================ #

def main():
    # Initialize Session State
    if "language" not in st.session_state:
        st.session_state.language = "English"  # Default language

    conversation_history = []

    # Get texts based on the selected language
    texts = get_texts(st.session_state.language)

    # Render Header
    render_header(encoded_logo, texts)

    # Language selection checkboxes
    col1, col2 = st.columns(2)
    with col1:
        st.checkbox(
            "English",
            value=st.session_state.english,
            key="english_checkbox",
            on_change=select_english,
        )
    with col2:
        st.checkbox(
            "Nederlands",
            value=st.session_state.nederlands,
            key="nederlands_checkbox",
            on_change=select_nederlands,
        )

    # Highlight the selected language
    st.write(f"**Current Language:** {st.session_state.language}")
    
    # Initialize Speech Config
    speech_config = initialize_speech_config()
    if not speech_config:
        return

    # Chat Interaction
    if st.button("Start Talk"):
        # Prepare temporary file path
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            temp_audio_path = temp_audio.name

        # Record audio
        record_audio(temp_audio_path)

        # Transcribe audio using Whisper
        user_input, detected_language = transcribe_audio(client, temp_audio_path)

        # Clean up temporary file
        os.remove(temp_audio_path)

        if user_input:
            render_chat_bubble(user_input, is_user=True)

            # Determine the response language
            response_language = detected_language

            # Generate GPT response
            bot_response = generate_response(user_input, conversation_history, response_language)
            if bot_response:
                conversation_history.append({"role": "user", "content": user_input})
                conversation_history.append({"role": "assistant", "content": bot_response})
                render_chat_bubble(bot_response, is_user=False)

                # Synthesize bot's response with Azure TTS
                bot_audio = synthesize_speech(speech_config, bot_response, response_language)
                play_audio(bot_audio)


if __name__ == "__main__":
    main()

# streamlit run c:/Users/stath/Desktop/PromoBot/AzureStudioChatGPTVoiceBot-main/Main_AI_GPT_only.py