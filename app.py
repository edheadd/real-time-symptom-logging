from flask import Flask, render_template, jsonify
import sys, os
import threading  # For non-blocking recording
import nlp_module.nlp_model as nlp

# Add the parent directory (project_root) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now import the voice_recognizer from the speech_to_text_module package
from speech_to_text_module.voice_recognizer import voice_recognizer

app = Flask(__name__)
recognizer = voice_recognizer()
nat_lang_processor = nlp.NLP_model()

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
    nlp_results = nat_lang_processor.get_nlp_results(translated_message)
    # perfrom processing w nlp results
    return jsonify({"nlp_results": nlp_results})

if __name__ == '__main__':
    app.run(debug=False)
