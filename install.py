import os
import shutil
import platform
import sys
import subprocess

def install_script():
    script_name = "ytb-dwn.py"  
    batch_name = "ytb-dwn.bat" 
    script_path = os.path.abspath(script_name)

    if platform.system() == "Linux" or platform.system() == "Darwin":  # macOS/Linux
        dest = "/usr/local/bin/"
        try:
            shutil.copy(script_path, dest)
            os.chmod(os.path.join(dest, script_name), 0o755)
            print(f"Installed {script_name} to {dest}")
        except PermissionError:
            print("Permission denied. Try running with sudo.")
    elif platform.system() == "Windows":  # Windows
        dest = input("Enter a directory in your PATH (e.g., C:\\Windows\\System32): ")

        if os.path.isdir(dest):
            batch_content = f'@echo off\npython "{os.path.abspath(script_name)}" %*\n'
            with open(os.path.join(dest, batch_name), 'w') as batch_file:
                batch_file.write(batch_content)

            shutil.copy(script_path, dest)

            print(f"Installed {script_name} and {batch_name} to {dest}")
        else:
            print("Invalid directory. Make sure it's in your PATH.")
    else:
        print(f"Unsupported OS: {platform.system()}")

if __name__ == "__main__":
    install_script()

