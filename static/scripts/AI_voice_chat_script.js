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
	document.getElementById("language_text").textContent = "Geselecteerde taal: Nederlands";
	document.getElementById("Listen_button").textContent = "Begin Met Praten";
	document.getElementById("Home_button").textContent = "Terug naar Start";
	document.getElementById("Promobot_Titel").textContent = "Smart Manufacturing & Robotics Minor Vertegenwoordiger";
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
	document.getElementById("language_text").textContent = "Selected Language: English";
	document.getElementById("Listen_button").textContent = "Start Talking";
	document.getElementById("Home_button").textContent = "Back to Home";
	document.getElementById("Promobot_Titel").textContent = "Smart Manufacturing & Robotics Minor Representative";
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

function setup(){
	dutch_button();
	document.getElementsByClassName("question")[0].style.visibility = "hidden";
	document.getElementsByClassName("AI_response")[0].style.visibility = "hidden";
}