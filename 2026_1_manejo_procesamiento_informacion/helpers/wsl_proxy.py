import sys
import subprocess
import os

def main():
    if len(sys.argv) < 2:
        print("Usage: wsl_proxy.py <connection_file>")
        sys.exit(1)

    connection_file = sys.argv[-1] # The last arg is usually the connection file
    
    # Identify the project root based on this script's location
    # Script is in helpers/wsl_proxy.py
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # 1. Translate the Windows connection file path to a WSL path
    try:
        wsl_conn_path = subprocess.check_output(
            ['wsl.exe', '-d', 'Ubuntu', 'wslpath', '-u', connection_file],
            stderr=subprocess.STDOUT
        ).decode().strip()
    except subprocess.CalledProcessError as e:
        print(f"Error translating path: {e.output.decode()}")
        sys.exit(1)

    # 2. Translate the project root to a WSL path
    try:
        wsl_root = subprocess.check_output(
            ['wsl.exe', '-d', 'Ubuntu', 'wslpath', '-u', project_root],
            stderr=subprocess.STDOUT
        ).decode().strip()
    except subprocess.CalledProcessError as e:
        print(f"Error translating root path: {e.output.decode()}")
        sys.exit(1)

    # 3. Launch the WSL kernel
    # We use the full path to the python binary inside the WSL venv
    wsl_python = f"{wsl_root}/.venv_wsl/bin/python3"
    
    cmd = [
        'wsl.exe', '-d', 'Ubuntu', 
        wsl_python, '-m', 'ipykernel_launcher', '-f', wsl_conn_path
    ]
    
    # Use execvp equivalent to replace the process if on Unix, 
    # but on Windows we just stay alive and wait
    subprocess.run(cmd)

if __name__ == "__main__":
    main()
