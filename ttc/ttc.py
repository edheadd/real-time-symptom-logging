import sounddevice as sd
import numpy as np
import speech_recognition as sr
import pyttsx3

# Initialize the recognizer and speech engine
r = sr.Recognizer()
engine = pyttsx3.init()

# Function to convert text to speech
def SpeakText(command):
    engine.say(command)
    engine.runAndWait()

# Function to capture audio using sounddevice and convert it to text
def recognize_audio():
    samplerate = 16000  # Sample rate (Google's default is 16000)
    duration = 5  # Duration to record (in seconds)
    
    # Record audio using sounddevice
    print("Listening...")
    audio = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()  # Wait until the recording is finished
    audio = np.squeeze(audio)  # Remove unnecessary dimensions
    
    # Convert audio to recognizer-friendly format
    audio_data = sr.AudioData(audio.tobytes(), samplerate, 2)
    
    try:
        # Recognize the audio using Google Web Speech API
        text = r.recognize_google(audio_data)
        print(f"Did you say: {text}")
        SpeakText(text)
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio")

# Main loop
while True:
    recognize_audio()
