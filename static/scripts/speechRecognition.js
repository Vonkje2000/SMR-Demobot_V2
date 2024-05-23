
const commandsList = [
    'start system',
    'stop system',
    'detect people', 'people detect', 'detecting people', 'detection people',
    'pose detection','see how i move','move detection', 'detect move', 'detect pose',
    'stop detect','stop',
    
    'hi robo','hello', 'hey robo', 'how are you',
    'feelings','read my feel','emotion',
    'emergency'
];

function executeTasks(command) {
    const isSystemStarted = startBtn.innerText.includes("Stop");
    const isPoseDetectionStarted = poseDetectionBTN.innerText.includes("Stop");
    const isHumanDetectionStarted = peopleDetectionBTN.innerText.includes("Stop");
    const isEmotionDetectionStarted = emotionDetectionBTN.innerText.includes("Stop");

    switch (command) {
        case 'start system':
            if (!isSystemStarted) startBtn.click();
            break;
        case 'stop system':
            if (isSystemStarted) startBtn.click();
            break;
        case 'detect people': case 'people detect': case 'detecting people': case 'detection people':
            if (!isHumanDetectionStarted) peopleDetectionBTN.click();
            break;
        case 'pose detection':case 'see how i move': case 'move detection': case 'detect move': case 'detect pose':
            if (!isPoseDetectionStarted) poseDetectionBTN.click();
            break;
        case 'feelings':case 'read my feel': case 'emotion':
            if (!isEmotionDetectionStarted) emotionDetectionBTN.click();
            break;
        case 'stop detect': case 'stop':
            document.querySelectorAll('.control-btns, #startBtn').forEach(btn => {
                if (btn.innerText.includes("Stop")) {
                    console.log("match", btn.innerText);
                    btn.click();
                } else {
                    console.log("no match", btn.innerText);
                }
            });
            break;

        case 'emergency':
                speak(MESSAGES.EMERGENCY)
                break            
        case 'hi robo': case 'hey robo': case 'hello':
            speak(MESSAGES.HI)
            break
        case 'how are you':
                speak(MESSAGES.GREETINGS_ANSWER)
                break    
        default:
            console.log(`Command "${command}" not recognized.`);
            break;
    }
}

let lastCommand = ''
function startContinuousRecognition() {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'en-US';
    recognition.interimResults = true;  // Enable interim results
    recognition.continuous = true;

    recognition.onresult = (event) => {
        const results = Array.from(event.results);
        const interimResult = results.filter(result => !result.isFinal).map(result => result[0].transcript.toLowerCase().trim().replace("  "," ")).join(' ');

        console.log(`Interim transcript: ${interimResult}`);
    
        const checkAndExecute = (transcript) => {
            for (let command of commandsList) {
                if (transcript.includes(command)) {
                    if (lastCommand !=command) {
                        console.log(`Command sent: ${command}`);
                        executeTasks(command);
                        lastCommand = command
                    }
                    break;
                }
            }
        };
        
        if (interimResult.trim()) {
            checkAndExecute(interimResult.trim());
        }
    };
    
    recognition.onerror = (event) => { console.error(`Recognition error: ${event.error}`);};

    recognition.onend = () => {
        console.log('Speech recognition service disconnected');
        setTimeout(() => {
            recognition.start(); // Restart recognition with a slight delay to prevent immediate end/start loop
        }, 100);
    };

    recognition.start();
}

startContinuousRecognition();