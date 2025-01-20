import os
import tempfile
from flask import request, jsonify, render_template
import numpy as np
import azure.cognitiveservices.speech as speechsdk
import openai
import webrtcvad

import re

# Import audio recording libraries
import soundfile as sf
import sounddevice as sd 

# ================================ #
#          Configuration           #
# ================================ #

asked_question = " "
AI_response = " "
webpage_selected_language = "English"

def AI_index():
	return render_template('AI_voice_chat.html')

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
    record_audio_until_silence(temp_audio_path)

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
        raise AttributeError(f"Error during transcription: {e}")
	
    # Clean up temporary file
    os.remove(temp_audio_path)

    return transcription, azure_language_code

def record_audio_until_silence(temp_audio_path, samplerate=8000, frame_duration_ms=10, silence_duration=2):
	"""
	Record audio until silence is detected, using WebRTC VAD.
	"""
	vad = webrtcvad.Vad(3)  # Level 3 is the most aggressive noise suppression
	buffer = []
	chunksize = int(samplerate * frame_duration_ms / 1000)
	silence_counter = 0
	max_silence_chunks = int((samplerate * silence_duration) / chunksize)

	try:
		stream = sd.InputStream(samplerate=samplerate, channels=1, dtype='int16', blocksize=chunksize)
		with stream:
			while True:
				data, overflowed = stream.read(chunksize)
				frame = np.frombuffer(data, dtype=np.int16)

				# WebRTC VAD expects 16-bit mono PCM audio
				is_speech = vad.is_speech(frame.tobytes(), samplerate)
				
				buffer.extend(frame)

				if is_speech:
					silence_counter = 0
				else:
					silence_counter += 1

				if silence_counter > max_silence_chunks:
					break

		buffer = np.array(buffer, dtype='int16')
		sf.write(temp_audio_path, buffer, samplerate)
	
	except Exception as e:
		if os.path.exists(temp_audio_path):
			os.remove(temp_audio_path)
		raise SystemError(f"Error during audio recording: {e}")

def filter_text(transcription):
	"""
	Filters the given transcription to allow only alphanumeric characters, spaces,
	and the symbols (), !, @. Excludes all other symbols including *.
	"""
	# Regex to match allowed characters: alphanumeric, spaces, and specific symbols
	transcription = re.sub(r'\*', '', transcription)
	transcription = re.sub(r'\`', '', transcription)
	transcription = re.sub(r'###', '#', transcription)
	transcription = re.sub(r'\n---\n', '\n', transcription)
	transcription = re.sub(r'\n\n', '\n', transcription)
	#transcription = re.sub(r"[^a-zA-Z0-9\s\(\)\!\@\.\,\:\'\\\£\$\%\€\°\?\[\]\&\{\}\;\-\_\+\/]",transcription) # Explicitly excludes all other characters, including *
	return transcription

def generate_response(input_text, conversation_history, language_code):
	# Generates GPT response using OpenAI based on the selected language.
    messages = [{"role": "system", "content": detailed_prompt}] + conversation_history + [
        {"role": "user", "content": input_text}]

	# Set prompt and response language based on user's selection
    if language_code == "en-GB":
        prompt_language = "Respond in English."
    elif language_code == "nl-NL":
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
	voice_mapping = {
		"en-GB": "en-GB-RyanNeural",
		"nl-NL": "nl-NL-MaartenNeural"
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
	response_language = "en-GB" if webpage_selected_language == "English" else "nl-NL"
	synthesize_speech(speech_config, listening_text, response_language)

	# Transcribe audio using Whisper
	user_input, _ = transcribe_audio()
		
	if user_input:
		global asked_question
		global AI_response
		asked_question = user_input

		# Generate Bot Response in selected language
		bot_response = generate_response(user_input, conversation_history, response_language)
		bot_response = filter_text(bot_response)  # Filter the response text
		conversation_history.append({"role": "user", "content": user_input})
		conversation_history.append({"role": "assistant", "content": bot_response})
		AI_response = bot_response

        # Synthesize response using the selected language's voice
		synthesize_speech(speech_config, bot_response, response_language)

# ================================ #
#          Main Application        #
# ================================ #

conversation_history = []

# Initialize stuf
detailed_prompt = load_prompt()
speech_config = initialize_speech_config()
client = initialize_openAI()