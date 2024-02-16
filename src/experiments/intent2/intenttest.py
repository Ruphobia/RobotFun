#!/usr/bin/python3.8
import torch
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

def main():
    model_dir = f"{get_current_directory_path()}/intent_classification_model"
    classify_intent = load_model_and_tokenizer(model_dir)
    
    print("Type 'quit' to exit.")
    while True:
        text = input("Enter your prompt: ")
        if text.lower() == "quit":
            break
        prediction = classify_intent(text)
        intent_tag = prediction[0]['label']
        print(f"Predicted Intent: {intent_tag}")

if __name__ == "__main__":
    main()
