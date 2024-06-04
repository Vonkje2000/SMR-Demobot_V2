
const socket = io();
socket.on('connect', () => console.log('Connected to the server'));

function sendMessage(message,disableButtonsInHome=true) {
    disableButtons(disableButtonsInHome);
    socket.emit('message', JSON.stringify({message }));
}


function disableButtons(disable = true) {
    document.querySelectorAll('.control-btns, #startBtn').forEach(button => button.disabled = disable);
}

function stopRunningActions(){
    document.querySelectorAll('.control-btns').forEach(btn => {
        if (btn.innerText.includes("Stop") || btn.innerText.includes("started")|| btn.innerText.includes("running")) btn.click();
    });
}
