import os
import base64
import tempfile

import streamlit as st
from streamlit_chat import message
import azure.cognitiveservices.speech as speechsdk
import openai
from openai import OpenAI

# Import audio recording libraries
import soundfile as sf  
import sounddevice as sd  

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ================================ #
#          Configuration           #
# ================================ #

def load_prompt_and_logo():

    """
    Load a detailed GPT prompt and encode the logo image as Base64.
    """ 
    prompt_path = "AI_voice_chat/Prompttext.text"
    logo_path = "AI_voice_chat/CBLogo.png"

    with open(prompt_path, "r", encoding="utf-8") as file:
        detailed_prompt = file.read()
    with open(logo_path, "rb") as image_file:
        encoded_logo = base64.b64encode(image_file.read()).decode("utf-8")
    return detailed_prompt, encoded_logo

# Load system prompt and logo
detailed_prompt, encoded_logo = load_prompt_and_logo()

# Texts for UI components based on language selection
TEXTS = {
    "English": {
        "header": "Promo Bot",
        "subheader": "Representing the Smart Manufacturing & Robotics minor in Delft.",
        "description": "Select your preferred language for the text on screen, and Press the button below to start a talk.",
        "listening": "I'm now listening",
        "language_button": "Nederlands",
    },
    "Nederlands": {
        "header": "Promo Bot",
        "subheader": "Representerend de minor Smart Manufacturing & Robotics in Delft.",
        "description": "Kies je voorkeurstaal voor de tekst op het scherm en druk op de knop hieronder om een gesprek te starten.",
        "listening": "Ik luister nu",
        "language_button": "English",
    },
}

# ================================ #
#           Helper Functions       #
# ================================ #

def initialize_speech_config():
    """
    Initialize Azure Speech SDK configuration for Text-to-Speech (TTS).
    """
    azure_api_key = os.getenv("AZURE_TTS_KEY")
    azure_region = os.getenv("AZURE_TTS_REGION")
    if not azure_api_key or not azure_region:
        st.error("Azure TTS API credentials are missing.")
        return None
    return speechsdk.SpeechConfig(subscription=azure_api_key, region=azure_region)

def transcribe_audio(client, temp_audio_path):
    """
    Transcribes audio using OpenAI's Whisper-1 model with multilingual detection.
    Handles full language names (e.g., 'dutch') and maps them to Azure-compatible codes.
    """
    try:
        with open(temp_audio_path, "rb") as audio_file:
            whisper_response = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="verbose_json"
            )
            
        # Extract transcription and language
        transcription = whisper_response.text.strip()
        detected_language = whisper_response.language.lower()  # Normalize to lowercase

        #st.write(f"**Whisper Detected Language:** {detected_language}")  # Debug output

        # Map Whisper's output to Azure-compatible language codes
        azure_language_mapping = {
            "en": "en-GB",       # English (ISO code)
            "nl": "nl-NL",       # Dutch (ISO code)
            "dutch": "nl-NL",    # Whisper sometimes returns 'dutch' as the language name
            "english": "en-GB"   # Whisper sometimes returns 'english'
        }

        # Map detected language to Azure-compatible code, default to 'en-GB'
        azure_language_code = azure_language_mapping.get(detected_language, "en-GB")

    except Exception as e:
        st.error(f"Error during transcription: {e}")
        return None, "en-GB"  # Default fallback to English

    return transcription, azure_language_code


def generate_response(input_text, conversation_history, language_code):
    """
    Generates GPT response using OpenAI based on the detected language.
    """
    messages = [{"role": "system", "content": detailed_prompt}] + conversation_history + [
        {"role": "user", "content": input_text}
    ]

    # Language-specific instructions
    if language_code == "en-GB":
        prompt_language = "Respond in English."
    elif language_code == "nl-NL":
        prompt_language = "Respond in Dutch (Nederlands)."
    else:
        prompt_language = "Respond in the appropriate language."

    messages.insert(0, {"role": "system", "content": prompt_language})

    # Call OpenAI GPT API  
    try:
        response = client.chat.completions.create(
            model="gpt-4o-2024-11-20", messages=messages, max_tokens=200, temperature=0
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error generating response: {e}")
        return None


def synthesize_speech(speech_config, text, language_code):
    """
    Convert text to speech using Azure TTS and return audio data.
    """
    # Map detected language to appropriate Azure TTS voice
    voice_mapping = {
        "en-GB": "en-GB-RyanNeural",  # English voice
        "nl-NL": "nl-NL-MaartenNeural"  # Dutch voice
    }

    # Default to English voice if language code is unrecognized
    voice_name = voice_mapping.get(language_code, "en-GB-RyanNeural")
    speech_config.speech_synthesis_voice_name = voice_name

    try:
        #st.write(f"**Selected Voice:** {voice_name}")  # Debug print
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
        result = synthesizer.speak_text_async(text).get()
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            return result.audio_data
        else:
            st.error("Speech synthesis failed.")
            return None
    except Exception as e:
        st.error(f"Error during speech synthesis: {e}")
        return None


def play_audio(audio_data):
    """
    Play audio using a temporary file served via Streamlit.
    """
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
    st.session_state.english = False # Default to unchecked for English
if "nederlands" not in st.session_state:
    st.session_state.nederlands = True  # Default to checked for Nederlands

def record_audio(temp_audio_path, duration=10, samplerate=44100):
    """
    Record audio from the default microphone and save to a file.
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
    """
    Main function to run the Streamlit app.
    """
    # Initialize session state for language
    if "language" not in st.session_state:
        st.session_state.language = "Nederlands"  # Default language

    conversation_history = [] # Track the conversation

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

    # Highlight the selected language for UI purposes
    st.write(f"**Selected Language:** {st.session_state.language}")

    # Initialize Speech Config
    speech_config = initialize_speech_config()
    if not speech_config:
        return

    # Chat Interaction
    if st.button("Start Talk"):
        # Inform the user "I'm now listening" in the current Selected language
        listening_text = texts["listening"]
        ui_language_code = "en-GB" if st.session_state.language == "English" else "nl-NL"
        listening_audio = synthesize_speech(speech_config, listening_text, ui_language_code)
        if listening_audio:
            play_audio(listening_audio)

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
            # Display transcribed text
            render_chat_bubble(user_input, is_user=True)

            # Default to detected language
            if detected_language:
                response_language = detected_language
            else:
                response_language = "en-GB"  # Fallback to English if detection fails

            #st.write(f"**Detected Language:** {response_language}") # Debug output (keep this)

            # Generate GPT response
            bot_response = generate_response(user_input, conversation_history, response_language)
            if bot_response:
                conversation_history.append({"role": "user", "content": user_input})
                conversation_history.append({"role": "assistant", "content": bot_response})
                render_chat_bubble(bot_response, is_user=False)

                # Synthesize bot's response using detected language
                bot_audio = synthesize_speech(speech_config, bot_response, response_language)
                if bot_audio:
                    play_audio(bot_audio)
                else:
                    st.error("Failed to synthesize speech.")

if __name__ == "__main__":
    main()

# streamlit run "AI_voice_chat/Main_AI_GPT_only.py"