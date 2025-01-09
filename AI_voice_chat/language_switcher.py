import streamlit as st
import azure.cognitiveservices.speech as speechsdk

# Define language-specific text and voice configuration
LANGUAGES = {
    "English": {
        "subtitle": "Representing the Smart Manufacturing & Robotics minor in Delft.",
        "description": "Press the button below to ask a question, and I will respond.",
        "listening_message": "I am now listening",
        "start_talking": "Start Talk",
        "voice": "en-US-ChristopherNeural",
    },
    "Dutch": {
        "subtitle": "Vertegenwoordiger van de minor Smart Manufacturing & Robotics in Delft.",
        "description": "Druk op de knop hieronder om een vraag te stellen, en ik zal antwoorden.",
        "listening_message": "Ik luister nu",
        "start_talking": "Begin met praten",
        "voice": "nl-NL-ColetteNeural",
    },
}

def initialize_language():
    """
    Initialize the language selection in Streamlit's session state.
    Defaults to 'English'.
    """
    if "language" not in st.session_state:
        st.session_state.language = "English"

def render_language_buttons():
    """
    Render language selection buttons with improved positioning and alignment.
    """
    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 20px;">
            <button onclick="window.location.reload()" 
                    style="background-color: #007BFF; color: white; 
                    padding: 10px 202px; font-size: 16px; 
                    border-radius: 5px; margin-right: 10px; cursor: pointer;">
                English
            </button>
            <button onclick="window.location.reload()" 
                    style="background-color: #FF5722; color: white; 
                    padding: 10px 20px; font-size: 16px; 
                    border-radius: 5px; cursor: pointer;">
                Dutch
            </button>
        </div>
        """,
        unsafe_allow_html=True,
    )

def get_current_language_config():
    """
    Get the current language's configuration.
    """
    return LANGUAGES[st.session_state.language]

def synthesize_listening_message(speech_config, file_path):
    """
    Synthesize the 'listening' message based on the selected language.
    """
    lang_config = get_current_language_config()
    speech_config.speech_synthesis_voice_name = lang_config["voice"]

    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
    result = speech_synthesizer.speak_text_async(lang_config["listening_message"]).get()

    with open(file_path, "wb") as f:
        f.write(result.audio_data)

    return lang_config["listening_message"]

if __name__ == "__main__":
    st.title("Language Switcher Test")
    initialize_language()
    render_language_buttons()

    lang_config = get_current_language_config()
    st.write(f"Selected Language: {st.session_state.language}")
    st.write(f"Subtitle: {lang_config['subtitle']}")
    st.write(f"Description: {lang_config['description']}")
    st.write(f"'Start Talking' Button Text: {lang_config['start_talking']}")
