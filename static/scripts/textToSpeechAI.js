
const synth = window.speechSynthesis;
const voices = synth.getVoices();
let speakRunning = false
function speak(text, callback) {
    speakRunning = true
    // Cancel any ongoing speech to ensure a clean state
    if (window.speechSynthesis.speaking) {
        console.log("Speech synthesis is already in progress.");
        window.speechSynthesis.cancel();
    }

    disableButtons(true, 'speak true'); // Disable buttons at the start of the speech

    const synth = window.speechSynthesis;
    const utterance = new SpeechSynthesisUtterance(text);

    // Select a voice; defaulting to the first compatible one if multiple are valid
    utterance.voice = voices.find(voice =>
        ['Microsoft Susan - English (United Kingdom)', 
         'Microsoft Hazel - English (United Kingdom)', 
         'Google UK English Male'].includes(voice.name));

    // Configure the voice properties
    utterance.pitch = 1.15; // Higher pitch
    utterance.rate = 1;  // Slightly faster rate

    // Event when speech starts
    utterance.onstart = function() {
        sendMessage({aiAnswer: text})
        if(!aiTaskRunning) {
            if(transcriptHomePage){
                transcriptHomePage.classList.add('robotAnswer'); showTextOneByOne(text,transcriptHomePage) 
            }
        }
        // if(!aiTaskRunning) transcriptHomePage.innerText = text

        console.log("Speech has started.");
        setSpeechTimeout(); // Set a timeout to handle hanging
    };

    // Event when speech ends
    utterance.onend = function() {
        console.log("Speech has ended.");
        clearSpeechTimeout();
        finalizeSpeech();
    };

    // Handle speech synthesis errors
    utterance.onerror = function(event) {
        console.error("Speech synthesis error:", event.error);
        clearSpeechTimeout();
        finalizeSpeech();
    };

    // Speak the utterance
    synth.speak(utterance);

    // Helper functions
    let speechTimeout;
    function setSpeechTimeout() {
        clearSpeechTimeout(); // Clear existing timeout before setting a new one
        speechTimeout = setTimeout(() => {
            console.error("Speech timeout reached. Forcing stop.");
            synth.cancel(); // Force stop any speech that is hanging
            finalizeSpeech();
        }, 25000); // Set timeout for 20 seconds

    }

    function clearSpeechTimeout() {
        if (speechTimeout) {
            clearTimeout(speechTimeout);
            speechTimeout = null;
        }
    }

    function finalizeSpeech() {
        disableButtons(false, 'finalizeSpeech'); // Re-enable buttons when speech is complete or stopped
        setTimeout(() => { speakRunning = false }, 1500);
        if (callback) {
            callback();
        }
    }
}

// window.speechSynthesis.onvoiceschanged = () => {
//     const voices = window.speechSynthesis.getVoices();
//     // console.log(voices);
// };


