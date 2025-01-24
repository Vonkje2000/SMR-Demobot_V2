let startButton = document.getElementById('start-button');
let timerElement = document.getElementById('timer');
let pressTimer;

startButton.addEventListener('mousedown', function() {
  // Stuur een signaal naar de server
  fetch('/rockpaperscissors/start_robot', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ message: 'start button pressed' })
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(data => {
    console.log('Server response:', data);
  })
  .catch(error => console.error('Error sending start signal:', error));

  // Verberg de startknop en toon de timer
  let countdown = 13;
  startButton.style.display = 'none';
  timerElement.style.display = 'block';
  timerElement.textContent = countdown;

  let interval = setInterval(function() {
    countdown--;
    timerElement.textContent = countdown;

    if (countdown <= 0) {
      clearInterval(interval);
      timerElement.textContent = 'Go!';
      // Fetch the image from the Flask backend
      setTimeout(fetchImage, 2500);
    }
  }, 1000);
});

startButton.addEventListener('mouseup', function() {
  clearTimeout(pressTimer);
});

startButton.addEventListener('mouseleave', function() {
  clearTimeout(pressTimer);
});

document.getElementById('language-switch').addEventListener('click', function() {
  let instructionsEn = document.getElementById('instructions-en');
  let instructionsNl = document.getElementById('instructions-nl');
  let instructionsTitle = document.getElementById('instructions-title');
  let languageSwitchButton = document.getElementById('language-switch');

  if (instructionsEn.style.display === 'none') {
    instructionsEn.style.display = 'block';
    instructionsNl.style.display = 'none';
    instructionsTitle.textContent = 'Instructions';
    languageSwitchButton.textContent = 'Switch to Dutch';
  } else {
    instructionsEn.style.display = 'none';
    instructionsNl.style.display = 'block';
    instructionsTitle.textContent = 'Instructies';
    languageSwitchButton.textContent = 'Switch to English';
  }
});

async function fetchImage() {
  console.log('Fetching image...');

  var response = await fetch('/rockpaperscissors/game_result', {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
      },
  })
  .then(response => response.json());
  //document.getElementsByClassName("question")[0].textContent = response.result;
  console.log(response.result);
  var image_path = "";
  if(response.result === "robot"){
    image_path = '/static/images/you_lose.png';
  }
  else if(response.result === "user"){
    image_path = '/static/images/you_win.png';
  }
  else if(response.result === "draw"){
    image_path = '/static/images/draw.png';
  }

  if(image_path !== '') {
  await fetch('/rockpaperscissors/get_captured_image') // Gebruik localhost of 127.0.0.1   get_captured_image
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.blob();
    })
    .then(blob => {
      console.log('Image fetched successfully');
      let img = document.createElement('img');
      img.src = URL.createObjectURL(blob);
      img.alt = 'Captured Hand Gesture';
      let imageContainer = document.getElementById('image-container');
      imageContainer.innerHTML = ''; // Clear any existing content
      imageContainer.appendChild(img);
    })
    .catch(error => console.error('Error fetching image:', error));
	}
	else{
		let imageContainer = document.getElementById('image-container');
    	imageContainer.innerHTML = ''; // Clear any existing content
	}

	if(image_path === ''){
		image_path = '/static/images/No_hand_detected.png';
	}

  if(image_path !== '') {
    await fetch(image_path) // Gebruik localhost of 127.0.0.1   get_captured_image
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.blob();
    })
    .then(blob => {
      let img = document.createElement('img');
      img.src = URL.createObjectURL(blob);
      //img.alt = 'Result';
      let imageContainer = document.getElementById('result-image-container');
      imageContainer.innerHTML = ''; // Clear any existing content
      imageContainer.appendChild(img);

    })
    .catch(error => console.error('Error fetching image:', error));
  }
  else{
	let imageContainer = document.getElementById('result-image-container');
    imageContainer.innerHTML = ''; // Clear any existing content
  }
  	startButton.style.display = 'block';
	timerElement.style.display = 'none';
}

document.addEventListener('contextmenu', function (e) {
  e.preventDefault();
});

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