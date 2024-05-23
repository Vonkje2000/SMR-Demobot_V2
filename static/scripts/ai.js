let lastTaskDone = true
const transcript=  document.getElementById('transcript')

function useAiToGetAnswer(text) {
    lastTaskDone = false
    console.log("request sent to ai", text)
    transcript.innerText = 'Thinking ...'
    fetch('https://api.openai.com/v1/completions', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer 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`
        },
        body: JSON.stringify({
            model: 'gpt-3.5-turbo-instruct',
            // prompt:`${text}? answer in English`,
            prompt:`Answer briefly: ${text} `,
            max_tokens: 150
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.choices[0])
        // responseDiv.innerText = data.choices[0].text.trim();
        const aiAnswer = data.choices[0].text.trim().replaceAll("OpenAI", MESSAGES.ROBOT_NAME)
        speak(aiAnswer, ()=>{
            lastTaskDone=true;
            transcript.innerText = ''
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
