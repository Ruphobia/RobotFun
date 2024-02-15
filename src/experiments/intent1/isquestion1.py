#!/usr/bin/python3.8
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Check if a GPU is available and set PyTorch to use it
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("shahrukhx01/question-vs-statement-classifier")
model = AutoModelForSequenceClassification.from_pretrained("shahrukhx01/question-vs-statement-classifier").to(device)

def classify_question(text):
    # Tokenize the input text
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True).to(device)
    # Use the model to predict whether the text is a question
    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits
    probabilities = torch.softmax(logits, dim=1)
    # Get the label with the highest probability
    predicted_label = torch.argmax(probabilities, dim=1).item()
    labels = ['statement', 'question']
    label = labels[predicted_label]
    confidence = probabilities[0, predicted_label].item()
    return label, confidence

# Sample program running in a loop
print("Type 'quit' to exit.")
while True:
    user_input = input("You: ")
    if user_input.lower() == 'quit':
        break
    label, confidence = classify_question(user_input)
    print(f"Text: {user_input}")
    print(f"Is Question: {label}, Confidence: {confidence:.2f}")

