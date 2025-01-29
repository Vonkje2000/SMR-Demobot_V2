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


var home_button_pressed = false;
async function home_button(){
	if (home_button_pressed === true){
		return;
	}
	home_button_pressed = true;
	while (true){
		var response = await fetch('/rockpaperscissors/state', {
			method: 'GET',
			headers: {
			  'Content-Type': 'application/json'
			},
		})
		.then(response => {
			if (!response.ok){
				throw new Error('Network response was not ok');
			}
			return response.json();
		})
		.catch(error => console.error('Error sending start signal:', error));
		//console.log(response)
	
		if(response.status === "none"){
			window.location.href="/index";
			return
		}
	}
}
