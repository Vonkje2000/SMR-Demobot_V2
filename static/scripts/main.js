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
const counterElement = document.getElementById("counter");
const gameImg = document.getElementById("gameImg");
const gameBox = document.getElementById("gameBox");

peopleDetectionBTN.addEventListener('click', () => handleDetectionByVision('AI: Detect People', '/objects_detection', peopleDetectionBTN, MESSAGES.HUMANS_DETECTION, MUSICS.HUMANS_DETECTION));
poseDetectionBTN.addEventListener('click', () => handleDetectionByVision('AI: Seeing how you move', '/pose_detection', poseDetectionBTN,MESSAGES.POSE_DETECTION,MUSICS.POSE_DETECTION));
emotionDetectionBTN.addEventListener('click', () => handleDetectionByVision('AI: Detect emotions', '/emotion_detection', emotionDetectionBTN,MESSAGES.EMOTIONS_DETECTION, MUSICS.EMOTIONS_DETECTION));
danceBtn.addEventListener('click', ()=>{handleDance(danceBtn)});
playGameBTN.addEventListener('click',handlePlayGame)
emergencyBtn.addEventListener('click', () => {
    speak(MESSAGES.EMERGENCY, ()=>{  mute(); disableButtons(false) })
});

let loopInterval;
function handlePlayGame() {
    gameBox.style.display = "block"
    gameImg.style.display = 'block';
    gameImg.src = "/static/images/rock-paper-scissors.png"
    playGameBTN.innerText = 'Rock Paper Scissors Game started';

    speak(MESSAGES.PLAY_GAME, ()=>{ 
    showOptions()
    let count = 0;
    const images = ["/static/images/rock.png", "/static/images/paper.png", "/static/images/scissors.png"];
    speak(MESSAGES.COUNT123)
     const countdown = setInterval(() => {
        if (count < 3) {
            counterElement.textContent = ++count;
            if (count ==2)  sendMessage('game', 'rock_paper_scissors');
        }else{
            clearInterval(countdown); 
            counterElement.textContent = 'Go!';   
            startImageLoop();
        }
    }, 500);

    
    function startImageLoop() {

        let loopCount = 0;
        loopInterval = setInterval(() => {
            gameImg.src = images[loopCount % images.length];
            loopCount++;
        }, 50);
    }

    })
}

function enableVideoFeed(src,btn){
    gameBox.style.display = 'none'
    videoFeed.style.display = 'block';
    videoFeed.src = src;
    btn.innerText = 'Stop Detection';
    staticImage.style.display = 'none';
    btn.style.background = "linear-gradient(45deg, #fafbfc 10%, white 10%)"
    btn.classList.add("started")
    videoFeed.style.position="absolute"
}

function disableVideoFeed(btn,detectText){
    videoFeed.style.display = 'none';
    videoFeed.src = '';
    btn.innerText = detectText;
    staticImage.style.display = 'block'; 
    btn.style.background = "#f8f9fa"
    btn.classList.remove("started")
}

function mute(){ music.pause(); dancingVideo.pause()}
function showOptions(on = true){
    document.querySelectorAll('.control-btns').forEach(btn => btn.style.display = on?'block':'none');
}
function handleDetectionByVision(detectText, src, btn, MESSAGES, musicFile) {
    showOptions()
    mute()
    spinners.style.display = 'block';
    if (videoFeed.style.display === 'none') {
        music.src = `/static/music/${musicFile}`
        
        setTimeout(() => { music.play()}, 2000);
        speak(MESSAGES.START, ()=>{
            disableButtons()
            btn.disabled = false;
        }) 
        enableVideoFeed(src,btn);
        
    }else{
        disableButtons()
        speak(MESSAGES.STOP)  // sendMessage('voice',`${src.replace("/","")}_stopped`);
        disableVideoFeed(btn,detectText)
    }
    videoFeed.onload = () => { spinners.style.display = 'none'; videoFeed.style.position = 'unset'; }
    videoFeed.onerror = () => { spinners.style.display = 'none'; videoFeed.style.position = 'unset'; }

}

function handleDance(btn) {
    gameBox.style.display = 'none'
    showOptions()
    // sendMessage('robot', 'dancing_started');
    speak(MESSAGES.DANCING_MODE.START, ()=>{
        disableVideoFeed(btn,'Dance mode is running')
        dancingVideo.style.display = 'block';
        dancingVideo.src = '/static/videos/dancing_robot.mp4';
        staticImage.style.display = 'none';
        dancingVideo.play()
        disableButtons()
        dancingVideo.onended = () => {
            disableButtons(false)
            // sendMessage('robot', 'dancing_ended');
            speak(MESSAGES.DANCING_MODE.END)
            dancingVideo.style.display = 'none';
            staticImage.style.display = 'block';
            btn.innerText ='Dance for me'
        };
    })

  
}


function handleStartStop() {
    mute()
    dancingVideo.style.display = 'none'
    gameBox.style.display = 'none'
    dancingVideo.pause()
    if(startBtn.innerText.includes('Start')){
        // sendMessage('voice', 'active_system')
        startBtn.innerText = 'Stop System'
        speak(MESSAGES.SYSTEM.START)
        showOptions()
        document.getElementById('startBtn').style.display = 'block';
    }else{
        startBtn.innerText = 'Start System'
        // sendMessage('voice', 'deactivate_system')
        speak(MESSAGES.SYSTEM.STOP)
        staticImage.style.display = 'block'
        showOptions(false)
        videoFeed.style.display = 'none'
    }
} 



socket.on('connect', () => console.log('Connected to the server'));
socket.on('response', data => {
    if (data.robotchoise ) {     
        speak(`Robot choose ${data.robotchoise}`)
        counterElement.innerText = data.robotchoise
        gameImg.src = `/static/images/${data.robotchoise}.png`;
        clearInterval(loopInterval);
    }
});

function sendMessage(type, message) {
    disableButtons();
    socket.emit('message', JSON.stringify({ type, message }));
}
