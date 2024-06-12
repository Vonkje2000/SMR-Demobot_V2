
const socket = io();
socket.on('connect', () => console.log('Connected to the server'));

function sendMessage(message) {
    socket.emit('message', JSON.stringify({message }));
}
