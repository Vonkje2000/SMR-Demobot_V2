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

    // Start checking the internet connection
    checkInternetStatus();

function checkInternetStatus() {
    const aiButton = document.getElementById('ai-button');

    if (!aiButton) {
        console.error("AI button not found. Check the element's ID.");
        return;
    }

    async function updateButtonStatus() {
        try {
            const response = await fetch('/internet_status');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            if (data.connected) {
                aiButton.removeAttribute('disabled'); // Enable button
                aiButton.href = "AI_voice_chat"; // Set proper link
                aiButton.style.pointerEvents = 'auto'; // Allow interaction
                aiButton.style.opacity = 1; // Full visibility
            } else {
                aiButton.setAttribute('disabled', 'true'); // Disable button
                aiButton.href = "#"; // Block navigation
                aiButton.style.pointerEvents = 'none'; // Block interaction
                aiButton.style.opacity = 0.5; // Reduce visibility
            }
        } catch (error) {
            console.error("Error checking internet status:", error);
            // Fallback: Assume no internet if request fails
            aiButton.setAttribute('disabled', 'true');
            aiButton.href = "#";
            aiButton.style.pointerEvents = 'none';
            aiButton.style.opacity = 0.5;
        }
    }

    // Initial check and set interval for periodic updates
    updateButtonStatus();
    setInterval(updateButtonStatus, 2000); // Poll every 2 seconds
}

document.addEventListener("DOMContentLoaded", () => {
    const fullscreenButton = document.getElementById("fullscreen-button");
    const fullscreenKey = "persistentFullscreen"; // LocalStorage key
  
    // Check if the screen is in fullscreen mode
    function isFullscreen() {
        return (
            document.fullscreenElement ||
            document.webkitFullscreenElement ||
            document.mozFullScreenElement ||
            document.msFullscreenElement ||
            (window.innerHeight === screen.height && window.innerWidth === screen.width) // Manual detection
        );
    }
  
    // Toggle fullscreen mode
    function toggleFullscreen() {
        if (!isFullscreen()) {
            if (document.documentElement.requestFullscreen) {
                document.documentElement.requestFullscreen();
            } else if (document.documentElement.webkitRequestFullscreen) {
                document.documentElement.webkitRequestFullscreen();
            } else if (document.documentElement.mozRequestFullScreen) {
                document.documentElement.mozRequestFullScreen();
            } else if (document.documentElement.msRequestFullscreen) {
                document.documentElement.msRequestFullscreen();
            }
            // Mark fullscreen as persistent
            localStorage.setItem(fullscreenKey, "true");
        } else {
            if (document.exitFullscreen) {
                document.exitFullscreen();
            } else if (document.webkitExitFullscreen) {
                document.webkitExitFullscreen();
            } else if (document.mozCancelFullScreen) {
                document.mozCancelFullScreen();
            } else if (document.msExitFullscreen) {
                document.msExitFullscreen();
            }
            // Remove persistent fullscreen marker
            localStorage.removeItem(fullscreenKey);
        }
    }
  
    // Update the visibility of the fullscreen button
    function updateFullscreenButton() {
        if (!isFullscreen()) {
            fullscreenButton.style.display = "flex";
        } else {
            fullscreenButton.style.display = "none";
        }
    }
  
    // Re-enter fullscreen mode if persistentFullscreen is set
    function checkPersistentFullscreen() {
        if (localStorage.getItem(fullscreenKey) === "true" && !isFullscreen()) {
            toggleFullscreen();
        }
    }
  
    // Periodically check for fullscreen state (to handle F11 or manual changes)
    setInterval(updateFullscreenButton, 500);
  
    // Attach the toggle fullscreen function to the button
    fullscreenButton.addEventListener("click", toggleFullscreen);
  
    // Listen for fullscreen change events
    document.addEventListener("fullscreenchange", updateFullscreenButton);
    document.addEventListener("webkitfullscreenchange", updateFullscreenButton); // Safari/Chrome
    document.addEventListener("mozfullscreenchange", updateFullscreenButton); // Firefox
    document.addEventListener("MSFullscreenChange", updateFullscreenButton); // IE/Edge
  
    // Check persistent fullscreen on page load
    checkPersistentFullscreen();
  
    // Initial check
    updateFullscreenButton();
  });