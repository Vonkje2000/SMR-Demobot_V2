

function executeTasks(command) {
        const isSystemStarted = startBtn.innerText.includes("Stop");
        const isPoseDetectionStarted = poseDetectionBTN.innerText.includes("Stop");
        const isHumanDetectionStarted = peopleDetectionBTN.innerText.includes("Stop");
        const isEmotionDetectionStarted = emotionDetectionBTN.innerText.includes("Stop");
        const isDancingModeOn = danceBtn.innerText.includes("running");
        const isGameStarted = danceBtn.innerText.includes("Started");

        switch (command) {
            case 'start system': case 'star system':
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
            case 'start dance': 
            case 'start dancing':
            case 'dance for':
                if (!isDancingModeOn) danceBtn.click();
                break;
            case 'stop danc':
                    if (isDancingModeOn) danceBtn.click();
                    break;  

            case 'stop detect': 
            case 'stop': 
            case 'turn off':
                document.querySelectorAll('.control-btns, #startBtn').forEach(btn => {
                    if (btn.innerText.includes("Stop") || btn.innerText.includes("started")|| btn.innerText.includes("running")) btn.click();
                });
                break;
            case 'emergency':
                speak(MESSAGES.EMERGENCY);
                break;
            case 'start game':
            case 'play game':
            case 'playing game':     
            case 'gaming':
            case 'play again':
            case 'start again':     
                if(!isGameStarted) playGameBTN.click();
                break;    
            case 'hi robo': 
            case 'hey': 
            case 'hello':
                speak(MESSAGES.HI);
            break;
            case 'good': 
            case 'great': 
            case 'doing well':
                speak(MESSAGES.HAPPY_TO_HEAR);
                break;    
            case 'name':
                speak(MESSAGES.SAYING_ROBOT_NAME);
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
let lastAiCommand=''
function startContinuousRecognition() {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'en-US';
    recognition.interimResults = true;
    recognition.continuous = true;

    let lastCommand = '';
    let lastAiCommand = '';

    recognition.onresult = (event) => {
        if(lastTaskDone){
            const results = Array.from(event.results);
            const interimResult = results.filter(result => !result.isFinal).map(result => result[0].transcript.toLowerCase().trim().replace("  "," ")).join(' ');
            const finalResults = results.filter(result => result.isFinal);
            const finalResult = finalResults.length > 0 ? finalResults[finalResults.length - 1][0].transcript.toLowerCase().trim().replace("  "," ") : '';
    
            console.log(`Interim transcript: ${interimResult}`);
            console.log(`Final transcript: ${finalResult}`);
    
            let textInCommands = false;
            const checkAndExecute = (transcript) => {
                for (let command of commandsList) {
                    if (transcript.includes(command)) {
                        textInCommands = true;
                        if (lastCommand != command || command.includes("stop danc")) {
                            console.log(`Command sent: ${command}`);
                            executeTasks(command);
                            lastCommand = command;
                            break;
                        }
                    }
                }
            };
    
            if (interimResult.trim()) {
                checkAndExecute(interimResult.trim());
            }
            if (!textInCommands && finalResult.trim().startsWith('smart robot') && lastTaskDone && finalResult.trim().length>15 && finalResult !== lastAiCommand) {
                console.log("Called Ai", finalResult, lastTaskDone, lastAiCommand, textInCommands);
                useAiToGetAnswer(finalResult.trim());
                lastAiCommand = finalResult;
            }
        };
    
        }
     
    recognition.onerror = (event) => { console.error(`Recognition error: ${event.error}`); };
    recognition.onend = () => {
        console.log('Speech recognition service disconnected');
        setTimeout(() => {
            recognition.start(); // Restart recognition with a slight delay to prevent immediate end/start loop
        }, 150);
    };

    recognition.start();
}

startContinuousRecognition();