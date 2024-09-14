from transformers import BertTokenizerFast, BertForTokenClassification
from datasets import load_dataset

tokenizer = BertTokenizerFast.from_pretrained("dmis-lab/biobert-base-cased-v1.1")
model = BertForTokenClassification.from_pretrained("dmis-lab/biobert-base-cased-v1.1")

def tokenize_and_align_labels(examples):
    tokenized_inputs = tokenizer(examples["text"], padding="max_length", truncation=True)

    labels = []
    for i, label in enumerate(examples["entities"]):
        label_ids = [label_map.get(label, -100) for label in label]
        labels.append(label_ids + [-100] * (len(tokenized_inputs["input_ids"][i]) - len(label_ids)))
    
    tokenized_inputs["labels"] = labels
    return tokenized_inputs

# Example usage
dataset = load_dataset("json", data_files={"train": "path_to_your_data.json"})
tokenized_datasets = dataset.map(tokenize_and_align_labels, batched=True)
