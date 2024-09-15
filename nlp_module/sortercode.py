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

# Define the search string (exact match, case-sensitive, without spaces)
search_string = 'AIDS'  # Replace with your actual search string

# Function to check if the search string is in any of the combined strings
def search_in_row(row):
    combined_string = ' '.join(row)
    return search_string in combined_string

# Search for the string in each row and retrieve the first two columns
result = []
for index, row in df.iterrows():
    if search_in_row([row['primary_name'], row['consumer_name'], row['synonyms']]):
        result.append({
            'primary_name': row['primary_name'],
            'consumer_name': row['consumer_name'],
            'synonyms': row['synonyms']
        })

# Print the results
for item in result:
    if item['primary_name'] != item['consumer_name']:
        print(f"Primary Name: {item['primary_name']}, Consumer Name: {item['consumer_name']}")
    else:
        print(f"Primary Name: {item['primary_name']}")
