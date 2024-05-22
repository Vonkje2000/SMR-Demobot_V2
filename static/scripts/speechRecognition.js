
const commandsList = [
    'start system',
    'stop system',
    'detect people', 'people detect', 'detecting people', 'detection people',
    // 'detect objects', 'objects detect', 'detection objects',
    'stop detect'
];

function executeTasks(command) {
    const isSystemStarted = startBtn.innerText.includes("Stop");

    switch (command) {
        case 'start system':
            if (!isSystemStarted) startBtn.click();
            break;

        case 'stop system':
            if (isSystemStarted) startBtn.click();
            break;

        case 'detect people':
        case 'people detect':
        case 'detecting people':
        case 'detection people':
            if (objectsDetectionBTN.innerText.includes("AI")) objectsDetectionBTN.click();
            break;

        // case 'detect objects':
        // case 'objects detect':
        // case 'detection objects':
        //     if (objectsDetectionBTN.innerText.includes("AI")) objectsDetectionBTN.click();
        //     break;

        case 'stop detect':
            document.querySelectorAll('.control-btns').forEach(btn => {
                if (btn.innerText.includes("Stop")) {
                    console.log("match", btn.innerText);
                    btn.click();
                } else {
                    console.log("no match", btn.innerText);
                }
            });
            break;

        default:
            console.log(`Command "${command}" not recognized.`);
            break;
    }
}
function startContinuousRecognition() {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'en-US';
    recognition.interimResults = true;  // Enable interim results
    recognition.continuous = true;

    recognition.onresult = (event) => {
        const results = Array.from(event.results);
        const interimResult = results.filter(result => !result.isFinal).map(result => result[0].transcript.toLowerCase().trim().replace("  "," ")).join(' ');

        console.log(`Interim transcript: ${interimResult}`);
    
        const checkAndExecute = (transcript) => {
            for (let command of commandsList) {
                if (transcript.includes(command)) {
                    console.log(`Command sent: ${command}`);
                    executeTasks(command);
                    break;
                }
            }
        };
        
        if (interimResult.trim()) {
            checkAndExecute(interimResult.trim());
        }
    };
    
    recognition.onerror = (event) => { console.error(`Recognition error: ${event.error}`);};

    recognition.onend = () => {
        console.log('Speech recognition service disconnected');
        setTimeout(() => {
            recognition.start(); // Restart recognition with a slight delay to prevent immediate end/start loop
        }, 100);
    };

    recognition.start();
}

startContinuousRecognition();