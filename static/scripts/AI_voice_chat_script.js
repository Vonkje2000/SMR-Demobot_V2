var listen_interval;

function start_listen() {
	if(!listen_interval){
		fetch('/API', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
    		},
    		body: JSON.stringify({listen_button:'true'})
		})
		.then(response => response.json())
		.then(data => console.log(data))
		.catch(error => console.error('Error:', error));

		var fetchInterval = 2000;
		listen_interval = setInterval(message_status, fetchInterval);
		document.getElementById("Listen_button").style.setProperty('--btn-color', 'red');

		document.getElementsByClassName("question")[0].textContent = "...";
		document.getElementsByClassName("question")[0].style.visibility = "visible";
		document.getElementsByClassName("AI_response")[0].textContent = "...";
		document.getElementsByClassName("AI_response")[0].style.visibility = "hidden";
	}
}

function dutch_button(){
	if(!listen_interval){
	document.getElementById("language_text").textContent = "Wijzig de taal";
	document.getElementById("Listen_button").textContent = "Start Chat";
	document.getElementById("Home_button").textContent = "Terug naar Start";
	document.getElementById("Promobot_Titel").textContent = "Smart Manufacturing & Robotics Minor Vertegenwoordiger";
	
	// Hide the English button and keep the Dutch button visible
	document.getElementById("Dutch_button").style.display = "none";
	document.getElementById("English_button").style.display = "inline-block";
	fetch('/API', {
		method: 'POST',
		headers: {
		  'Content-Type': 'application/json'
		},
		body: JSON.stringify({Language:'Dutch'})
	  })
	  .then(response => response.json())
	  .then(data => console.log(data))
	  .catch(error => console.error('Error:', error));
	}
}

function english_button(){
	if(!listen_interval){
	document.getElementById("language_text").textContent = "Change the language";
	document.getElementById("Listen_button").textContent = "Start Chat";
	document.getElementById("Home_button").textContent = "Back to Home";
	document.getElementById("Promobot_Titel").textContent = "Smart Manufacturing & Robotics Minor Representative";
	
	// Hide the Dutch button and keep the English button visible
	document.getElementById("English_button").style.display = "none";
	document.getElementById("Dutch_button").style.display = "inline-block";
	
	fetch('/API', {
		method: 'POST',
		headers: {
		  'Content-Type': 'application/json'
		},
		body: JSON.stringify({Language:'English'})
	  })
	  .then(response => response.json())
	  .then(data => console.log(data))
	  .catch(error => console.error('Error:', error));
	}
}

/* would this work better? something chat gpt sugested.
function get_language(){
	fetch('/API', {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json'
		  }
	})
	.then(response => response.json())
	.then(data => console.log(data))
	.catch(error => console.error('Error:', error));
}*/

function get_language(){
	fetch('/API', {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json'
		  },
		  body: JSON.stringify({data:'messages'})
	})
	.then(response => response.json())
	.then(data => console.log(data))
	.catch(error => console.error('Error:', error));
}

async function message_status() {
	var response = await fetch('/API', {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json'
		  },
	})
	.then(response => response.json());
	//console.log(response);
	if(response.question!= "..."){
		document.getElementsByClassName("question")[0].textContent = response.question;
		document.getElementsByClassName("AI_response")[0].innerHTML = response.AI_answer.replace(/\n/g, '<br>');
		document.getElementsByClassName("question")[0].style.visibility = "visible";

		document.getElementsByClassName("AI_response")[0].textContent = "...";
		document.getElementsByClassName("AI_response")[0].style.visibility = "visible";
	}

	if (response.AI_answer != "..."){
		document.getElementsByClassName("AI_response")[0].textContent = response.AI_answer;
		document.getElementsByClassName("AI_response")[0].innerHTML = response.AI_answer.replace(/\n/g, '<br>');
		document.getElementsByClassName("AI_response")[0].style.visibility = "visible";
		clearInterval(listen_interval);
		listen_interval = undefined;
		document.getElementById("Listen_button").style.setProperty('--btn-color', '#2a2929e6');
	}
}

var inactivityTime = function () {
    var time;
    window.onload = resetTimer;
    // DOM Events
    document.onclick = resetTimer;

    function logout() {
		console.log("trigger");
		document.location.href = "/";
    }

    function resetTimer() {
        clearTimeout(time);
        time = setTimeout(logout, 120*1000)
    }
};

document.addEventListener('contextmenu', function (e) {
    e.preventDefault();
});

function setup(){
	dutch_button()

	document.getElementsByClassName("question")[0].style.visibility = "hidden";
	document.getElementsByClassName("AI_response")[0].style.visibility = "hidden";
	inactivityTime();
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