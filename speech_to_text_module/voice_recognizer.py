import sounddevice as sd
import speech_recognition as sr
import numpy as np
import keyboard  # To detect key press

class voice_recognizer:
    def __init__(self, samplerate=16000, channels=1, dtype='int16'):
        self.r = sr.Recognizer()
        self.samplerate = samplerate
        self.channels = channels
        self.dtype = dtype
        self.recorded_audio = []

    def record_audio(self):
        """Start recording audio until the 's' key is pressed."""
        print("Listening... Press 's' to stop recording.")
        with sd.InputStream(samplerate=self.samplerate, channels=self.channels, dtype=self.dtype) as stream:
            while True:
                if keyboard.is_pressed('s'):
                    print("\n'S' key pressed. Stopping recording...")
                    break  # Stop recording when 's' key is pressed
                
                # Read small chunks of audio data
                audio_chunk, overflowed = stream.read(1024)
                if overflowed:
                    print("Audio overflow occurred.")
                self.recorded_audio.append(audio_chunk)

    def process_audio(self):
        """Process the recorded audio into a recognizable format."""
        if self.recorded_audio:
            # Concatenate all recorded chunks
            recorded_audio = np.concatenate(self.recorded_audio, axis=0)
            # Convert the concatenated audio into an AudioData object
            return sr.AudioData(recorded_audio.tobytes(), self.samplerate, 2)
        return None

    def recognize_speech(self):
        """Recognize the speech from the processed audio."""
        audio_data = self.process_audio()
        if audio_data:
            try:
                # Recognize speech using Google Web Speech API
                text = self.r.recognize_google(audio_data)
                return text
            except sr.RequestError as e:
                print(f"API error: {e}")
            except sr.UnknownValueError:
                print("Sorry, I could not understand the audio.")
        return ""
