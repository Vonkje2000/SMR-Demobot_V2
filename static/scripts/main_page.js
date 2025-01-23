function setup() {
    const randomNumber = Math.floor(Math.random() * 3) + 1;
    const videoElement = document.getElementById('video');

    if (randomNumber === 1) {
        videoElement.src = "static/videos/SMR1 2024-2025 Promotional Video.mp4";
    } else if (randomNumber === 2) {
        videoElement.src = "static/videos/hhs.mp4";
    } else if (randomNumber === 3) {
        videoElement.src = "static/videos/dancing_robot.mp4";
    }

    videoElement.parentElement.volume = 0.5;
    videoElement.parentElement.load();

    // Start checking the internet connection
    checkInternetStatus();
}

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

