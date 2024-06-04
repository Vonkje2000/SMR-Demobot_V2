const ROBOT_NAME = 'smart robot'

const MESSAGES = {
    HUMANS_DETECTION: {
        START:'Humans detection process started.',
        STOP:"Humans detection stopped"
    },
    POSE_DETECTION: {
        START:'Pose detection started',
        STOP:"Pose detection stopped"
    },
    EMOTIONS_DETECTION: {
        START:'Detect emotions has been started',
        STOP:"Emotions detection stopped"
    },
    SYSTEM:{
        START:'The system has been activated',
        STOP:"The system has been disactivated"
    },
    EMERGENCY:"Emergency mode started. Please stay away from the robot. The robot is stopping immediately.",
    STOP_EMERGENCY: 'Emergency mode is canceled. Robot tasks have resumed',
    DANCING_MODE:{
        START:"Dancing mode activated! Let's dance and make unforgettable memories together",
        END: "Thanks for dancing with me"
    },
    HI:"Hey human",
    GREETINGS_ANSWER: "I'm fine, thank you for asking!",
    HAPPY_TO_HEAR: "I am happy to hear that",
    PLAY_GAME: 'Let\'s play rock paper scissors game. On count 3 start',
    COUNT123: '1.  2.  3. Go!',
    SAYING_ROBOT_NAME: `My name is ${ROBOT_NAME}`,
    ROBOT_LISTENING:'I am listening',
    ROBOT_NAME,
    STOP_SPEECH: 'Speech Recognition feature has been stopped',
    START_SPEECH: 'Speech Recognition feature has been started',
    TV_MODE: 'Requests have been sent to the both robots to move to tv mode',
    THANKS_RESPONSE  : 'You’re welcome!',
    CREATOR: 'I was created by students at The Hague University, led by software engineer Shiyar Jamo.',
    ORIGIN: 'I\'m from The Hague University in the Netherlands.'
}

const MUSICS = {
    HUMANS_DETECTION: "Corporate.mp3",
    POSE_DETECTION:"3.The Positive Rock(Short Version).wav",
    EMOTIONS_DETECTION:"Get That Feeling - Happy Upbeat Indie Pop (60s).mp3",
    SAD: "Emotional Piano.mp3",
    LAPTOP_TYPING: "TypingEffect.wav",
}


const commandsList = [
    'start system', 'star system',
    'stop system','turn off system','turn off the system',
    'detect people', 'people detect', 'detecting people', 'detection people', 'human detect',
    'pose detection','see how i move','move detection', 'detect move', 'detect pose',
    'stop detect', 'turn off detect',
    `hi ${ROBOT_NAME}`,`hey ${ROBOT_NAME}`,`hello ${ROBOT_NAME}`,
    'how are you','your day','do you do','how is it going','how is going',
    'doing great', 'i am good','doing well','i am great','i am fine',
    'feelings','read my feel','emotion',
    'turn on emergency', 'start emergency', 'call emergency',
    'start dance','start dancing','dance for',
    'start game', 'gaming','play again', 'start again', 'play game', 'playing game',
    'what is your name','who are you',
    'stop speech recognition', 'turn off speech', 'turn off the speech',
    'tv mode', 'mode tv',
    'thanks', 'thank you',
    'who made you','who created you','who built you', 'who is your creator','who designed you','who developed you',
    'where are you from','where you from','where were you made','where were you created', 'where were you built','where is your origin','in which country were you developed',
];

