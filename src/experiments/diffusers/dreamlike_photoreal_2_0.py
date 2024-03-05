#!/usr/bin/python3

import concurrent.futures
from diffusers import AutoPipelineForText2Image
import torch

# Schedulers

    # DDIM (Denoising Diffusion Implicit Models) Scheduler: This scheduler allows for faster image generation with
    # fewer steps by using a non-Markovian process. It's known for producing high-quality images with fewer inference
    # steps compared to other methods.

    # PNDM (Probability Noise Diffusion Model) Scheduler: A probabilistic approach that improves upon the DDIM scheduler 
    # by introducing a way to better estimate the denoising process, aiming to maintain image quality with potentially fewer steps.

    # K-LMS (Karras et al., Latent Space) Scheduler: Developed by Karras et al., this scheduler operates in the latent space and 
    # is designed to improve the efficiency of the diffusion process, often leading to high-quality results with reduced computational demands.

    # DDPM (Denoising Diffusion Probabilistic Models) Scheduler: The original scheduler based on a Markov chain process where the 
    # image is gradually denoised over a predefined number of steps. It's known for its stability and quality of generated images 
    # but typically requires more steps and thus more computational time.

    # LMS (Linear Multistep Scheduler): This scheduler uses a linear multistep approach for the denoising process, aiming to strike 
    # a balance between image quality and generation speed. It attempts to reduce the total number of required steps while maintaining 
    # high-quality outputs.

    # Heun (Heun's Method) Scheduler: An Euler-like scheduler that offers an alternative approach to managing the denoising process, 
    # with an emphasis on stability and accuracy at the cost of potentially more computation.

    # Euler (Euler Method) Scheduler: A simple and straightforward approach for the diffusion process, providing a baseline in terms 
    # of performance and quality. It's generally less efficient compared to more sophisticated schedulers.

# List of model IDs to test
model_ids = [
    "dreamlike-art/dreamlike-photoreal-2.0", # Ok, UC, nice, art like, doesn't follow directions well
    "Yntec/RealLife", # Ok, really good, possibly the best so far, not following directions
    "digiplay/majicMIX_realistic_v6", # Ok, UC, realistic, but video game like, doesn't follow directions well
    "SG161222/Realistic_Vision_V5.1_noVAE", # Ok, UC, mostly real, doesn't follow directions
    "stabilityai/stable-diffusion-xl-base-1.0", # Ok, neat, like post cards or something, doesn't follow directions well
    "stabilityai/sdxl-turbo", # Ok, UC, strange output, doesn't follow directions well
    "segmind/SSD-1B", # ok, UC, uh, scarry!!, doesn't follow directions well
    "dataautogpt3/OpenDalleV1.1", # Ok, good, not following directions
    "etri-vilab/koala-700m-llava-cap",
    "22h/vintedois-diffusion-v0-1", # Ok, C
    "darkstorm2150/Protogen_x5.8_Official_Release", # Ok, C
    "wavymulder/Analog-Diffusion", # Ok, C
    "runwayml/stable-diffusion-v1-5", # Ok, C
]

prompt = "fluffy white kitten playing in a field"
# Function to perform model inference
def run_inference(model_id, gpu_index):
    """
    Run model inference on a specific GPU.

    Parameters:
    - model_id: ID of the model to load and run.
    - gpu_index: Index of the GPU to use.
    """
    try:
        device = f"cuda:{gpu_index}"
        # device = f"cuda:1"
        pipe = AutoPipelineForText2Image.from_pretrained(model_id).to(device)


        images = pipe(
            prompt=prompt,
            safety_checker="no",
            enhance_prompt="yes",
            negative_prompt="",
            samples=2,
            width=640,
            height=480,
            num_inference_steps=20,
            guidance_scale=3,
            # scheduler="PNDM",  # Assuming you want to use a different scheduler
            seed=42,  # For reproducibility
            eta=0.5,  # Adjust randomness
        ).images
        print("Samples:", len(images))
        image = images[0]
        model_id_txt = model_id.replace("/", "_")
        prompt_txt = prompt.replace(" ", "_")
        image.save(f"./output/{model_id_txt}.jpg")
        print(f"Image saved: ./output/{model_id_txt}.jpg")
    except Exception as e:
        print(f"Error processing {model_id} on GPU {gpu_index}: {e}")

# Ensure the output directory exists
import os
if not os.path.exists('./output'):
    os.makedirs('./output')

# Create a ThreadPoolExecutor with 5 threads to match GPU count
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(run_inference, model_id, gpu_index % 5) for gpu_index, model_id in enumerate(model_ids)]

    # Optional: Wait for all futures to complete and handle exceptions
    for future in concurrent.futures.as_completed(futures):
        try:
            result = future.result()  # This will re-raise any exceptions caught during execution
        except Exception as e:
            print(f"Future execution resulted in an exception: {e}")
