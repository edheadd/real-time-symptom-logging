from flask import Flask, render_template, jsonify
import sys, os
import threading  # For non-blocking recording
import nlp_module.nlp_model as nlp
import nlp_module.process_symptoms as ps

# Add the parent directory (project_root) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now import the voice_recognizer from the speech_to_text_module package
from speech_to_text_module.voice_recognizer import voice_recognizer

app = Flask(__name__)
recognizer = voice_recognizer()
nat_lang_processor = nlp.NLP_model()
symptom_processor = nat_lang_processor.symp_process

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
    output = nlp_processing(translated_message)
    return jsonify({"message": output})

def nlp_processing(text):
    nlp_results = nat_lang_processor.get_nlp_results(text)
    nlp_results = list(nlp_results)
    output_str = ''
    for result in nlp_results:
        formal_result = symptom_processor.formalize_symptoms(result)
        if formal_result is not None: output_str = output_str + formal_result
    return output_str

if __name__ == '__main__':
    app.run(debug=False)
