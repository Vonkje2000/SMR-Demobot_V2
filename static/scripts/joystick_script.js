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

function startDrag(e) {
  e.preventDefault();
  dragging = true;
  containerRect = joystickContainer.getBoundingClientRect(); // Update containerRect on drag start
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
}

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

var home_button_pressed = false;
async function close_cleanup() {
	if (home_button_pressed === true){
		return;
	}
	home_button_pressed = true;
	while (true){
		var response = await fetch('/Maze_game/cleanup', {
			method: 'POST',
			headers: {
			'Content-Type': 'application/json'
			},
			body: JSON.stringify({message: 'Home button pressed'})
		})
		.then(response => {
			if (!response.ok){
				throw new Error('Network response was not ok');
			}
			return response.json();
		})
		.then(data => {
			console.log('server response:', data);
		})
		.catch(error => console.error('Error sending start signal:', error));

		if(response.status === "success"){
			window.location.href="/index";
			return
		}
	}
}

async function maze_restart() {
	await fetch('/Maze_game/reset', {
		method: 'POST',
		headers: {
		  'Content-Type': 'application/json'
		},
		body: JSON.stringify({message: 'Home button pressed'})
	})
	.then(response => {
		if (!response.ok){
			throw new Error('Network response was not ok');
		}
		return response.json();
	})
	.then(data => {
		console.log('server response:', data);
	})
	.catch(error => console.error('Error sending start signal:', error));
}