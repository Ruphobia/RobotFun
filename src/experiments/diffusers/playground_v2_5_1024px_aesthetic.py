#!/usr/bin/python3
from diffusers import DiffusionPipeline
import torch

pipe = DiffusionPipeline.from_pretrained(
    "playgroundai/playground-v2-1024px-aesthetic",
    torch_dtype=torch.float16,
    use_safetensors=True,
    add_watermarker=False,
    # variant="fp16"
)
pipe.to("cuda:1")

prompt = "fluffy white kitten playing with a mouse"
image = pipe(
    prompt=prompt,
    guidance_scale=15.0,
    num_inference_steps=200,
    width=1024,
    height=1024,
    scheduler="K_LMS"
).images[0] 
image.save("./output.jpg")