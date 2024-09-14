from transformers import pipeline
import pandas as pd
import re

# Load the CSV
df = pd.read_csv('symptoms.csv', header=None, names=['primary_name', 'consumer_name', 'synonyms'])

# Convert 'synonyms' from string to list
df['synonyms'] = df['synonyms'].apply(lambda x: eval(x) if isinstance(x, str) and x.startswith('[') else [])

# To be replaced by tts module
patient_text = """
    Despite her concerns about dizziness, a persistent cough, acne, and a recent injury, she was relieved when tests ruled out cancer, including breast cancer, spine cancer, terminal cancer, and even an undetected tumor, though the doctors cautioned her about the dangers of AIDs, cocaine addiction, and crack abuse, which could further complicate her health if left unchecked, especially with her bleeding corn and occasional fluid leaks, leaving her temporarily disabled and in need of careful medical attention.
"""

# Load your trained NER model
model_path = 'saved_biobert_model'  # Uncomment and replace with your model paths
nlp = pipeline("ner", model=model_path, tokenizer=model_path)  # Using CPU
#nlp = pipeline("ner", model=model_path, tokenizer=model_path, device=0)  # Using GPU (device=0) if available

# Extract entities
entities = nlp(patient_text)

# Function to split text into individual words
def extract_words(text):
    # Split by spaces and punctuation, and remove any empty strings
    words = re.findall(r'\b\w+\b', text.lower())
    return words

# Create a set to avoid duplicates
symptoms_set = set()

df['primary_name'].apply(lambda x: symptoms_set.update(extract_words(x)))

# Process 'synonyms'
df['synonyms'].apply(lambda x: symptoms_set.update(extract_words(str(x).strip("[]").replace("'", ""))))

# Convert the set to a list for output
symptoms_list = list(symptoms_set)

# Remove words from symptoms_list that are less than 4 characters
symptoms_list = [word for word in symptoms_list if len(word) > 3]

# Filter out words and sort entities by their scores in descending order
filtered_entities = [entity for entity in entities if len(entity['word']) > 3]

matching_entities = []

# Print matching words
for entity in filtered_entities:
    if entity["word"] in symptoms_list:
        entity["score"] = entity["score"]*1.5
        matching_entities.append(entity)

sorted_entities = sorted(filtered_entities, key=lambda x: x['score'], reverse=True)

# Print words and scores in order of greatest to least score
#for entity in sorted_entities:
#    print(f"Word: {entity['word']}, Score: {entity['score']:.4f}")

to_check = set()

lowest_score = 1
for entity in matching_entities:
    if entity["score"] < lowest_score:
        lowest_score = entity["score"]
print(lowest_score)

for i in range(len(entities)):
    if entities[i]['score'] > lowest_score and entities[i] in filtered_entities:
        to_check.add(entities[i]['word'])
        if entities[i+1]['score'] > lowest_score and entities[i+1] in filtered_entities:
            to_check.add(entities[i]['word']+" "+entities[i+1]['word'])
            #print(entities[i]['word']+" "+entities[i+1]['word'])
            
            to_check.add(entities[i+1]['word']+" "+entities[i]['word'])
            #print(entities[i+1]['word']+" "+entities[i]['word'])
            
            
print(to_check)