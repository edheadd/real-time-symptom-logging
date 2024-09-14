import pandas as pd
import re


# Load the CSV
df = pd.read_csv('symptoms.csv', header=None, names=['primary_name', 'consumer_name', 'synonyms'])

# Convert 'Keywords' from string to list
df['synonyms'] = df['synonyms'].apply(lambda x: eval(x) if isinstance(x, str) and x.startswith('[') else [])

# To be replaced by tts module
patient_text = """
    i have had a persistent cough, fever, and fatigue over the last few days. i also have scarlet fever.
"""

def clean_word(word):
    return re.sub(r'[^\w\s]', '', word).strip()

words = [clean_word(word).lower() for word in patient_text.split()]

def find_symptoms(words, symptom_df):
    detected_conditions = []
    for _, row in symptom_df.iterrows():
        primary_name = row['primary_name'].rstrip().lower()
        consumer_name = row['consumer_name'].rstrip().lower()
        synonyms = row['synonyms']
        keywords = []
        keywords.append(primary_name)
        keywords.append(consumer_name)
        for synonym in synonyms:
            keywords.append(synonym.rstrip().lower())
        for word in words:
            if word in keywords:
                detected_conditions.append(f"{primary_name} ({consumer_name})")
    
    return detected_conditions


# Detect symptoms in the patient text
detected_symptoms = find_symptoms(words, df)

# Print the results
print("Detected conditions:", detected_symptoms)
