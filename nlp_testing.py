from transformers import pipeline

# Load pre-trained BERT model for medical text analysis
nlp = pipeline("ner", model="dmis-lab/biobert-base-cased-v1.1")

# Patient text
patient_text = """
    I have had a persistent cough, fever, and fatigue over the last few days.
"""

# Run the model to detect named entities (symptoms)
entities = nlp(patient_text)

clean_list = []

for entity in entities:
    clean_entity = {
        "word": entity["word"],
        "score": entity["score"]
    }
    clean_list.append(clean_entity)
    
print(clean_list)