#!/usr/bin/python3.8
import torch
import json
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification, pipeline
import os

def get_current_directory_path():
    """
    Returns the absolute path of the current working directory.
    
    Returns:
        str: The absolute path of the current working directory.
    """
    current_path = os.getcwd()
    return current_path

def load_model_and_tokenizer(model_dir):
    """
    Load the fine-tuned model and tokenizer from the specified directory.
    
    Parameters:
        model_dir (str): Directory where the model and tokenizer are saved.
    
    Returns:
        pipeline: Hugging Face inference pipeline for intent classification.
    """
    tokenizer = DistilBertTokenizerFast.from_pretrained(model_dir)
    model = DistilBertForSequenceClassification.from_pretrained(model_dir)
    return pipeline("text-classification", model=model, tokenizer=tokenizer)

def load_tag_mappings(model_dir):
    """
    Load the tag-to-index mappings from the specified directory.
    
    Parameters:
        model_dir (str): Directory where the tag_to_idx.json file is saved.
    
    Returns:
        dict: A dictionary to convert index to tag labels.
    """
    mapping_file = os.path.join(model_dir, "tag_to_idx.json")
    with open(mapping_file, 'r') as f:
        tag_to_idx = json.load(f)
    idx_to_tag = {v: k for k, v in tag_to_idx.items()}
    return idx_to_tag

def main():
    model_dir = f"{get_current_directory_path()}/intent_classification_model"
    classify_intent = load_model_and_tokenizer(model_dir)
    idx_to_tag = load_tag_mappings(model_dir)
    
    print("Type 'quit' to exit.")
    while True:
        text = input("Enter your prompt: ")
        if text.lower() == "quit":
            break
        prediction = classify_intent(text)
        # Convert the numerical label to the corresponding intent tag
        intent_tag = idx_to_tag[int(prediction[0]['label'].split('_')[-1])]
        print(f"Predicted Intent: {intent_tag}")

if __name__ == "__main__":
    main()
