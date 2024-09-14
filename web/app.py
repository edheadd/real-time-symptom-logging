from flask import Flask, render_template, jsonify
import sys, os
import threading  # For non-blocking recording

# Add the parent directory (project_root) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now import the voice_recognizer from the speech_to_text_module package
from speech_to_text_module.voice_recognizer import voice_recognizer

app = Flask(__name__)
recognizer = voice_recognizer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_recording', methods=['POST'])
def start_recording():
    # Run the recording process in a separate thread so it's non-blocking
    threading.Thread(target=recognizer.start_recording).start()
    return jsonify({"message": "Recording started."})

@app.route('/stop_recording', methods=['POST'])
def stop_recording():
    # Stop the recording and process the audio
    recognizer.stop_recording()
    translated_message = recognizer.recognize_speech()
    return jsonify({"message": translated_message})

if __name__ == '__main__':
    app.run(debug=False)
