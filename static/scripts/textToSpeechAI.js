
const synth = window.speechSynthesis;
const voices = synth.getVoices();

function speak(text, callback) {
    console.log("From speak");
    
    // Cancel any ongoing speech to ensure a clean state
    if (window.speechSynthesis.speaking) {
        console.error("Speech synthesis is already in progress.");
        window.speechSynthesis.cancel();
    }

    disableButtons(true); // Disable buttons at the start of the speech

    const synth = window.speechSynthesis;
    const utterance = new SpeechSynthesisUtterance(text);

    // Select a voice; defaulting to the first compatible one if multiple are valid
    utterance.voice = voices.find(voice =>
        ['Microsoft Susan - English (United Kingdom)', 
         'Microsoft Hazel - English (United Kingdom)', 
         'Google UK English Male'].includes(voice.name));

    // Configure the voice properties
    utterance.pitch = 1.25; // Higher pitch
    utterance.rate = 1.1;  // Slightly faster rate

    // Event when speech starts
    utterance.onstart = function() {
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
        disableButtons(false); // Re-enable buttons when speech is complete or stopped
        if (callback) {
            callback();
        }
    }
}

function disableButtons(disable) {
    // Example: Disable/enable all buttons on the page
    const buttons = document.querySelectorAll("button");
    buttons.forEach(button => {
        button.disabled = disable;
    });
}


window.speechSynthesis.onvoiceschanged = () => {
    const voices = window.speechSynthesis.getVoices();
    // console.log(voices);
};

function disableButtons(disable = true) {
    document.querySelectorAll('.control-btns, #startBtn').forEach(button => button.disabled = disable);
}
