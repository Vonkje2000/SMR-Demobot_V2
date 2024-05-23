const MESSAGES = {
    HUMANS_DETECTION: {
        START:'Humans detection process started.',
        STOP:"Humans detection stopped"
    },
    POSE_DETECTION: {
        START:'Pose detection started',
        STOP:"Pose detection stopped"
    },
    EMOTIONS_DETECTION: {
        START:'Detect emotions has been started',
        STOP:"Emotions detection stopped"
    },
    SYSTEM:{
        START:'The system has been activated',
        STOP:"The system has been disactivated"
    },
    EMERGENCY:"Emergency mode started, Please stay away from the robot. Robot stopping immediately. ",
    DANCING_MODE:{
        START:"Dancing mode activated! Let's dance and make unforgettable memories together",
        END: "Thanks for dancing with me"
    },
    HI:"Hi my friend",
    GREETINGS_ANSWER: "I am doing great, my friend, and I hope you are too."
}
const MUSICS = {
    HUMANS_DETECTION: "Corporate.mp3",
    POSE_DETECTION:"3.The Positive Rock(Short Version).wav",
    EMOTIONS_DETECTION:"Get That Feeling - Happy Upbeat Indie Pop (60s).mp3",
    SAD: "Emotional Piano.mp3",
}

const synth = window.speechSynthesis;
const voices = synth.getVoices();

function speak(text,callback) {
    disableButtons()
    const synth = window.speechSynthesis;
    const utterance = new SpeechSynthesisUtterance(text);    
    
    // Choose a voice
    utterance.voice =voices.find(voice => voice.name === 'Microsoft Susan - English (United Kingdom)' || voice.name === 'Microsoft Hazel - English (United Kingdom)');
    
    // Adjust pitch and rate to make the voice sound more child-like
    utterance.pitch = 1.25; // Higher pitch
    utterance.rate = 1.1;  // Slightly faster rate
    
     // Call the callback function when the speech ends
     utterance.onend = function() {
        disableButtons(false)
        if (callback) {
            callback();
        }
    };

    utterance.onerror = function(event) {
        console.error("Speech synthesis error:", event.error);
        if (callback) {
            callback(event);
        }
    };

    synth.speak(utterance);
}

// window.speechSynthesis.onvoiceschanged = () => {
//     const voices = window.speechSynthesis.getVoices();
//     console.log(voices);
// };

function disableButtons(disable = true) {
    document.querySelectorAll('.control-btns, #startBtn').forEach(button => button.disabled = disable);
}
