
const commandsList = [
    'start system',
    'stop system',
    'detect people', 'people detect', 'detecting people', 'detection people',
    'pose detection','see how i move','move detection', 'detect move', 'detect pose',
    'stop detect','stop', 'turn off',
    'hi','hello', 'hey',
    'how are you','your day','do you do','how is it going','how\'s it going','how is going',
    'doing great', 'good','doing well',
    'feelings','read my feel','emotion',
    'emergency',
    'dance','dancing',
    'start game', 'gaming','play again', 'start again'
];


function executeTasks(command) {
        const isSystemStarted = startBtn.innerText.includes("Stop");
        const isPoseDetectionStarted = poseDetectionBTN.innerText.includes("Stop");
        const isHumanDetectionStarted = peopleDetectionBTN.innerText.includes("Stop");
        const isEmotionDetectionStarted = emotionDetectionBTN.innerText.includes("Stop");
        const isDancingModeOn = danceBtn.innerText.includes("running");
        const isGameStarted = danceBtn.innerText.includes("Started");

        switch (command) {
            case 'start system':
                if (!isSystemStarted) startBtn.click();
                break;
            case 'stop system':
                if (isSystemStarted) startBtn.click();
                break;
            case 'detect people': 
            case 'people detect': 
            case 'detecting people': 
            case 'detection people':
                if (!isHumanDetectionStarted) peopleDetectionBTN.click();
                break;
            case 'pose detection':
            case 'see how i move': 
            case 'move detection': 
            case 'detect move': 
            case 'detect pose':
                if (!isPoseDetectionStarted) poseDetectionBTN.click();
                break;
            case 'feelings':
            case 'read my feel': 
            case 'emotion':
                if (!isEmotionDetectionStarted) emotionDetectionBTN.click();
                break;
            case 'dance': 
            case 'dancing':
                if (!isDancingModeOn) danceBtn.click();
                break;
            case 'stop detect': 
            case 'stop': 
            case 'turn off':
                document.querySelectorAll('.control-btns, #startBtn').forEach(btn => {
                    if (btn.innerText.includes("Stop") || btn.innerText.includes("started")) btn.click();
                });
                break;
            case 'emergency':
                speak(MESSAGES.EMERGENCY);
                break;
            case 'start game':
            case 'gaming':
            case 'play again':
            case 'start again':     
                if(!isGameStarted) playGameBTN.click();
                break;    
            case 'hi': 
            case 'hey': 
            case 'hello':
                speak(MESSAGES.HI);
            break;
            case 'good': 
            case 'great': 
            case 'doing well':
                speak(MESSAGES.HAPPY_TO_HEAR);
                break;    
            case 'how are you':
            case 'your day':
            case 'do you do':
            case 'how is it going':
            case 'how\'s it going':
            case 'how is going':
                speak(MESSAGES.GREETINGS_ANSWER);
                break;
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
        // console.log(`Interim transcript: ${interimResult}`);
    
        const checkAndExecute = (transcript) => {
            for (let command of commandsList) {
                if (transcript.includes(command)) {
                    if (lastCommand !=command) {
                        console.log(`Command sent: ${command}`);
                        executeTasks(command);
                        lastCommand = command;
                    } break;
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