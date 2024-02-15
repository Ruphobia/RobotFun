#!/usr/bin/python3.8
import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import warnings

# Configuration
os.environ['PYTORCH_CUDA_ALLOC_CONF'] = "expandable_segments:True"
warnings.filterwarnings('ignore')
device = 'cuda' if torch.cuda.is_available() else 'cpu'

# *** General Chat ***
model_name = "gpt2"  
# model_name = "gpt2-medium" 
# model_name = "gpt2-large"
# model_name = "EleutherAI/gpt-neo-125M" 
# model_name = "EleutherAI/gpt-neo-1.3B" # Too large for GTX 1650

# Load model and tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name).to(device)

def answer_question(question):
    # Format input to indicate that it's a question
    input_text = f"Q: {question}\nA:"
    inputs = tokenizer.encode(input_text, return_tensors='pt').to(device)
    with torch.no_grad():
        # Generate response with appropriate parameters
        answer_ids = model.generate(inputs, max_length=50, pad_token_id=tokenizer.eos_token_id, temperature=0.1, top_k=50)
    answer = tokenizer.decode(answer_ids[:, inputs.shape[-1]:][0], skip_special_tokens=True)
    return answer

while True:
    user_question = input("You: ")
    if user_question.lower() == 'quit':
        break
    response = answer_question(user_question)
    print(f"Roger the Robot: {response}")
