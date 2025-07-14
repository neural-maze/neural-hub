import runpod
import os
import sys
from dotenv import load_dotenv
from pathlib import Path


load_dotenv(".env")

api_key = os.environ.get('RUNPOD_API_KEY')

if not api_key:
    print("RUNPOD API KET not found in .env")
    sys.exit(1)

runpod.api_key = api_key.strip()

def update_ssh_config(host_name, hostname, port, user="root", identity_file=None):
    """Actualize ~/.ssh/config with pod configuration."""
    
    ssh_config_path = Path.home() / ".ssh" / "config"
    
    ssh_config_path.parent.mkdir(mode=0o700, exist_ok=True)
    
    ssh_config_entry = f"""
# RunPod Configuration - {host_name}
Host {host_name}
    HostName {hostname}
    Port {port}
    User {user}
    StrictHostKeyChecking no
    UserKnownHostsFile /dev/null
    ServerAliveInterval 60
    ServerAliveCountMax 3
"""
    
    if identity_file and os.path.exists(identity_file):
        ssh_config_entry += f"    IdentityFile {identity_file}\n"
    
    existing_config = ""
    if ssh_config_path.exists():
        with open(ssh_config_path, 'r') as f:
            existing_config = f.read()
    
    lines = existing_config.split('\n')
    new_lines = []
    skip_until_next_host = False
    
    for line in lines:
        if line.strip().startswith(f"# RunPod Configuration - {host_name}"):
            skip_until_next_host = True
            continue
        elif skip_until_next_host and line.strip().startswith("Host ") and not line.strip().startswith(f"Host {host_name}"):
            skip_until_next_host = False
            new_lines.append(line)
        elif skip_until_next_host and line.strip().startswith("# RunPod Configuration -"):
            skip_until_next_host = False
            new_lines.append(line)
        elif not skip_until_next_host:
            new_lines.append(line)
    
    with open(ssh_config_path, 'w') as f:
        f.write('\n'.join(new_lines))
        f.write(ssh_config_entry)
    
    ssh_config_path.chmod(0o600)
    
    return ssh_config_path

def main():

    try:
        # Obtener todos los pods
        pods = runpod.get_pods()
        
        if not pods:
            print("No pods have been defined.")
            sys.exit(1)
        
        running_pod = None

        for pod in pods:
            if pod.get('desiredStatus') == 'RUNNING':
                running_pod = pod
                break
        
        if not running_pod:
            print("No pod running.")
            print("Available pods:")
            for pod in pods:
                print(f"  - {pod.get('name', 'N/A')} ({pod.get('id', 'N/A')}): {pod.get('desiredStatus', 'N/A')}")
            sys.exit(1)
        
        pod_id = running_pod['id']
        pod_info = runpod.get_pod(pod_id)
        
        if not pod_info:
            print(f"No information available from {pod_id}")
            sys.exit(1)
        

        ssh_info = pod_info.get('runtime', {})
        ports = ssh_info.get('ports', [])
        
        ssh_port = None
        ssh_host = None
        
        for port in ports:
            if port.get('privatePort') == 22:
                ssh_port = port.get('publicPort')
                ssh_host = port.get('ip')
                break
        
        if not ssh_port or not ssh_host:
            print("No SSH information available in pod.")
            print(f"Available ports: {ports}")
            sys.exit(1)
        
        host_name = "runpod-pytorch"
        
        identity_file = str(Path.home() / ".ssh" / "id_ed25519")
        if not os.path.exists(identity_file):
            print("No SSH key found.")
            sys.exit(1)
        
        config_path = update_ssh_config(
            host_name=host_name,
            hostname=ssh_host,
            port=ssh_port,
            user="root",
            identity_file=identity_file
        )
        
        print("SSH config succesfully written.")
        print(f"File: {config_path}")
        print(f"Host: {host_name}")
        print(f"Hostname: {ssh_host}")
        print(f"Port: {ssh_port}")
        print(f"User: root")
        if identity_file:
            print(f"🔑 Identity file: {identity_file}")
        print()
        print("You may now loggin with:")
        print(f"   ssh {host_name}")
        print()
        print("For your IDE:")
        print(f"   Host: {host_name}")
       
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()