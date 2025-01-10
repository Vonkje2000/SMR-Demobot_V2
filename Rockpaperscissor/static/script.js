let startButton = document.getElementById('start-button');
let timerElement = document.getElementById('timer');
let countdown = 3;
let pressTimer;

startButton.addEventListener('mousedown', function() {
  pressTimer = setTimeout(function() {
    // Verberg de startknop en toon de timer
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
        fetchImage();
      }
    }, 1000);
  }, 150); // 2 seconden ingedrukt houden
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

function fetchImage() {
  console.log('Fetching image...');
  fetch('http://127.0.0.1:5000/get_image') // Gebruik localhost of 127.0.0.1
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