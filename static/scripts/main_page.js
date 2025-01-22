function setup(){
    const randomNumber = Math.floor(Math.random() * 3) + 1;
    if (randomNumber === 1){document.getElementById('video').src = "static/videos/SMR1 2024-2025 Promotional Video.mp4"}
    else if (randomNumber === 2){document.getElementById('video').src = "static/videos/hhs.mp4"}
    else if (randomNumber === 3){document.getElementById('video').src = "static/videos/dancing_robot.mp4"}
    
    document.getElementById('video').parentElement.volume = 0.5;
    document.getElementById('video').parentElement.load();

}


document.addEventListener('contextmenu', function (e) {
    e.preventDefault();
});

