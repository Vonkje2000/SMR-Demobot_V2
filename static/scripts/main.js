


const visionDetectionBTN = document.getElementById('visionDetectionBTN');
const poseDetectionBTN = document.getElementById('poseDetectionBTN');
const emotionDetectionBTN = document.getElementById('emotionDetectionBTN');

const videoFeed = document.getElementById('videoFeed');
const staticImage = document.getElementById('staticImage');
const spinners = document.getElementById('spinners');
const startBtn = document.getElementById('startBtn');
const music = document.getElementById('music');

visionDetectionBTN.addEventListener('click', () => toggleDetection('AI: Detect People', '/objects_detection', visionDetectionBTN));
poseDetectionBTN.addEventListener('click', () => toggleDetection('AI: Seeing how you move', '/pose_detection', poseDetectionBTN));
emotionDetectionBTN.addEventListener('click', () => toggleDetection('AI: Detect emotions', '/pose_detection', poseDetectionBTN));

function toggleDetection(detectText, src, btn) {
    music.pause()
    spinners.style.display = 'block';
    if(videoFeed.style.display=='none'){
        sendMessage('voice', 'humen_detection_started')
        videoFeed.style.display = 'block'
        videoFeed.style.position = 'absolute'
        videoFeed.src = src
        btn.innerText = 'Stop Detection'
        staticImage.style.display = 'none'
    
        disableButtons()
            setTimeout(() => {   
                sendMessage('voice', 'move')
                setTimeout(() => {
                    if (detectText.includes('move')) {  music.play()}
                }, 8000);   
                btn.disabled = false;
            }, 6000);
        
    }else{
        sendMessage('voice', 'humen_detection_stopped')
        videoFeed.style.display = 'none'
        videoFeed.src = ''
        btn.innerText = detectText
        staticImage.style.display = 'block'
        disableButtons(false)
    }

    videoFeed.onload = ()=>{ spinners.style.display = 'none';videoFeed.style.position = 'unset'}
    videoFeed.onerror = ()=> { spinners.style.display = 'none'; videoFeed.style.position = 'unset'};
}

const danceBTN = document.getElementById('danceBTN');
const dancingVideo = document.getElementById('dancingVideo');

danceBTN.addEventListener('click', ()=>{
    disableButtons(true)
    sendMessage('robot', 'dancing_started')
    videoFeed.style.display = 'none'
    staticImage.style.display = 'none'
    dancingVideo.style.display = 'block'
    dancingVideo.src = '/static/videos/dancing_robot.mp4'
    setTimeout(() => {
        dancingVideo.play()
    }, 6000);

    // Event listener for when the video finishes
    dancingVideo.onended = function() {
        disableButtons(false)
        sendMessage('robot', 'dancing_ended');

        dancingVideo.style.display = 'none';
        staticImage.style.display = 'block'; 
    };

})


const playGameBTN = document.getElementById('playGameBTN');
playGameBTN.addEventListener('click', ()=>{
    sendMessage('robot', 'game_started')
})


function disableButtons(disable = true) {
    const buttons = document.querySelectorAll('.control-btns'); // Selects all buttons with class 'control-btns'
    buttons.forEach(button => {
        button.disabled = disable; 
    });
}


function handleStartStop() {
    disableButtons(false)
    music.pause()
    dancingVideo.style.display = 'none'
    dancingVideo.pause()
    if(startBtn.innerText.includes('Start')){
      
        sendMessage('voice', 'active_system')
        startBtn.innerText = 'Stop System'
        setTimeout(() => {
            document.querySelectorAll('.control-btns').forEach(btn => btn.style.display = 'block');
            document.getElementById('startBtn').style.display = 'block';
        }, 2000);
    }else{
        startBtn.innerText = 'Start System'
        sendMessage('voice', 'deactivate_system')
        staticImage.style.display = 'block'
        document.querySelectorAll('.control-btns').forEach(btn => btn.style.display = 'none');
        videoFeed.style.display = 'none'
    }

} 


var socket = io();

socket.on('connect', function() {
    console.log('Connected to the server');
});

socket.on('response', function(data) {
    console.log('Received data:', data);
    disableButtons(false)
    // You can update the DOM or perform actions based on received data
});

function sendMessage(type,message) {
    disableButtons(true)
    socket.emit('message',JSON.stringify({type,message}));
}

