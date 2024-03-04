#!/usr/bin/python3

from diffusers import StableDiffusionPipeline
import torch

# model_id = "dreamlike-art/dreamlike-photoreal-2.0"
# model_id = "Yntec/RealLife"
# model_id = "digiplay/majicMIX_realistic_v6"
model_id = "Lykon/absolute-reality-1.6525"


pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
pipe = pipe.to("cuda")

prompt = ""
images = pipe(prompt).images
image = images[0]

print("Number of images:", len(images))

model_id_txt = model_id.replace("/","_")
prompt_txt = prompt.replace(" ","_")
image.save(f"./{model_id_txt}_{prompt_txt}_result.jpg")
