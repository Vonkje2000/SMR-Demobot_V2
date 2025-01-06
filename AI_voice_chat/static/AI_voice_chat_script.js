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
	}
}

function dutch_button(){
	document.getElementById("language_text").textContent = "Geselecteerde taal: Nederlands";
	document.getElementById("Listen_button").textContent = "Begin Met Praten";
	document.getElementById("Home_button").textContent = "Terug naar Start";
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

function english_button(){
	document.getElementById("language_text").textContent = "Selected Language: English";
	document.getElementById("Listen_button").textContent = "Start Talking";
	document.getElementById("Home_button").textContent = "Back to Home";
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
	document.getElementsByClassName("question")[0].textContent = response.question;
	document.getElementsByClassName("AI_response")[0].textContent = response.AI_answer;
	if (response.AI_answer != "..."){
		clearInterval(listen_interval);
		listen_interval = undefined;
	}
}

function setup(){
	english_button();
}