// Update the board
function update_board(boardState) {
	var cells = document.getElementsByClassName("cell")
	for (let i = 0; i < 9; i++) {
		if (boardState !== undefined && (boardState[i] === 'X' || boardState[i] === 'O')) {
			cells[i].classList.add('taken');
			cells[i].textContent = boardState[i];
		}
		else if (boardState !== undefined && (boardState[i] === '-')) {
			cells[i].classList.add('taken');
			cells[i].textContent = ' ';
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
	document.getElementById('players').innerHTML = 'Game is starting, please wait.';
    const response = await fetch(`/tictactoe/restart/${restart}`, { method: 'POST' });
    const data = await response.json();
    update_board(data.board);
    current_letter = data.current_letter;

    // Replace "Human" with "Player" and wrap in bold tags
    const xPlayer = data.x_player === "Human" ? "<strong>Player</strong>" : data.x_player;
    const oPlayer = data.o_player === "Human" ? "<strong>Player</strong>" : data.o_player;

    // Update players' text using innerHTML to apply bold tags
    document.getElementById('players').innerHTML = `X: ${xPlayer}, O: ${oPlayer}`;
    document.getElementById('status').textContent = '';
    document.getElementById('board').style.pointerEvents = 'auto';
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

	if (data.winner) {
        // Determine winner
        const xPlayer = document.getElementById('players').textContent.includes('X: Player');
        const winnerMessage = data.winner === 'X'
            ? (xPlayer ? 'Player wins!' : 'Computer wins!')
            : (xPlayer ? 'Computer wins!' : 'Player wins!');

        showModal(winnerMessage); // Show modal for winner
        document.getElementById('board').style.pointerEvents = 'none';
        return;
    } else if (data.is_tie) {
        showModal("It's a tie!"); // Show modal for tie
        document.getElementById('board').style.pointerEvents = 'none';
        return;
    }
}


// Show modal with game status
function showModal(message) {
    const modal = document.getElementById('status-modal');
    const statusElement = document.getElementById('status');
    statusElement.textContent = message;
    modal.style.display = 'flex'; // Show the modal
}

var closemodal_run_once = false;

// Close modal
async function closeModal() {
	if (closemodal_run_once === false) {
		closemodal_run_once = true;
		const response = await fetch(`/tictactoe/cleanup`, { method: 'GET' });
		const data = await response.json();
		console.log(data.board);
		update_board(['-','-','-','-','-','-','-','-','-']);

		document.getElementById('mode').textContent = 'Select a mode';
		document.getElementById('players').innerHTML = '';
	
		const modal = document.getElementById('status-modal');
		modal.style.display = 'none'; // Hide the modal
		closemodal_run_once = false;
	}
}
function setup(){
	document.getElementById('board').style.pointerEvents = 'none';
}