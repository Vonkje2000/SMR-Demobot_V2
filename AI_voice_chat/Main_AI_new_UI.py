import os
import tempfile
from flask import Flask, request, jsonify, render_template
import logging

import azure.cognitiveservices.speech as speechsdk
import openai

import re

# Import audio recording libraries
import soundfile as sf
import sounddevice as sd 

# ================================ #
#          Configuration           #
# ================================ #

#app = Flask(__name__)
logging.getLogger('werkzeug').disabled = True

asked_question = " "
AI_response = " "
webpage_selected_language = "English"

#@app.route('/AI_voice_chat')
#@app.endpoint('/AI_voice_chat')
def AI_index():
	return render_template('AI_voice_chat.html')

#@app.route('/API', methods=['POST', 'GET'])
#@app.endpoint('API', methods=['POST', 'GET'])
#@app.endpoint('API')
def post_api():
	global asked_question
	global AI_response
	global webpage_selected_language
	if request.method == 'POST':
		data = request.json
		button_state = data.get('listen_button')
		Language = data.get('Language')
		if button_state != None:
			asked_question = "..."
			AI_response = "..."
			start_listening()
		if Language != None:
			webpage_selected_language = Language
			if (webpage_selected_language == "Dutch"):
				webpage_selected_language = "Nederlands"
			print(Language)
		return jsonify({"status": "success"})
	if request.method == 'GET':
		response = {"question": asked_question, "AI_answer": AI_response}
		return jsonify(response)


def load_prompt():
	prompt_path = "AI_voice_chat/Prompttext.text"
	with open(prompt_path, "r", encoding="utf-8") as file:
		detailed_prompt = file.read()
	return detailed_prompt

# Language-based text swapping
TEXTS = {
	"English": {
		"listening": "I'm now listening",
	},
	"Nederlands": {
		"listening": "Ik luister nu",
	},
}

# ================================ #
#           Helper Functions       #
# ================================ #

def initialize_speech_config():
	"""Initialize Azure speech configuration."""
	azure_api_key = os.getenv("AZURE_TTS_KEY")
	if not azure_api_key:
		raise KeyError("Azure TTS API credentials are missing.")
	azure_region = os.getenv("AZURE_TTS_REGION")
	if not azure_region:
		raise KeyError("Azure region is missing.")
	
	return speechsdk.SpeechConfig(subscription=azure_api_key, region=azure_region)

def initialize_openAI():
	openai.api_key = os.getenv("OPENAI_API_KEY")
	if not openai.api_key:
		raise KeyError("OpenAI API key is missing.")
	return openai.Client()

def transcribe_audio():
    """
    Transcribes audio using OpenAI's Whisper-1 model with multilingual detection.
    Handles full language names (e.g., 'dutch') and maps them to Azure-compatible codes.
    """
    
	# Prepare temporary file path
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio_path = temp_audio.name

    # Record audio
    record_audio(temp_audio_path)

    client = openai.Client()

    try:
        with open(temp_audio_path, "rb") as audio_file:
            whisper_response = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="verbose_json"
            )
            
        # Extract transcription and language
        transcription = whisper_response.text.strip()
        transcription = filter_text(transcription)  # Filter the transcription
        detected_language = whisper_response.language.lower()  # Normalize to lowercase

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
        # Clean up temporary file
        os.remove(temp_audio_path)
        raise AttributeError("Error during transcription: {e}")
    
    # Clean up temporary file
    os.remove(temp_audio_path)

    return transcription, azure_language_code

def record_audio(temp_audio_path, duration=10, samplerate=44100):
    """
    Record audio from the default microphone and save to a file.
    """
    try:
        audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
        sd.wait()  # Wait until recording is finished

        # Save the recording to a wav file
        sf.write(temp_audio_path, audio_data, samplerate)
    except Exception as e:
        raise SystemError(f"Error during audio recording: {e}")

def filter_text(transcription):
    """
    Filters the given transcription to allow only alphanumeric characters, spaces,
    and the symbols (), !, @. Excludes all other symbols including *.
    """
    # Regex to match allowed characters: alphanumeric, spaces, and specific symbols
    transcription = re.sub(r'\*', '', transcription)
    allowed_pattern = r"[^a-zA-Z0-9\s\(\)\!\@]"  # Explicitly excludes all other characters, including *
    return re.sub(allowed_pattern, "", transcription)

def generate_response(input_text, conversation_history, language_code):
	#Generates GPT response using OpenAI based on the detected language.
	messages = [{"role": "system", "content": detailed_prompt}] + conversation_history + [
		{"role": "user", "content": input_text}]

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
	#Generates speech audio data using the appropriate voice for the detected language.
	voice_mapping = {
        "en-GB": "en-GB-RyanNeural",  # English voice
        "nl-NL": "nl-NL-MaartenNeural"  # Dutch voice
    }
	voice_name = voice_mapping.get(language_code, "en-GB-RyanNeural")
	speech_config.speech_synthesis_voice_name = voice_name
	synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
	synthesizer.speak_text_async(text).get()

def start_listening():
	# Get texts based on the selected language
	texts = TEXTS.get(webpage_selected_language, TEXTS["English"])

	# Map session state language to the corresponding speech synthesis language code
	listening_text = texts["listening"]
	ui_language_code = "en-GB" if webpage_selected_language == "English" else "nl-NL"
	synthesize_speech(speech_config, listening_text, ui_language_code)

	# Transcribe audio using Whisper
	user_input, detected_language = transcribe_audio()
		
	if user_input:
		global asked_question
		global AI_response
		asked_question = user_input

		# Default to detected language
		if detected_language:
			response_language = detected_language
		else:
			response_language = "en-GB"  # Fallback to English if detection fails

		# Generate and Play Bot Response
		bot_response = generate_response(user_input, conversation_history, response_language)
		bot_response = filter_text(bot_response)  # Filter the transcription
		conversation_history.append({"role": "user", "content": user_input})
		conversation_history.append({"role": "assistant", "content": bot_response})
		AI_response = bot_response
		synthesize_speech(speech_config, bot_response, response_language)

# ================================ #
#          Main Application        #
# ================================ #

conversation_history = []

# Initialize stuf
detailed_prompt = load_prompt()
speech_config = initialize_speech_config()
client = initialize_openAI()

#def main():
#	app.run(debug=False)

#if __name__ == "__main__":
#	print(" * Running on http://127.0.0.1:5000")
#	main()
