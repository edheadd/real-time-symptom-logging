from transformers import pipeline
import torch
from process_symptoms import get_symptoms_list

class NLP_model():

    def __init__(self):
        # Load your trained NER model
        model_path = '../saved_biobert_model'  # Uncomment and replace with your model paths
        # Determine whether to use GPU or CPU
        device = 0 if torch.cuda.is_available() else -1
        # Initialize the pipeline with the appropriate device
        self.nlp = pipeline("ner", model=model_path, tokenizer=model_path, device=device)
        
        self.entities = []
        self.filtered_entities = []
        self.matching_entities = []

    def apply_nlp(self, text):
        # Extract entities
        self.entities = self.nlp(text)
        
        self.filtered_entities = [entity for entity in self.entities if len(entity['word']) > 3]
        
        symptoms_list = get_symptoms_list();
        
        # Print matching words
        for entity in self.filtered_entities:
            if entity["word"] in symptoms_list:
                entity["score"] = entity["score"]*1.5
                self.matching_entities.append(entity)
    
    def get_nlp_results(self, text):
        
        self.apply_nlp(text)
        
        to_check = set()
        lowest_score = 1
        
        for entity in self.matching_entities:
            if entity["score"] < lowest_score:
                lowest_score = entity["score"]

        for i in range(len(self.entities)):
            if self.entities[i]['score'] > lowest_score and self.entities[i] in self.filtered_entities:
                to_check.add(self.entities[i]['word'])
                if self.entities[i+1]['score'] > lowest_score and self.entities[i+1] in self.filtered_entities:
                    to_check.add(self.entities[i]['word']+" "+self.entities[i+1]['word'])            
                    to_check.add(self.entities[i+1]['word']+" "+self.entities[i]['word'])
                    
        return to_check