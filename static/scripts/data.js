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
    EMERGENCY:"Emergency mode started, Please stay away from the robot. Robot stopping immediately. ",
    DANCING_MODE:{
        START:"Dancing mode activated! Let's dance and make unforgettable memories together",
        END: "Thanks for dancing with me"
    },
    HI:"Hey human",
    GREETINGS_ANSWER: "I am doing great, and I hope you are too.",
    HAPPY_TO_HEAR: "I am happy to hear that",
    PLAY_GAME: 'Let\'s play rock paper scissors game. On count 3 start',
    COUNT123: '1.  2.  3. Go!',
    SAYING_ROBOT_NAME: `My name is ${ROBOT_NAME}`,
    ROBOT_LISTENING:'I am listening',
    ROBOT_NAME,
    STOP_SPEECH: 'Speech Recognition feature has been stopped',
    START_SPEECH: 'Speech Recognition feature has been started',
    TV_MODE: 'Requests have been sent to the both robots to move to tv mode',
    THANKS_RESPONSE  : 'You’re welcome!'
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
    'detect people', 'people detect', 'detecting people', 'detection people',
    'pose detection','see how i move','move detection', 'detect move', 'detect pose',
    'stop detect', 'turn off detect',
    `hi ${ROBOT_NAME}`,`hey ${ROBOT_NAME}`,`hello ${ROBOT_NAME}`,
    'how are you','your day','do you do','how is it going','how\'s it going','how is going',
    'doing great', 'good','doing well',
    'feelings','read my feel','emotion',
    'turn on emergency', 'start emergency', 'call emergency',
    'start dance','start dancing','dance for',
    'start game', 'gaming','play again', 'start again', 'play game', 'playing game',
    'what is your name','what\'s your name',
    'stop speech recognition', 'turn off speech', 'turn off the speech',
    'tv mode', 'mode tv',
    'thanks', 'thank you'
];

