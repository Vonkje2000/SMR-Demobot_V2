let isPaused = false; // Simulate paused state
let resetTimer; // Timer for tracking button hold
const resetHoldTime = 3000; // 3 seconds in milliseconds

// Function to show the reset modal
function showResetModal() {
    const resetModal = document.getElementById('reset-modal');
    resetModal.style.display = 'flex'; // Show the modal
}

// Function to hide the reset modal and reset the game
function resetGame() {
    const resetModal = document.getElementById('reset-modal');
    resetModal.style.display = 'none'; // Hide the modal

    // Simulate unpausing the game (test logic)
    isPaused = false;
    console.log("Game has been unpaused and reset."); // TEST LOG

    // TODO: Replace with actual reset logic
}

// Function to start the reset timer
function startResetTimer() {
    resetTimer = setTimeout(() => {
        resetGame(); // Trigger reset if button is held long enough
    }, resetHoldTime);
    console.log("Hold the button for 5 seconds to reset..."); // TEST LOG
}

// Function to cancel the reset timer
function cancelResetTimer() {
    clearTimeout(resetTimer); // Clear the timer if the button is released early
    console.log("Reset canceled."); // TEST LOG
}
//// //// Commenting this out keeps the function intact but prevents it from running. - TODO
// // Trigger the reset modal when the game is paused (test logic)
// function testPauseTrigger() {
//     isPaused = true; // Simulate the game being paused
//     console.log("Game is now paused."); // TEST LOG

//     if (isPaused) {
//         showResetModal(); // Show the reset modal
//     }
// }

// Attach event listeners for holding the reset button
document.addEventListener("DOMContentLoaded", () => {
    const resetButton = document.getElementById('reset-button');

    // Start the timer when the button is pressed
    resetButton.addEventListener('mousedown', startResetTimer);
    resetButton.addEventListener('touchstart', startResetTimer); // For touch devices

    // Cancel the timer when the button is released or interaction ends
    resetButton.addEventListener('mouseup', cancelResetTimer);
    resetButton.addEventListener('mouseleave', cancelResetTimer); // In case the cursor leaves the button
    resetButton.addEventListener('touchend', cancelResetTimer); // For touch devices
});

/// Commenting this out prevents the modal from appearing after 5 seconds.
// // TEST: Simulate pause trigger after 5 seconds
// setTimeout(testPauseTrigger, 5000);

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

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


//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////



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


 document.addEventListener('contextmenu', function (e) {
    e.preventDefault();
});

document.addEventListener("selectstart", function (e) {
    e.preventDefault(); // Prevent text selection
    console.log("Text selection disabled"); // Optional: Debug message
});
