
import pyttsx3
import pygame

def get_engine():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # Adjust index if needed
    engine.setProperty('rate', 120)
    engine.setProperty('volume', 1)
    return engine

def say(text):
    engine = get_engine()
    engine.say(text)
    try:
        engine.runAndWait()
    except Exception as e:
        print('Error in text-to-speech:', e)
    finally:
        engine.stop()


def play_sound(sound_file):
    # Initialize Pygame
    pygame.init()

    # Load the sound
    click_sound = pygame.mixer.Sound(sound_file)

    # Play the sound
    click_sound.play()

    # Keep the script running long enough for the sound to play
    pygame.time.wait(int(click_sound.get_length() * 1000))
