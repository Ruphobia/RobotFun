#!/usr/bin/python3.8
import warnings
# Suppress all warnings
warnings.filterwarnings('ignore')

import torch
from transformers import pipeline

# Check if a GPU is available and set PyTorch to use it
device = 0 if torch.cuda.is_available() else -1  # device = 0 for GPU, -1 for CPU

# Load the classification pipeline with our chosen model, specify the device
classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english", device=device) # Positive and Negative, no neutral


def classify_sentiment(text):
    # Use the classifier to predict the intent
    result = classifier(text)
    # Assuming the model's output format is a list of dicts with 'label' and 'score'
    sentiment = result[0]['label']
    
    return sentiment

# Sample program running in a loop
print("Type 'quit' to exit.")
while True:
    user_input = input("You: ")
    if user_input.lower() == 'quit':
        break
    sentiment = classify_sentiment(user_input)
    print(f"Sentiment: {sentiment}")
