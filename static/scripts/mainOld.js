const peopleDetectionBTN = document.getElementById('peopleDetectionBTN');
const poseDetectionBTN = document.getElementById('poseDetectionBTN');
const emotionDetectionBTN = document.getElementById('emotionDetectionBTN');
const playGameBTN = document.getElementById('playGameBTN');
const emergencyBtn = document.getElementById('emergency');
const danceBtn = document.getElementById('danceBtn');

const videoFeed = document.getElementById('videoFeed');
const staticImage = document.getElementById('staticImage');
const spinners = document.getElementById('spinners');
const startBtn = document.getElementById('startBtn');
const music = document.getElementById('music');
const dancingVideo = document.getElementById('dancingVideo');


const socket = io();

peopleDetectionBTN.addEventListener('click', () => toggleDetection('AI: Detect People', '/objects_detection', peopleDetectionBTN));
poseDetectionBTN.addEventListener('click', () => toggleDetection('AI: Seeing how you move', '/pose_detection', poseDetectionBTN));
emotionDetectionBTN.addEventListener('click', () => toggleDetection('AI: Detect emotions', '/emotion_detection', emotionDetectionBTN));
danceBtn.addEventListener('click', ()=>{handleDance(danceBtn)});
playGameBTN.addEventListener('click', () => sendMessage('robot', 'game_started'));

emergencyBtn.addEventListener('click', () => {
    sendMessage('voice', 'emergency')
});


function enableVideoFeed(src,btn){
    videoFeed.style.display = 'block';
    videoFeed.src = src;
    btn.innerText = 'Stop Detection';
    staticImage.style.display = 'none';
    btn.style.background = "linear-gradient(45deg, #fafbfc 10%, white 10%)"
    btn.classList.add("started")
}

function disableVideoFeed(btn,detectText){
    videoFeed.style.display = 'none';
    videoFeed.src = '';
    btn.innerText = detectText;
    staticImage.style.display = 'block'; 
    btn.style.background = "#f8f9fa"
    btn.classList.remove("started")

}

function mute(){
    music.pause();
    dancingVideo.pause()
}
function toggleDetection(detectText, src, btn) {
    mute()
    spinners.style.display = 'block';
    if (videoFeed.style.display === 'none') {
        sendMessage('voice',`${src.replace("/","")}_started`);
        enableVideoFeed(src,btn);
    }else{
        sendMessage('voice',`${src.replace("/","")}_stopped`);
        disableVideoFeed(btn,detectText)
    }
    videoFeed.onload = () => { spinners.style.display = 'none'; videoFeed.style.position = 'unset'; }
    videoFeed.onerror = () => { spinners.style.display = 'none'; videoFeed.style.position = 'unset'; }

}

function handleDance(btn) {
    sendMessage('robot', 'dancing_started');
    disableVideoFeed(btn,'Dance mode is running')
    dancingVideo.style.display = 'block';
    dancingVideo.src = '/static/videos/dancing_robot.mp4';
    staticImage.style.display = 'none';
    dancingVideo.onended = () => {
        disableButtons(false)
        sendMessage('robot', 'dancing_ended');
        dancingVideo.style.display = 'none';
        staticImage.style.display = 'block';
        btn.innerText ='Dance for me'
    };
}

function disableButtons(disable = true) {
    document.querySelectorAll('.control-btns, #startBtn').forEach(button => button.disabled = disable);
}

function handleStartStop() {
    music.pause()
    dancingVideo.style.display = 'none'
    dancingVideo.pause()
    if(startBtn.innerText.includes('Start')){
        sendMessage('voice', 'active_system')
        startBtn.innerText = 'Stop System'
        document.querySelectorAll('.control-btns').forEach(btn => btn.style.display = 'block');
        document.getElementById('startBtn').style.display = 'block';
    }else{
        startBtn.innerText = 'Start System'
        sendMessage('voice', 'deactivate_system')
        staticImage.style.display = 'block'
        document.querySelectorAll('.control-btns').forEach(btn => btn.style.display = 'none');
        videoFeed.style.display = 'none'
    }
} 



socket.on('connect', () => console.log('Connected to the server'));
socket.on('response', data => {
    console.log('Received data:', data);
    const message = data.message
    if (message === 'dancing_started') {dancingVideo.play();} 
    else if(message.includes('detection_started')) {
        document.querySelector(".started").disabled = false;
        if(message.includes("pose_detection_started")){
            sendMessage("voice", "move")
        }else{
            music.play();
        }
    }else if(message.includes("move")){
        document.querySelector(".started").disabled = false;
        music.play();
    } else if(message.includes('detection_stopped') ||message !== 'emergency'){
        dancingVideo.pause(); 
        music.pause();
        disableButtons(false)  
    } 

});

function sendMessage(type, message) {
    disableButtons();
    socket.emit('message', JSON.stringify({ type, message }));
}
