const peopleDetectionBtn = document.getElementById('peopleDetectionBtn');
const poseDetectionBtn = document.getElementById('poseDetectionBtn');
const emotionDetectionBtn = document.getElementById('emotionDetectionBtn');
const playGameBtn = document.getElementById('playGameBtn');
const emergencyBtn = document.getElementById('emergencyBtn');
const danceBtn = document.getElementById('danceBtn');
const staticImage = document.getElementById('staticImage');
const startBtn = document.getElementById('startBtn');
const tvModeBtn = document.getElementById('tvModeBTN');
let emergencyMode = false
let emergencyImg = document.querySelector('#emergencyBtn img')

const detectionButtons = [
    { btn: peopleDetectionBtn, text: 'AI: Detect People', src: '/objects_detection', message: MESSAGES.HUMANS_DETECTION, music: MUSICS.HUMANS_DETECTION },
    { btn: poseDetectionBtn, text: 'AI: Seeing how you move', src: '/pose_detection', message: MESSAGES.POSE_DETECTION, music: MUSICS.POSE_DETECTION },
    { btn: emotionDetectionBtn, text: 'AI: Detect emotions', src: '/emotion_detection', message: MESSAGES.EMOTIONS_DETECTION, music: MUSICS.EMOTIONS_DETECTION },
];

detectionButtons.forEach(({ btn, text, src, message, music }) => {
    btn.addEventListener('click', () => handleDetectionByVision(btn, text, src,message, music));
});

danceBtn.addEventListener('click', () => handleDance(danceBtn));
playGameBtn.addEventListener('click', handlePlayGame);
startBtn.addEventListener('click', handleStartStop)
tvModeBtn.addEventListener('click', () => { sendMessage('tvMode'); speak(MESSAGES.TV_MODE); });

emergencyBtn.addEventListener('click', handleEmergency);

function handleEmergency(){
    if(!emergencyMode){
        if( speechRecognitionCheckbox.checked) speechRecognitionCheckbox.click(); speechRecognitionCheckbox.disabled = true
        emergencyMode = true
        stopRunningActions()
        speak(MESSAGES.EMERGENCY,()=>{  disableButtons(); }); 
        emergencyImg.src = '/static/images/safe-shield.png'
        emergencyImg.title = "Cancle Emergency"
        sendMessage('startEmergency')
    }else{
        emergencyMode = false
        if(!speechRecognitionCheckbox.checked) speechRecognitionCheckbox.click()
        speak(MESSAGES.STOP_EMERGENCY); 
        emergencyImg.src = '/static/images/sos.png';
        emergencyImg.title = "Start Emergency"
        sendMessage('stopEmergency')
    }
}

function handleStartStop() {
    const isStarting = startBtn.innerText.includes('Start');
    startBtn.innerText = isStarting ? 'Stop System' : 'Start System';
    speak(isStarting ? MESSAGES.SYSTEM.START : MESSAGES.SYSTEM.STOP);
    showOptions(isStarting);
    document.getElementById('startBtn').style.display = 'block';
}

function handleDetectionByVision(btn, detectText, src, message, musicFile) {
    handleStartStop()
    if (!btn.innerText.includes('Stop') ) {
        sendMessage({ startVision: true, src, musicFile });
        sendMessage(src.replace('/', ''));
        speak(message.START, () => { disableButtons(); btn.disabled = false; });
        btn.innerText = 'Stop Detection';
        btn.style.background = "linear-gradient(45deg, #fafbfc 10%, white 10%)";
        btn.classList.add("started");
    } else {
        stopAction(btn, detectText, message.STOP);
    }
}

function stopAction(btn, detectText, stopMessage) {
    console.log('From stopAction',btn )
    sendMessage('stopVision');
    speak(stopMessage);
    btn.innerText = detectText;
    btn.style.background = "#f8f9fa";
    btn.classList.remove("started");
}

function showOptions(on = true){
    document.querySelectorAll('.control-btns').forEach(btn => btn.style.display = on?'block':'none');
}

function handleDance(btn) {
    handleStartStop()
    if (!danceBtn.innerText.includes("running")) {
        speak(MESSAGES.DANCING_MODE.START, ()=>{
            sendMessage('danceMode');
            btn.innerText = 'Dance mode is running'
            btn.style.background = "#f8f9fa"
            btn.classList.remove("started")
        })
    }

}

function handlePlayGame() {
    sendMessage('playGame');
    playGameBtn.innerText = 'Game started';
}
function endDancing(){
    speak(MESSAGES.DANCING_MODE.END, ()=>{
        danceBtn.innerText ='Dance for me'
    })
}


socket.on('response', data => {
    console.log(data.message)
    if (data.robotChoice) { playGameBtn.innerText = 'Play again'; disableButtons(false);}
    if(data.message =='danceModeDone') endDancing()
});

