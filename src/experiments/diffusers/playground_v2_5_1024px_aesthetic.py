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
pipe.to("cuda:2")

prompt = "white fluffy kitten playing in a field"
image  = pipe(prompt=prompt, guidance_scale=3).images[0]
image.save("./output.jpg")