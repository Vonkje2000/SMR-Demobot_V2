
function showTextOneByOne(text, element, speed = 150) {
    element.classList.add('robotAnswer')
    element.innerText = '';  // Clear the element initially
    const words = text.split(' ');
    let index = 0;

    const interval = setInterval(() => {
        if (index >= words.length){ 
            clearInterval(interval); 
        }
        else element.innerText += ' ' +words[index++] + ' ';
    }, speed);
}


function showOptions(on = true){
    document.querySelectorAll('.control-btns').forEach(btn => btn.style.display = on?'block':'none');
}

function disableButtons(disable = true) {
    document.querySelectorAll('.control-btns, #startBtn').forEach(button => button.disabled = disable);
}

function stopRunningActions(){
    document.querySelectorAll('.control-btns').forEach(btn => {
        if (btn.innerText.includes("Stop") || btn.innerText.includes("started")|| btn.innerText.includes("running")) btn.click();
    });
}
