const speechRecognitionCheckbox = document.getElementById('SpeechRecognition');

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
            case 'stop system': case'turn off system': case'turn off the system':
                if (isSystemStarted) startBtn.click();
                break;
            case 'detect people': case 'people detect': case 'detecting people': case 'detection people':
                if (!isHumanDetectionStarted) peopleDetectionBTN.click();
                break;
            case 'pose detection': case 'see how i move': case 'move detection': case 'detect move': case 'detect pose':
                if (!isPoseDetectionStarted) poseDetectionBTN.click();
                break;
            case 'feelings': case 'read my feel': case 'emotion':
                if (!isEmotionDetectionStarted) emotionDetectionBTN.click();
                break;
            case 'start dance':  case 'start dancing': case 'dance for':
                if (!isDancingModeOn) danceBtn.click();
                break;
            case 'stop danc':
                if (isDancingModeOn) danceBtn.click();
                break;  
            case 'stop detect':  case 'turn off detect':
                document.querySelectorAll('.control-btns, #startBtn').forEach(btn => {
                    if (btn.innerText.includes("Stop") || btn.innerText.includes("started")|| btn.innerText.includes("running")) btn.click();
                });
                break;
            case 'emergency':  
                speak(MESSAGES.EMERGENCY); 
                break;
            case 'start game':   case 'play game':  case 'playing game': case 'gaming': case 'play again': case 'start again':     
                if(!isGameStarted) playGameBTN.click();
                break;    
            case 'hi robo': case 'hey robo': case 'hello robo':
                speak(MESSAGES.HI);
            break;
            case 'good': case 'great': case 'doing well':
                speak(MESSAGES.HAPPY_TO_HEAR);
                break;    
            case 'what is your name':  case 'what\'s your name':
                speak(MESSAGES.SAYING_ROBOT_NAME);
                break;   
            case 'how are you': case 'your day': case 'do you do': case 'how is it going': case 'how\'s it going': case 'how is going':
                speak(MESSAGES.GREETINGS_ANSWER);
                break;
            case 'stop speech recognition':
                    speechRecognitionCheckbox.click()
                    break; 
            case ROBOT_NAME:
                speak(MESSAGES.ROBOT_LISTENING)           
            default:
                console.log(`Command "${command}" not recognized.`);
                break;
        }
}

let lastCommand = ''
let lastAiCommand=''
let recognition
let startListening = false;
function startContinuousRecognition() {
    recognition = new (window.speechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'en-US';
    recognition.interimResults = true;
    recognition.continuous = true;

    recognition.onresult = (event) => {
        if(lastTaskDone){
            const results = Array.from(event.results);
            const interimResult = results.filter(result => !result.isFinal).map(result => result[0].transcript.toLowerCase().trim().replace("  "," ")).join(' ');
            const finalResults = results.filter(result => result.isFinal);
            const finalResult = finalResults.length > 0 ? finalResults[finalResults.length - 1][0].transcript.toLowerCase().trim().replace("  "," ") : '';
    
            console.log(`Interim transcript: ${interimResult}`);
            console.log(`Final transcript: ${finalResult}`);
            transcript.innerText = interimResult
            let textInCommands = false;
            const checkAndExecute = (transcript) => {
                for (let command of commandsList) {
                    if (transcript.includes(command) ) {
                        startListening = false;
                        textInCommands = true;
                        if (lastCommand != command) {
                            console.log(`Command sent: ${command}`);
                            if(transcript === ROBOT_NAME){
                                setTimeout(() => {  lastCommand = ''}, 5000);
                            }
                            executeTasks(command);
                            lastCommand = command;
                            break;
                        }
                    }
                }
            };
    
            if (interimResult) checkAndExecute(interimResult);
            

            if(startListening && finalResult.length>15 && (!finalResult.startsWith(ROBOT_NAME)) && (!textInCommands)){
                console.log('sending data', finalResult)
                startListening = false;
                useAiToGetAnswer(finalResult);
            }

            if (finalResult.startsWith(ROBOT_NAME) && (!textInCommands)) {
                startListening = true
                console.log('starting listening')
            }

            
        };
    
        }
     
    recognition.onerror = (event) => { console.error(`Recognition error: ${event.error}`); };
    recognition.onend = () => {
        console.log('Speech recognition service disconnected');
        if (speechRecognitionCheckbox.checked) {
            setTimeout(() => {
              recognition.start(); // Restart recognition with a slight delay to prevent immediate end/start loop
            }, 150);
          }
    };

    recognition.start();
}

function stopSpeechRecognition() {
    if (recognition) {
      console.log('Stopping speech recognition');
      recognition.onend = null; // Temporarily remove the onend handler to avoid auto-restart
      recognition.stop();
      recognition = null;
      console.log('Speech recognition stopped');
    }
  }
if(speechRecognitionCheckbox.checked) startContinuousRecognition()
speechRecognitionCheckbox.addEventListener('change', (event) => {
      if (event.target.checked) {
        speak(MESSAGES.START_SPEECH); 
        startContinuousRecognition()
      } 
      else {
        stopSpeechRecognition()
        speak(MESSAGES.STOP_SPEECH); 
      }
});
