#!/usr/bin/python3.8
import json
import torch
from sklearn.model_selection import train_test_split
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification, Trainer, TrainingArguments
import os

def get_current_directory_path():
    """
    Returns the absolute path of the current working directory.

    Returns:
        str: The absolute path of the current working directory.
    """
    current_path = os.getcwd()
    return current_path

def load_data(file_path='intents.json'):
    with open(file_path, 'r') as f:
        intents = json.load(f)
    texts = []
    labels = []
    tag_to_idx = {}
    for intent in intents['intents']:
        tag = intent['tag']
        if tag not in tag_to_idx:
            tag_to_idx[tag] = len(tag_to_idx)
        for pattern in intent['patterns']:
            texts.append(pattern)
            labels.append(tag_to_idx[tag])
    return texts, labels, tag_to_idx

class IntentDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

def main():
    # Setup device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    texts, labels, tag_to_idx = load_data(f"{get_current_directory_path()}/intents.json")
    tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-uncased')

    train_texts, val_texts, train_labels, val_labels = train_test_split(texts, labels, test_size=0.1)
    train_encodings = tokenizer(train_texts, truncation=True, padding=True, max_length=64)
    val_encodings = tokenizer(val_texts, truncation=True, padding=True, max_length=64)

    train_dataset = IntentDataset(train_encodings, train_labels)
    val_dataset = IntentDataset(val_encodings, val_labels)

    training_args = TrainingArguments(
        output_dir="{get_current_directory_path()}/results",
        num_train_epochs=3,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=64,
        warmup_steps=500,
        weight_decay=0.01,
        logging_dir="{get_current_directory_path()}/logs",
        logging_steps=10,
    )

    model = DistilBertForSequenceClassification.from_pretrained('distilbert-base-uncased', num_labels=len(tag_to_idx)).to(device)

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset
    )

    trainer.train()

    # Save the model and tokenizer
    model.save_pretrained(f"{get_current_directory_path()}/intent_classification_model")
    tokenizer.save_pretrained(f"{get_current_directory_path()}/intent_classification_model")
    print("Training complete. Model saved to ./intent_classification_model")

if __name__ == "__main__":
    main()
