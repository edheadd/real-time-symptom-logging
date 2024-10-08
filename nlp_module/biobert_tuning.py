import pandas as pd
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments, DataCollatorWithPadding
from sklearn.preprocessing import LabelEncoder
import torch

# Load the CSV file
def load_csv(file_path):
    df = pd.read_csv(file_path)
    return df

# Create a label mapping
def create_label_mapping(df):
    labels = df['label'].unique()
    label_encoder = LabelEncoder()
    label_encoder.fit(labels)
    return label_encoder

# Convert labels to integers
def convert_labels_to_integers(df, label_encoder):
    # Convert labels to integers using the label encoder
    df['label'] = label_encoder.transform(df['label'])
    
    # Convert to integers (CrossEntropyLoss expects integer labels)
    df['label'] = df['label'].astype(int)
    
    return df

# Convert to Hugging Face Dataset
def convert_to_dataset(df):
    dataset = Dataset.from_pandas(df)
    return dataset

# Preprocess the Data for BioBERT
def preprocess_data(dataset, tokenizer):
    def preprocess_function(examples):
        return tokenizer(examples['text'], padding="max_length", truncation=True, max_length=128)
    
    tokenized_dataset = dataset.map(preprocess_function, batched=True)
    return tokenized_dataset

# Prepare the data for PyTorch
def prepare_data_for_training(tokenized_dataset):
    tokenized_dataset = tokenized_dataset.train_test_split(test_size=0.2)
    
    # Ensure labels are of type long (CrossEntropyLoss requires long integer labels)
    def convert_labels_to_long(example):
        example['label'] = torch.tensor(example['label'], dtype=torch.long)
        return example

    tokenized_dataset = tokenized_dataset.map(convert_labels_to_long)
    tokenized_dataset.set_format("torch", columns=["input_ids", "attention_mask", "label"])
    return tokenized_dataset

# Load the BioBERT model
def load_biobert_model(num_labels, device):
    model = AutoModelForSequenceClassification.from_pretrained('dmis-lab/biobert-base-cased-v1.1', num_labels=num_labels)
    # Move the model to GPU if available
    model.to(device)
    return model

# Create Trainer
def create_trainer(model, tokenized_dataset, tokenizer):
    training_args = TrainingArguments(
        output_dir='./results',
        evaluation_strategy="epoch",  # Updated to use evaluation_strategy
        learning_rate=2e-5,
        per_device_train_batch_size=64,
        per_device_eval_batch_size=64,
        num_train_epochs=20,
        weight_decay=0.01,
        # Enable GPU usage if available
        fp16=torch.cuda.is_available(),  # Use mixed-precision training if GPU is available
    )
    
    # Use DataCollatorWithPadding
    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)
    
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset['train'],
        eval_dataset=tokenized_dataset['test'],
        data_collator=data_collator,
    )
    
    return trainer

def save_model_and_tokenizer(model, tokenizer, output_dir):
    # Save the model
    model.save_pretrained(output_dir)
    # Save the tokenizer
    tokenizer.save_pretrained(output_dir)

# Main function
def main(file_path):
    # Check if a GPU is available
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    df = load_csv(file_path)
    
    # Create label mapping and convert labels to integers (instead of floats)
    label_encoder = create_label_mapping(df)
    df = convert_labels_to_integers(df, label_encoder)
    
    dataset = convert_to_dataset(df)
    
    tokenizer = AutoTokenizer.from_pretrained('dmis-lab/biobert-base-cased-v1.1')
    tokenized_dataset = preprocess_data(dataset, tokenizer)
    tokenized_dataset = prepare_data_for_training(tokenized_dataset)
    
    num_labels = len(label_encoder.classes_)
    model = load_biobert_model(num_labels, device)
    
    trainer = create_trainer(model, tokenized_dataset, tokenizer)
    trainer.train()
    
    results = trainer.evaluate()
    print(results)
    
    # Save the model and tokenizer
    output_dir = './saved_biobert_model'
    save_model_and_tokenizer(model, tokenizer, output_dir)

if __name__ == "__main__":
    file_path = 'conll_dataset2.csv'  # Replace with your CSV file path
    main(file_path)
