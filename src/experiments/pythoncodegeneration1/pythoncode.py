#!/usr/bin/python3.8


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
    Create a RAM drive with the specified size in gigabytes and mount it at the specified location.
    
    Parameters:
        size_gb (int): The size of the RAM drive in gigabytes.
        mount_location (str): The location where the RAM drive will be mounted.
    """
    import subprocess

    subprocess.run(["sudo", "mkdir", "-p", mount_location])
    subprocess.run(["sudo", "mount", "-t", "tmpfs", "-o", f"size={size_gb}G", "tmpfs", mount_location])

# create a ram drive to store the models
create_ram_drive(200, "/home/jwoods/ramdisk")

# kill / restart ollama
kill_ollama_service()

from ollama import generate
from tqdm import tqdm
from ollama import pull
# modelname = "dolphin-mistral:latest"
# modelname = "llama2-uncensored"
# modelname = "dolphin-mixtral"
modelname = "codellama:70b"

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

for part in generate(modelname, 'write a chatbot in python usine import ollama, have a global variable that i can set the model name, if possible have ollama load the entire model in rame i have massive ammounts of ram, give it some history so we can have context', stream=True):
  print(part['response'], end='', flush=True)