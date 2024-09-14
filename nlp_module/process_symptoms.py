import pandas as pd
import re

class symptoms():
    
    def __init__(self):
        pass
    
    def get_symptoms_list(self):
        # Create a set to avoid duplicates
        symptoms_set = set()
        
        df = pd.read_csv('symptoms.csv', header=None, names=['primary_name', 'consumer_name', 'synonyms'])

        df['primary_name'].apply(lambda x: symptoms_set.update(self.extract_words(x)))

        # Process 'synonyms'
        df['synonyms'].apply(lambda x: symptoms_set.update(self.extract_words(str(x).strip("[]").replace("'", ""))))

        # Convert the set to a list for output
        symptoms_list = list(symptoms_set)

        # Remove words from symptoms_list that are less than 4 characters
        symptoms_list = [word for word in symptoms_list if len(word) > 3]
        
        return symptoms_list
        
    def extract_words(text):
        # Split by spaces and punctuation, and remove any empty strings
        words = re.findall(r'\b\w+\b', text.lower())
        return words