const joystickContainer = document.querySelector('.joystick-container');
const joystick = document.querySelector('.joystick');
const joystickStick = document.querySelector('.joystick-stick');
const coordinatesDisplay = document.querySelector('.coordinates');

let dragging = false;
let containerRect = joystickContainer.getBoundingClientRect();

joystick.addEventListener('mousedown', startDrag);
joystick.addEventListener('touchstart', startDrag);

document.addEventListener('mousemove', drag);
document.addEventListener('touchmove', drag);

document.addEventListener('mouseup', stopDrag);
document.addEventListener('touchend', stopDrag);

var lastMove = 0;

function startDrag(e) {
  e.preventDefault();
  dragging = true;
  containerRect = joystickContainer.getBoundingClientRect(); // Update containerRect on drag start
  lastMove = 0
}

function drag(e) {
  if (!dragging) return;

  const touch = e.touches ? e.touches[0] : e;
  const offsetX = touch.clientX - containerRect.left;
  const offsetY = touch.clientY - containerRect.top;

  const centerX = containerRect.width / 2;
  const centerY = containerRect.height / 2;
  const maxDistance = containerRect.width / 2;

  const dx = offsetX - centerX;
  const dy = offsetY - centerY;
  const distance = Math.min(Math.sqrt(dx * dx + dy * dy), maxDistance);

  const angle = Math.atan2(dy, dx);

  const x = centerX + distance * Math.cos(angle);
  const y = centerY + distance * Math.sin(angle);

  joystick.style.left = `${x}px`;
  joystick.style.top = `${y}px`;

  // Update joystick stick
  joystickStick.style.height = `${distance}px`;
  joystickStick.style.transform = `translateX(-50%) rotate(${angle - Math.PI / 2}rad)`;

  // Joystick output (normalized)
  const normalizedX = (x - centerX) / maxDistance;
  const normalizedY = -(y - centerY) / maxDistance;
  console.log('Joystick position:', { x: normalizedX, y: normalizedY });

  // Update coordinates display
  coordinatesDisplay.textContent = `x: ${normalizedX.toFixed(2)}, y: ${normalizedY.toFixed(2)}`;

  // Send data to server
  if(Date.now() - lastMove > 200) {
    fetch('/joystick', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ x: parseFloat(normalizedX.toFixed(2)), y: parseFloat(normalizedY.toFixed(2)) })
    })
  
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));
  lastMove = Date.now();
  }
}

document.addEventListener('contextmenu', function (e) {
  e.preventDefault();
});

function stopDrag() {
  dragging = false;
  joystick.style.left = '50%';
  joystick.style.top = '50%';
  joystickStick.style.height = '0';
  joystickStick.style.transform = 'translateX(-50%)';
  coordinatesDisplay.textContent = 'x: 0.00, y: 0.00';
  fetch('/joystick', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ x: parseFloat(0), y: parseFloat(0) })
  })
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