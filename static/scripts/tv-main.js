

const counterElement = document.getElementById("counter");
const gameImg = document.getElementById("gameImg");
const gameBox = document.getElementById("gameBox");
const videoFeed = document.getElementById('videoFeed');
const staticImage = document.getElementById('staticImage');
const transcriptBox = document.getElementById('transcriptBox');

const spinners = document.getElementById('spinners');
const music = document.getElementById('music');
const video = document.getElementById('video');
const defaultVideo = video.src
const images = ["/static/images/rock.png", "/static/images/paper.png", "/static/images/scissors.png"];
const transcriptTVPage = document.getElementById("transcriptTVPage");

let loopInterval;
function handlePlayRockPaperGame() {
    gameBox.style.display = "block"
    gameImg.style.display = 'block';
    gameImg.src = "/static/images/rock-paper-scissors.png"
    video.style.display = 'none'
    speak(MESSAGES.PLAY_GAME, ()=>{ 
    sendMessage('gameMode');
    let count = 0;
     const countdown = setInterval(() => {
        if (count < 3) {
            speak(count+1)
            counterElement.textContent = ++count;
            if(count === 1)  startImageLoop()
        }else{
            clearInterval(countdown); 
        }
    },1000);
    })
}


function startImageLoop() {
    let loopCount = 0;
    loopInterval = setInterval(() => {
        gameImg.src = images[loopCount % images.length];
        loopCount++;
    }, 50);
}

function restChanges(){
    
    gameBox.style.display = 'none'
    spinners.style.display = 'none'
    music.pause();
    video.muted = true
    videoFeed.style.display = 'none'
    video.src = defaultVideo;
    video.style.display ="unset"
    transcriptBox.style.display = 'unset'
    video.style.width = '66%'
    video.style.margin = 'unset'
}

function enableVideoFeed(src){
    music.muted = false
    gameBox.style.display = 'none'
    videoFeed.style.display = 'unset';
    videoFeed.src = src;
    video.style.display = 'none';
    spinners.style.display = 'block';
}

function handleDetectionByVision(src,musicFile) {
    enableVideoFeed(src);
    music.src = `/static/music/${musicFile}`
    setTimeout(() => { music.play()}, 2000)

    videoFeed.onload = () => { spinners.style.display = 'none'; }
    videoFeed.onerror = () => { spinners.style.display = 'none';}
}

function processRobotchoise(robotchoise){
    clearInterval(loopInterval);
    speak(`Robot choose ${robotchoise}`)
    counterElement.innerText =robotchoise
    gameImg.src = `/static/images/${robotchoise}.png`;
    setTimeout(() => {
        restChanges()
    }, 3000);
}

function handleVideo(file, message) {
    gameBox.style.display = 'none'
    video.style.display = 'unset';
    video.src =`/static/videos/${file}`;
    if(message=='pongGameModeDone'){
        transcriptBox.style.display = 'none'
        // video.style.width = '80%'
        video.style.margin = 'auto'
    }
    video.muted = false
    video.play()
    video.onended = () => { 
        if(video.src.includes('pong_game.mp4') ||  video.src.includes('dancing_robot.mp4') ){
            restChanges(); 
            sendMessage(message);
        }
    };
}


socket.on('message', function(data) {
    console.log('Message received:', data);
});

socket.on('response', data => {
    if (data.robotChoice) processRobotchoise(data.robotChoice)
    if(data.message.startVision) handleDetectionByVision(data.message.src,data.message.musicFile)
    if(data.message === 'stopVision' || data.message ==='startEmergency') restChanges()
    if(data.message === 'playRockPaperGame') handlePlayRockPaperGame()
    if(data.message === 'playPongGame') setTimeout(() => {   handleVideo('pong_game.mp4', 'pongGameModeDone')}, 4000);
    if(data.message ==='danceMode') handleVideo('dancing_robot.mp4', 'danceModeDone')

    try {
        if (typeof data.message === 'object' && data.message !== null) {
            if ('aiAnswer' in data.message) {
                showTextOneByOne(data.message.aiAnswer, transcriptTVPage);
            }
            if ('transcript' in data.message) {
                transcriptTVPage.classList.remove('robotAnswer');
                transcriptTVPage.innerText = data.message.transcript;
            }
        }
    } catch (error) {
        console.log(error)
    }
//    console.log("From page 2",data)
});
