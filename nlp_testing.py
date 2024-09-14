from transformers import pipeline

# Load pre-trained BERT model for medical text analysis
nlp = pipeline("ner", model="dmis-lab/biobert-base-cased-v1.1")

# Patient text
patient_text = """
    I have had a persistent cough, fever, and fatigue over the last few days.
"""

# Run the model to detect named entities (symptoms)
entities = nlp(patient_text)

# Initialize an empty list to store clean entities
clean_list = []

for entity in entities:
    word = entity["word"]
    if len(word) > 1:  # Filter out single-character words
        clean_entity = {
            "word": word,
            "score": entity["score"]
        }
        clean_list.append(clean_entity)
    
# Print the cleaned entities
for item in clean_list:
    print(item["word"], ": ", item["score"])
