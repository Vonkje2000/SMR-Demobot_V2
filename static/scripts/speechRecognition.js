const speechRecognitionCheckbox = document.getElementById('SpeechRecognition');
const isSystemStarted = startBtn.innerText.includes("Stop");
const isPoseDetectionStarted = poseDetectionBtn.innerText.includes("Stop");
const isHumanDetectionStarted = peopleDetectionBtn.innerText.includes("Stop");
const isEmotionDetectionStarted = emotionDetectionBtn.innerText.includes("Stop");
const isDancingModeOn = danceBtn.innerText.includes("running");
const isGameStarted = danceBtn.innerText.includes("Game started");

function executeTasks(command) {
        switch (command) {
            case 'start system': case 'star system':
                if (!isSystemStarted) startBtn.click();
                break;
            case 'stop system': case'turn off system': case'turn off the system':
                if (isSystemStarted) startBtn.click();
                break;
            case 'detect people': case 'people detect': case 'detecting people': case 'detection people':
                if (!isHumanDetectionStarted) peopleDetectionBtn.click();
                break;
            case 'pose detection': case 'see how i move': case 'move detection': case 'detect move': case 'detect pose':
                if (!isPoseDetectionStarted) poseDetectionBtn.click();
                break;
            case 'feelings': case 'read my feel': case 'emotion':
                if (!isEmotionDetectionStarted) emotionDetectionBtn.click();
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
            case 'turn on emergency': case 'start emergency': case 'call emergency':
                speak(MESSAGES.EMERGENCY); 
                break;
            case 'start game':   case 'play game':  case 'playing game': case 'gaming': case 'play again': case 'start again':     
                if(!isGameStarted) playGameBtn.click();
                break;    
            case `hi ${ROBOT_NAME}`: case `hey ${ROBOT_NAME}`: case `hello ${ROBOT_NAME}`:
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
            case 'thanks': case 'thank you':
                    speak(MESSAGES.THANKS_RESPONSE);
                break;    
            case 'stop speech recognition': case 'turn off speech': case 'turn off the speech':
                    speechRecognitionCheckbox.click()
                    break; 
            case 'tv mode': case 'mode tv':
                    tvModeBtn.click();
                    break;     
            default:
                console.log(`Command "${command}" not recognized.`);
                break;
        }
}

let lastCommand = ''
let lastAiCommand=''
let recognition
let startListening = false;
let textInCommands = false;

function startContinuousRecognition() {
    recognition = new (window.speechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'en-US';
    recognition.interimResults = true;
    recognition.continuous = true;

    recognition.onresult = (event) => {
        if(lastTaskDone){
          const results = Array.from(event.results);
          let interimResult = results.filter(result => !result.isFinal).map(result => result[0].transcript.toLowerCase().trim().replace("  ", " ")).join(' ');
          const finalResults = results.filter(result => result.isFinal);
          let finalResult = finalResults.length > 0 ? finalResults[finalResults.length - 1][0].transcript.toLowerCase().trim().replace("  ", " ") : '';
          interimResult = interimResult.trim().replaceAll('  ', ' ');
        
          console.log(`Interim transcript: ${interimResult}`);
          console.log(`Final transcript: ${finalResult}`);
          transcript.innerText = interimResult;

        if (interimResult) processTranscript(interimResult)
        
        // Replace all instances of ROBOT_NAME in finalResult
        finalResult = finalResult.replaceAll(ROBOT_NAME, '');

        if (lastTaskDone && startListening && finalResult.length > 15 && !textInCommands && finalResult != lastCommand) {
          lastCommand = finalResult;
          useAiToGetAnswer(finalResult);
        }
      
        if (interimResult.includes(ROBOT_NAME) && !textInCommands && !startListening) {
          speak(MESSAGES.ROBOT_LISTENING, () => {
            startListening = true;
          });
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

function processTranscript(transcript) {
  textInCommands = false;
  for (let command of commandsList) {
      if (transcript.includes(command) ) {
          startListening = false;
          textInCommands = true;
          if (lastCommand != command) {
              console.log(`Command sent: ${command}`);
              executeTasks(command);
              lastCommand = command;
              break;
          }
      }
  }
  }
