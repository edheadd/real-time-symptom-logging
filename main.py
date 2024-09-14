import nlp_module.nlp_model as nlp
import speech_to_text_module.voice_recognizer as vr

def main():
    
    voice_recognizer = vr.voice_recognizer()
    nat_lang_processor = nlp.NLP_model()
    
    text = voice_recognizer.recognize_speech()
    
    
    