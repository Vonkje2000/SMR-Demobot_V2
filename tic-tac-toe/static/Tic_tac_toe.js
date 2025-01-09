const board = document.getElementById('board');
const status = document.getElementById('status');
const restartButton = document.getElementById('restart');
const playersInfo = document.getElementById('players');

// Initialize the board
function initializeBoard(boardState) {
	board.innerHTML = '';
	for (let i = 0; i < 9; i++) {
		const cell = document.createElement('div');
		cell.classList.add('cell');
		cell.dataset.index = i;
		if (boardState && boardState[i] !== ' ') {
			cell.textContent = boardState[i];
			cell.classList.add('taken');
		}
		board.appendChild(cell);
	}
}
		
// Fetch the initial board state when the page loads
async function fetchInitialBoard() {
	const response = await fetch('/restart', { method: 'POST' });
	const data = await response.json();
	initializeBoard(data.board);
	playersInfo.textContent = `X: ${data.x_player}, O: ${data.o_player}`;
	status.textContent = '';
	board.style.pointerEvents = 'auto';
}

// Trigger the robot movement after the board is updated
async function triggerRobotMove(square, player) {
	console.log(`Triggering robot move for player '${player}' at square ${square}.`);
	fetch('/trigger_robot_move', {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify({ square: square, player: player })
	})
	.then(response => response.json())
	.then(data => {
		console.log(`Robot move triggered for player ${player} at square ${square}`); // Log the robot movement status
	});
}

var board_clicked = false

// Handle user clicks
board.addEventListener('click', async (e) => {
	if (board_clicked == true){
		return;
	}
	board_clicked = true
	const cell = e.target;
	const index = cell.dataset.index;

	if (cell.classList.contains('taken')) {
		board_clicked = false; 
		return;
	}

	// Send the move to the server
	const response = await fetch('/make_move', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({ square: parseInt(index) })
	});
	const data = await response.json();

	if (data.error) {
		alert(data.error);
		board_clicked = false;
		return;
	}

	// Update the board
	initializeBoard(data.board);

	// Trigger robot movement for the human move
	await triggerRobotMove(parseInt(index), data.current_letter);
	
	if (data.winner) {
		status.textContent = `${data.winner} wins!`;
		board.style.pointerEvents = 'none';
		board_clicked = false;
		return;
	} else if (data.is_tie) {
		status.textContent = "It's a tie!";
		board.style.pointerEvents = 'none';
		board_clicked = false;
		return;
		
	}

	// Get the computer's move
	const computerResponse = await fetch('/get_move', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		}
	});
	const computerData = await computerResponse.json();

	initializeBoard(computerData.board);

	// Trigger robot movement for the computer move
	await triggerRobotMove(computerData.move, computerData.current_letter);

	if (computerData.winner) {
		status.textContent = `${computerData.winner} wins!`;
		board.style.pointerEvents = 'none';
		board_clicked = false;
		return;
	} else if (computerData.is_tie) {
		status.textContent = "It's a tie!";
		board.style.pointerEvents = 'none';
		board_clicked = false;
		return;
	}
	board_clicked = false;
});

// Handle Restart
restartButton.addEventListener('click', fetchInitialBoard);

//Load the initial board state when the page loads
initializeBoard();
