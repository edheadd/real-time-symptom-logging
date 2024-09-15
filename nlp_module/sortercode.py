import pandas as pd
import ast

# Load the CSV file into a DataFrame
df = pd.read_csv('symptoms.csv', header=None, names=['primary_name', 'consumer_name', 'synonyms'])

# Convert 'synonyms' column from string to list of strings
def convert_to_list(x):
    try:
        return ast.literal_eval(x) if isinstance(x, str) and x.startswith('[') and x.endswith(']') else []
    except (ValueError, SyntaxError):
        return []

df['synonyms'] = df['synonyms'].apply(convert_to_list)

# Function to convert a value to a single string
def convert_value_to_string(value):
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

# Apply conversion function to 'primary_name', 'consumer_name', and 'synonyms'
df['primary_name'] = df['primary_name'].apply(convert_value_to_string)
df['consumer_name'] = df['consumer_name'].apply(convert_value_to_string)
df['synonyms'] = df['synonyms'].apply(lambda x: ' '.join(x))

# Function to preprocess text (convert to lowercase and strip trailing spaces)
def preprocess_text(text):
    return text.lower().rstrip()

# Apply preprocessing to the DataFrame columns
df['primary_name'] = df['primary_name'].apply(preprocess_text)
df['consumer_name'] = df['consumer_name'].apply(preprocess_text)
df['synonyms'] = df['synonyms'].apply(preprocess_text)

# Define the search string (case-insensitive)
search_string = 'Adenotonsillar hypertrophy'  # Replace with your actual search string
search_string = preprocess_text(search_string)  # Preprocess the search string

# Function to check if the search string exactly matches any of the combined strings
def search_in_row(row):
    combined_strings = [preprocess_text(cell) for cell in row]
    return search_string in combined_strings

# Use a set to keep track of unique rows
result = []
unique_primary_names = set()  # Use a set to track unique primary names

# Search for the string in each row and retrieve the first two columns
for index, row in df.iterrows():
    primary_name = row['primary_name']
    consumer_name = row['consumer_name']

    # Assuming search_in_row is a function that returns True or False
    if search_in_row([row['primary_name'], row['consumer_name'], row['synonyms']]):
        # Check if the primary_name is not already in the set
        if primary_name not in unique_primary_names:
            # Add primary_name to the set
            unique_primary_names.add(primary_name)
            # Append the row to the result
            result.append({
                'primary_name': primary_name,
                'consumer_name': consumer_name
            })

# Print the results
for item in result:
    if item['primary_name'] != item['consumer_name']:
        print(f"Primary Name: {item['primary_name']}, Consumer Name: {item['consumer_name']}")
    else:
        print(f"Primary Name: {item['primary_name']}")
