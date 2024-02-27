#!/usr/bin/python3.8
import os

# Set environment variables to use the first five GPUs and optimize memory allocation
os.environ['CUDA_VISIBLE_DEVICES'] = '0,1,2,3,4'
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"

import transformers
import torch

# Load tokenizer and model
tokenizer = transformers.AutoTokenizer.from_pretrained("WizardLM/WizardCoder-33B-V1.1")
model = transformers.AutoModelForCausalLM.from_pretrained("WizardLM/WizardCoder-33B-V1.1", device_map = 'auto')  # Ensure the model is compatible with generation tasks
model = model.half()

# # Utilize DataParallel for multi-GPU support
# if torch.cuda.is_available():
#     model = torch.nn.DataParallel(model).to('cuda')
#     model = model.half()  # Convert model to half precision
#     print("Using CUDA")
# else:
#     model = model.to('cpu')  # Fallback to CPU if needed
#     print("Using CPU")

def generate_code(query):
    input_ids = tokenizer(query, return_tensors="pt").input_ids
    if torch.cuda.is_available():
        input_ids = input_ids.to('cuda')  # Ensure input_ids are on the same device as the model

    # Generate output using the appropriate device
    output_ids = model.module.generate(input_ids, max_length=256) if hasattr(model, 'module') else model.generate(input_ids, max_length=256)

    return tokenizer.decode(output_ids[0], skip_special_tokens=True)

# Chatbot Loop
while True:
    user_query = input("You: ")
    if user_query.lower() == 'exit':
        break

    response = generate_code(user_query)
    print("Coding Bot: " + response)
