// Add an event listener to autoplay the next video when the current one ends
document.getElementById('video').parentElement.addEventListener('ended', setup);

let lastPlayedQueue = [];

function setup() {
    const videoElement = document.getElementById('video');
    let randomNumber;

    // Generate a random number not in the last 4 played
    do {
        randomNumber = Math.floor(Math.random() * 8) + 1;
    } while (lastPlayedQueue.includes(randomNumber));

    // Update the queue
    lastPlayedQueue.push(randomNumber);
    if (lastPlayedQueue.length > 4) {
        lastPlayedQueue.shift(); // Remove the oldest number to maintain queue size
    }

    if (randomNumber === 1) {
        videoElement.src = "static/videos/Comp1.mp4";
    } else if (randomNumber === 2) {
        videoElement.src = "static/videos/hhs.mp4";
    } else if (randomNumber === 3) {
        videoElement.src = "static/videos/Comp2.mp4";
    }  else if (randomNumber === 4) {
        videoElement.src = "static/videos/Comp3.mp4";
    } else if (randomNumber === 5) {
        videoElement.src = "static/videos/Comp4.mp4";
    } else if (randomNumber === 6) {
        videoElement.src = "static/videos/Comp5.mp4";
    } else if (randomNumber === 7) {
        videoElement.src  = "static/videos/Comp6.mp4";
    } else if (randomNumber === 8) {
        videoElement.src = "static/videos/Comp7.mp4";
    }
  
    videoElement.parentElement.volume = 0.5;
    videoElement.parentElement.load();
}


