import pandas as pd
import re
import ast

class symptom_processing():
    
    def __init__(self):
        self.df = pd.read_csv('C://Users//ebexi//OneDrive//Documents//i hate life//real-time-symptom-logging//nlp_module//symptoms.csv', 
                              header=None, 
                              names=['primary_name', 'consumer_name', 'synonyms'])
        
        # Convert all synonyms from a string to a list
        self.df['synonyms'] = self.df['synonyms'].apply(self.convert_to_list)
        
    def get_symptoms_list(self):
        
        # Open the CSV
        df = pd.read_csv('C://Users//ebexi//OneDrive//Documents//i hate life//real-time-symptom-logging//nlp_module//symptoms.csv', 
                              header=None, 
                              names=['primary_name', 'consumer_name', 'synonyms'])
        
        # Create a set to avoid duplicates
        symptoms_set = set()
        
        df['primary_name'].apply(lambda x: symptoms_set.update(self.extract_words(x)))
        df['synonyms'].apply(lambda x: symptoms_set.update(self.extract_words(str(x).strip("[]").replace("'", ""))))

        # Convert the set to a list for output
        symptoms_list = list(symptoms_set)

        # Remove words from symptoms_list that are less than 4 characters
        symptoms_list = [word for word in symptoms_list if len(word) > 3]
    
        return symptoms_list
    
    def formalize_symptoms(self, text):

        # Define the search string (case-insensitive)
        search_string = self.preprocess_text(text)  # Preprocess the search string

        # Use a string to keep results unique
        result = []
        unique_primary_names = []

        # Search for the string in each row and retrieve the first two columns
        for index, row in self.df.iterrows():
            primary_name = row['primary_name']
            consumer_name = row['consumer_name']
            synonyms = row['synonyms']
            for synonym in synonyms:
                synonym = self.preprocess_text(synonym)
            row_content = [self.preprocess_text(primary_name), self.preprocess_text(consumer_name)] + synonyms

            # If the search string is in the row
            if self.search_in_row(row_content, search_string):
                # Check if the primary_name is not already in the list
                if primary_name not in unique_primary_names:
                    # Add primary_name to the list
                    unique_primary_names.append(primary_name)
                    # Append the row to the result
                    result.append({
                        'primary_name': primary_name.rstrip(),
                        'consumer_name': consumer_name.rstrip()
                    })

        # Create a result string based on uniqueness of the two result columns.
        result_string = ''
        for item in result:
            if item['primary_name'] != item['consumer_name']:
                result_string = result_string + (f"Symptom: {item['primary_name']}, also known as {item['consumer_name']}\n")
            else:
                result_string = result_string + (f"Symptom: {item['primary_name']}\n")
        return result_string
            

    # Function to convert the string form of a list to a list
    def convert_to_list(self, x):
        try:
            return ast.literal_eval(x) if isinstance(x, str) and x.startswith('[') and x.endswith(']') else []
        except (ValueError, SyntaxError):
            return []
    
    # Function to convert a value to a single string
    def convert_value_to_string(self, value):
        if isinstance(value, str):
            if value.startswith('[') and value.endswith(']'):
                list_value = ast.literal_eval(value)
                return ' '.join(list_value) if list_value else ""
            else:
                return value
        elif isinstance(value, list):
            return ' '.join(value)
        else:
            return str(value)
        
    # Function to apply lowercase and remove excess whitespace
    def preprocess_text(self, text):
        return text.lower().rstrip()
    
    # Function to check if the search string exactly matches any of the combined strings
    def search_in_row(self, row, search_string):
        combined_strings = [cell.lower().rstrip() for cell in row]
        return search_string in combined_strings
    
    # Function to extract words from strings
    def extract_words(self, text):
        # Split by spaces and punctuation, and remove any empty strings
        words = re.findall(r'\b\w+\b', text.lower())
        return words
