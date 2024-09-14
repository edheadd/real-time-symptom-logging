import pandas as pd

# Load the CSV
df = pd.read_csv('symptoms.csv', header=None, names=['primary_name', 'consumer_name', 'synonyms'])

# Convert 'synonyms' from string to list
df['synonyms'] = df['synonyms'].apply(lambda x: eval(x) if isinstance(x, str) and x.startswith('[') else [])

def transform_to_conll(output_file):
    with open(output_file, 'w') as outfile:
        for _, row in df.iterrows():
            primary_name = row['primary_name'].strip().lower()
            consumer_name = row['consumer_name'].strip().lower()
            synonyms = row['synonyms']
            
            # Combine all terms
            keywords = [primary_name, consumer_name] + [synonym.strip().lower() for synonym in synonyms]
            
            # Write to file
            for word in keywords:
                if len(word) > 1:
                    outfile.write(f'{word}\tB-TERM\n')
                else:
                    outfile.write(f'{word}\tO\n')
            
            # Add a newline to separate entries
            outfile.write('\n')

# Example usage:
transform_to_conll('conll_data.conll')
