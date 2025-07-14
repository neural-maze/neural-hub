import runpod
import os
import sys
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(".env")

api_key = os.environ.get('RUNPOD_API_KEY')

if not api_key:
    print("Error: RUNPOD_API_KEY not found in .env.")
    sys.exit(1)


if not api_key.startswith('rpa_') or len(api_key) < 40:
    print("Invalid api key.")
    sys.exit(1)

runpod.api_key = api_key.strip()

ssh_public_key_path = Path.home() / ".ssh" / "id_ed25519.pub"

if not ssh_public_key_path.exists():
    print("Not public SSH key found.")
    sys.exit(1)

with open(ssh_public_key_path, 'r') as f:
    public_key = f.read().strip()

# Pod configuration

pod_config = {
    "name": "rtx6000-pytorch-pod",
    "image_name": "runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel-ubuntu22.04",
    "gpu_type_id": "NVIDIA RTX 6000 Ada Generation",
    "cloud_type": "ALL",
    "support_public_ip": True,
    "start_ssh": True,
    "container_disk_in_gb": 100,
    "volume_in_gb": 100,
    "min_vcpu_count": 1,
    "min_memory_in_gb": 1,
    "ports": "22/tcp",
    "volume_mount_path": "/workspace",
    "env": {"PUBLIC_KEY": public_key}
}

try:

    print("Creating pod...")

    response = runpod.create_pod(**pod_config)
    
    pod = None

    if isinstance(response, dict):
        pod = response
    elif isinstance(response, list) and len(response) > 0:
        pod = response[0]
    
    if pod and 'id' in pod:
        print(f"Created pod: {pod['id']}")
    else:
        print("Pod couldn't be created.")
        print(f"Response: {response}")
        sys.exit(1)
        
except Exception as e:
    print(f"Error creating the pod: {str(e)}")
    sys.exit(1)