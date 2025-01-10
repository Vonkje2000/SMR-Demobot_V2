// Update the board
function update_board(boardState) {
	var cells = document.getElementsByClassName("cell")
	for (let i = 0; i < 9; i++) {
		if (boardState !== undefined && (boardState[i] === 'X' || boardState[i] === 'O')) {
			cells[i].classList.add('taken');
			cells[i].textContent = boardState[i];
		}
		else{
			cells[i].classList.remove('taken');
			cells[i].textContent = ' ';
		}
	}
}

// Fetch the initial board state when the page loads
var current_letter;
async function start_game(restart, mode_text) {
	document.getElementById('mode').textContent = mode_text;
	const response = await fetch(`/tictactoe/restart/${restart}`, { method: 'POST' });
	const data = await response.json();
	update_board(data.board);
	current_letter = data.current_letter;
	document.getElementById('players').textContent = `X: ${data.x_player}, O: ${data.o_player}`;
	document.getElementById('status').textContent = '';
	document.getElementById('board').style.pointerEvents = 'auto';
}

// Trigger the robot movement after the board is updated
async function triggerRobotMove(square, player) {
	//console.log(`Triggering robot move for player '${player}' at square ${square}.`);
	fetch('/tictactoe/trigger_robot_move', {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify({ square: square, player: player })
	})
	.then(response => response.json())
	.then(data => {
		//console.log(`Robot move triggered for player ${player} at square ${square}`); // Log the robot movement status
	});
}

// Handle user clicks
async function player_move(i){
	document.getElementById('board').style.pointerEvents = 'none';
	const cell = document.getElementsByClassName("cell")[i];
	cell.classList.add('taken');
	cell.textContent = current_letter;
	
	await move("make",i);
	if(document.getElementById('status').textContent == ''){
		await move("get",69);
	}

	document.getElementById('board').style.pointerEvents = 'auto';
}

async function move(type, index){
	// Send the move to the server	#TODO should be get
	response = await fetch(`/tictactoe/move/${type}`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({ square: parseInt(index) })
	});
	data = await response.json();

	// Update the board
	update_board(data.board);

	// Trigger robot movement
	await triggerRobotMove(data.move, data.current_letter);

	if (data.winner) {
		document.getElementById('status').textContent = `${data.winner} wins!`;
		document.getElementById('board').style.pointerEvents = 'none';
		return;
	} else if (data.is_tie) {
		document.getElementById('status').textContent = "It's a tie!";
		document.getElementById('board').style.pointerEvents = 'none';
		return;
	}
}

function setup(){
	document.getElementById('board').style.pointerEvents = 'none';
	if(document.getElementById("players").textContent === ''){
		start_game('EASY',  'EASY MODE');
	}
}