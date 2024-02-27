#!/usr/bin/python3.8
import os

# Set environment variables to use the first five GPUs and optimize memory allocation
os.environ['CUDA_VISIBLE_DEVICES'] = '0,1,2,3,4'

from transformers import AutoTokenizer
import transformers
import torch
from transformers import pipeline

model = "WizardLM/WizardCoder-33B-V1.1" 
tokenizer = AutoTokenizer.from_pretrained(model)

llama_pipeline = pipeline(
    "text-generation",  # LLM task
    model=model,
    torch_dtype=torch.int8,
    device_map="auto",
)


def get_llama_response(prompt: str) -> None:
    """
    Generate a response from the Llama model.

    Parameters:
        prompt (str): The user's input/question for the model.

    Returns:
        None: Prints the model's response.
    """
    sequences = llama_pipeline(
        prompt,
        do_sample=True,
        top_k=10,
        num_return_sequences=1,
        eos_token_id=tokenizer.eos_token_id,
        max_length=256,
    )
    print("Chatbot:", sequences[0]['generated_text'])



while True:
    user_input = input("You: ")
    if user_input.lower() in ["bye", "quit", "exit"]:
        print("Chatbot: Goodbye!")
        break
    get_llama_response(user_input)