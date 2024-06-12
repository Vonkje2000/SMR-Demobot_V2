const transcriptHomePage= document.getElementById('transcriptHomePage')
let aiTaskRunning = false
const models = ['gpt-4o','gpt-4-turbo', 'gpt-3.5-turbo' ]

function useAiToGetAnswer(text) {
    aiTaskRunning = true
    music.src = `/static/music/${MUSICS.LAPTOP_TYPING}`
    music.play()
    fetch('https://api.openai.com/v1/chat/completions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer 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`},
        body: JSON.stringify({
            model: models[2], max_tokens: 150,
            messages: [{ role: 'user', content: `${text}, in less then 150 characters and text must be understand for beginners in English.` }],
        })
    })
    .then(response => response.json())
    .then(data => {
        const aiAnswer = data.choices[0].message.content.trim().replaceAll("OpenAI", MESSAGES.ROBOT_NAME)
        handleAIAnswer(aiAnswer)
        sendMessage({aiAnswer})
    })
    .catch(error => {
        console.log('Error:', error);
    });
}

function handleAIAnswer(aiAnswer){
    music.pause()
    speak(aiAnswer, ()=>{
        setTimeout(() => {
            aiTaskRunning = false;        
            startListening = false;
        }, 2000);
    })
    showTextOneByOne(aiAnswer,transcriptHomePage)
}
