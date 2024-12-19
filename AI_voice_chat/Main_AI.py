import os
from flask import Flask, request, jsonify, render_template

import azure.cognitiveservices.speech as speechsdk
import openai

# ================================ #
#          Configuration           #
# ================================ #

app = Flask(__name__)

asked_question = " "
AI_response = " "
webpage_selected_language = "English"

@app.route('/')
def index():
	return render_template('AI_voice_chat.html')

@app.route('/API', methods=['POST', 'GET'])
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


def transcribe_audio(speech_config, preferred_language=None):
	"""
	Transcribes audio from the default microphone, with support for Nederlands as the default language.
	Returns:
		- transcribed text (str)
		- detected language (str, e.g., 'en-GB' or 'nl-BE')
	"""
	audio_config = speechsdk.AudioConfig(use_default_microphone=True)

	if preferred_language == "Nederlands":
		# Auto-detection, but defaults to nl-BE
		auto_detect_config = speechsdk.languageconfig.AutoDetectSourceLanguageConfig(
			languages=["nl-BE", "en-GB"]
		)
		speech_recognizer = speechsdk.SpeechRecognizer(
			speech_config=speech_config,
			audio_config=audio_config,
			auto_detect_source_language_config=auto_detect_config,
		)
	else:
		# Auto-detection, but defaults to en-GB
		auto_detect_config = speechsdk.languageconfig.AutoDetectSourceLanguageConfig(
			languages=["en-GB", "nl-BE"]
		)
		speech_recognizer = speechsdk.SpeechRecognizer(
			speech_config=speech_config,
			audio_config=audio_config,
			auto_detect_source_language_config=auto_detect_config,
		)

	# Perform recognition
	result = speech_recognizer.recognize_once_async().get()

	# Get detected language
	detected_language = result.properties.get(
		speechsdk.PropertyId.SpeechServiceConnection_AutoDetectSourceLanguageResult
	)

	# Check for transcription failure or low confidence
	if not result.text.strip():
		print("Low recognition confidence, please try again.")
		return None, None

	return result.text.strip(), detected_language

def generate_response(input_text, conversation_history, language_code):
	#Generates GPT response using OpenAI based on the detected language.
	messages = [{"role": "system", "content": detailed_prompt}] + conversation_history + [
		{"role": "user", "content": input_text}]
	openai.api_key = os.getenv("OPENAI_API_KEY")
	if not openai.api_key:
		raise KeyError("OpenAI API key is missing.")

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
	voice_name = "en-GB-RyanNeural" if language_code == "en-GB" else "nl-BE-ArnaudNeural"
	speech_config.speech_synthesis_voice_name = voice_name
	synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
	result = synthesizer.speak_text_async(text).get()

def start_listening():
	# Get texts based on the selected language
	texts = TEXTS.get(webpage_selected_language, TEXTS["English"])

	# Map session state language to the corresponding speech synthesis language code
	language_code = "nl-BE" if webpage_selected_language == "Nederlands" else "en-GB"

	# Listening prompt based on language
	listening_text = texts["listening"]
	synthesize_speech(speech_config, listening_text, language_code)

	# Transcribe user input with fallback to auto-detection
	user_input, detected_language = transcribe_audio(speech_config, preferred_language=webpage_selected_language)
		
	if user_input:
		global asked_question
		global AI_response
		asked_question = user_input

		# Determine the response language based on detected language
		response_language = detected_language if detected_language else "en-GB"

		# Generate and Play Bot Response
		bot_response = generate_response(user_input, conversation_history, response_language)
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

def main():
	app.run(debug=False)

if __name__ == "__main__":
	main()