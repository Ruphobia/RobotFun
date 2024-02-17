#!/usr/bin/python3.8
import os
import shutil

# https://ollama.com/library
# https://github.com/ollama/ollama/blob/main/docs/faq.md

def kill_ollama_service() -> None:
    """
    Kill the service running at /usr/local/bin/ollama.
    """
    import subprocess

    subprocess.run(["sudo", "killall", "ollama"])

def create_ram_drive(size_gb: int, mount_location: str) -> None:
    """
    Create a RAM drive with the specified size in gigabytes and mount it at the specified location,
    if it's not already mounted. If the RAM drive is created, copy recursively from ~/work/ramdrive/*
    to ~/ramdrive/.
    
    Parameters:
        size_gb (int): The size of the RAM drive in gigabytes.
        mount_location (str): The location where the RAM drive will be mounted.
    """
    import subprocess

    # Check if the mount location is already in use
    with open("/proc/mounts", "r") as f:
        if any(mount_location in line for line in f):
            print(f"RAM drive already mounted at {mount_location}")
            return -1

    # Create and mount the RAM drive
    subprocess.run(["sudo", "mkdir", "-p", mount_location])
    subprocess.run(["sudo", "mount", "-t", "tmpfs", "-o", f"size={size_gb}G", "tmpfs", mount_location])

    # Copy files from ~/work/ramdrive/* to ~/ramdrive/
    source_dir = os.path.expanduser("~/work/ramdrive")
    dest_dir = os.path.expanduser("~/ramdrive")
    if os.path.exists(source_dir):
        shutil.copytree(source_dir, dest_dir)
        print(f"Copied files from {source_dir} to {dest_dir}")
    else:
        print(f"No files found at {source_dir}")
        
    return 0

def pull_model(modelname: str) -> None:
    """
    Pull the specified model using ollama.
    
    Parameters:
        modelname (str): The name of the model to pull.
    """
    from tqdm import tqdm
    from ollama import pull

    current_digest, bars = '', {}
    for progress in pull(modelname, stream=True):
        digest = progress.get('digest', '')
        if digest != current_digest and current_digest in bars:
            bars[current_digest].close()

        if not digest:
            print(progress.get('status'))
            continue

        if digest not in bars and (total := progress.get('total')):
            bars[digest] = tqdm(total=total, desc=f'pulling {digest[7:19]}', unit='B', unit_scale=True)

        if completed := progress.get('completed'):
            bars[digest].update(completed - bars[digest].n)

        current_digest = digest

def chatbot():
    # create a ram drive to store the models
    didCreateDrive = create_ram_drive(200, "/home/jwoods/ramdisk")

    # kill / restart ollama
    # kill_ollama_service()

    from ollama import generate

    # modelname = "dolphin-mistral:latest"
    # modelname = "llama2-uncensored"
    modelname = "dolphin-mixtral"
    # modelname = "codellama:70b"
    # modelname = "dolphin-2.0-mistral-7b.Q4_K_M.gguf"

    # Pull the model
    if (didCreateDrive == 0):
     pull_model(modelname)

    context = []
    while True:
        prompt = input("You: ")
        context.extend([ord(char) for char in prompt])

        for part in generate(modelname, prompt, context=context, stream=True):
            print(part['response'], end='', flush=True)
            
        print("")

if __name__ == "__main__":
    chatbot()
