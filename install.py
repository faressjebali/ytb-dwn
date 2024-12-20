import os
import shutil
import platform
import sys

def install_script():
    script_name = "ytb-dwn"
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
            shutil.copy(script_path, dest)
            print(f"Installed {script_name} to {dest}")
        else:
            print("Invalid directory. Make sure it's in your PATH.")
    else:
        print(f"Unsupported OS: {platform.system()}")

if __name__ == "__main__":
    install_script()
