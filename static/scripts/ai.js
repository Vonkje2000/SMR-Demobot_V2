let lastTaskDone = true
const transcript=  document.getElementById('transcript')
const models = ['gpt-4o','gpt-4-turbo', 'gpt-3.5-turbo' ]
function useAiToGetAnswer(text) {
    lastTaskDone = false
    console.log("request sent to ai", text)
    music.src = `/static/music/${MUSICS.LAPTOP_TYPING}`
    music.play()
    fetch('https://api.openai.com/v1/chat/completions', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer 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`
        },
        body: JSON.stringify({
            model: models[2],
            messages: [{ role: 'user', content: `${text}, in less then 150 characters and text as human talking.` }],
            max_tokens: 150
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.choices[0])
        // responseDiv.innerText = data.choices[0].text.trim();
        music.pause()
        const aiAnswer = data.choices[0].message.content.trim().replaceAll("OpenAI", MESSAGES.ROBOT_NAME)
        speak(aiAnswer, ()=>{
            transcript.innerText = ''
            lastTaskDone=true;
            startListening = false;
        })
        showTextOneByOne(aiAnswer,transcript)
    })
    .catch(error => {
        console.log('Error:', error);
    });
}


function showTextOneByOne(text, element, speed = 100) {
    const words = text.split(' ');
    let index = 0;
    element.innerText = '';  // Clear the element initially
    const interval = setInterval(() => {
        if (index >= words.length) clearInterval(interval);
        else element.innerText += ' ' +words[index++] + ' ';
    }, speed);
}
