from transformers import pipeline
import pandas as pd


# Load the CSV
df = pd.read_csv('symptoms.csv', header=None, names=['Condition', 'Description', 'Keywords'])

# Convert 'Keywords' from string to list
df['Keywords'] = df['Keywords'].apply(lambda x: eval(x) if isinstance(x, str) and x.startswith('[') else [])

# To be replaced by tts module
patient_text = """
    I have had a persistent cough, fever, and fatigue over the last few days.
"""

nlp = pipeline("ner", model="dmis-lab/biobert-base-cased-v1.1")

entities = nlp(patient_text)
for entity in entities:
    entity = entity.lower();


def find_symptoms(text_tokens, symptom_df):
    detected_conditions = []
    for _, row in symptom_df.iterrows():
        condition = row['Condition']
        description = row['Description']
        keywords = row['Keywords']
        
        # Check if any keyword from the list is in the text
        if any(keyword.lower() in text_tokens for keyword in keywords):
            detected_conditions.append(f"{condition} ({description})")
    
    return detected_conditions


# Detect symptoms in the patient text
detected_symptoms = find_symptoms(entities, df)

# Print the results
print("Detected conditions:", detected_symptoms)