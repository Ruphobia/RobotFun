#!/usr/bin/python3
from diffusers import StableDiffusionPipeline
import torch

model_id = "runwayml/stable-diffusion-v1-5"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
pipe = pipe.to("cuda:2")

prompt = "white fluffy kitten playing in a grassy field"
image = pipe(prompt).images[0]  
    
image.save("./output1.jpg")
