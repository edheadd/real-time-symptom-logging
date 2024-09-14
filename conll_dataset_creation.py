import pandas as pd

def conll_to_csv(conll_file, output_csv):
    data = []
    with open(conll_file, 'r') as infile:
        term_label_pair = []
        for line in infile:
            line = line.strip()
            if line:  # If the line is not empty
                term, label = line.split('\t')
                term_label_pair.append((term, label))
            else:  # If the line is empty, it means a new entry is starting
                if term_label_pair:  # Avoid writing if no data was collected
                    data.extend(term_label_pair)
                    term_label_pair = []
        
        # If there's any remaining data after the last entry
        if term_label_pair:
            data.extend(term_label_pair)
    
    # Create a DataFrame and write it to CSV
    df = pd.DataFrame(data, columns=['term', 'label'])
    df.to_csv(output_csv, index=False)

# Example usage:
conll_to_csv('conll_data.conll', 'output_data.csv')
