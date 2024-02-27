#!/usr/bin/python3.8
from llama_cpp import Llama

# set CMAKE_ARGS=-DLLAMA_CUBLAS=on
# set FORCE_CMAKE=1
# pip install llama-cpp-python --force-reinstall --upgrade --no-cache-dir

# CMAKE_ARGS="-DLLAMA_CUBLAS=on" FORCE_CMAKE=1 pip install llama-cpp-python --no-cache-dir --verbose


# Set gpu_layers to the number of layers to offload to GPU. Set to 0 if no GPU acceleration is available on your system.
llm = Llama(
  model_path="./wizardcoder-33b-v1.1.Q4_K_M.gguf",  # Download the model file first
  n_ctx=16384,  # The max sequence length to use - note that longer sequence lengths require much more resources
  n_threads=40,            # The number of CPU threads to use, tailor to your system and the resulting performance
  n_gpu_layers=60         # The number of layers to offload to GPU, if you have GPU acceleration available
)

# Simple inference example
output = llm(
  "Below is an instruction that describes a task. Write a response that appropriately completes the request.\n\n### Instruction:\n{prompt}\n\n### Response:", # Prompt
  max_tokens=512,  # Generate up to 512 tokens
  stop=["</s>"],   # Example stop token - not necessarily correct for this specific model! Please check before using.
  echo=True        # Whether to echo the prompt
)

# Chat Completion API

llm = Llama(model_path="./wizardcoder-33b-v1.1.Q4_K_M.gguf", chat_format="llama-2", n_gpu_layers=60)  # Set chat_format according to the model you are using
llm.create_chat_completion(
    messages = [
        {"role": "system", "content": "You are a story writing assistant."},
        {
            "role": "user",
            "content": "Write a story about llamas."
        }
    ]
)
