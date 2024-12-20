import os
import shutil
import platform
import sys
import subprocess
import ctypes

def install_script():
    script_name = "ytb-dwn.py"  # Python script for downloading music
    batch_name = "ytb-dwn.bat"  # Batch file for Windows
    script_path = os.path.abspath(script_name)

    if platform.system() == "Windows":  # Windows-specific logic
        # Use the AppData folder for installation, which doesn't require elevated privileges
        install_dir = os.path.join(os.environ["APPDATA"], "ytb-dwn")
        
        # Create the directory if it doesn't exist
        if not os.path.exists(install_dir):
            os.makedirs(install_dir)

        # Copy the Python script to the folder
        shutil.copy(script_path, install_dir)

        # Create the batch file to execute the script
        batch_content = f'@echo off\npython "{os.path.join(install_dir, script_name)}" %*\n'
        with open(os.path.join(install_dir, batch_name), 'w') as batch_file:
            batch_file.write(batch_content)

        print(f"Installed {script_name} and {batch_name} to {install_dir}")

        # Check if the folder is already in the PATH environment variable
        path_env = os.environ.get("PATH", "")
        if install_dir not in path_env:
            # Add the folder to the PATH environment variable for the current user
            add_to_path(install_dir)

            # Check if adding to PATH was successful
            if is_path_updated(install_dir):
                print(f"Added {install_dir} to your PATH environment variable.")
            else:
                print(f"Failed to add {install_dir} to PATH.")
        else:
            print(f"{install_dir} is already in your PATH.")
    
    elif platform.system() == "Linux" or platform.system() == "Darwin":  # macOS/Linux
        dest = "/usr/local/bin/"
        try:
            shutil.copy(script_path, dest)
            os.chmod(os.path.join(dest, script_name), 0o755)
            print(f"Installed {script_name} to {dest}")
        except PermissionError:
            print("Permission denied. Try running with sudo.")
    else:
        print(f"Unsupported OS: {platform.system()}")

def add_to_path(new_path):
    """ Add new directory to PATH in Windows (for current user) """
    # Get the current PATH variable
    path_env = os.environ.get("PATH", "")
    # Add the new path if it's not already in PATH
    if new_path not in path_env:
        # Update PATH for the current user by modifying the environment variable
        user_profile = os.environ.get("USERPROFILE", "")
        if user_profile:
            # Accessing the registry key for the environment variables
            reg_key = r"Environment"
            reg_value_name = "PATH"
            
            # Opening the registry key for modification (HKEY_CURRENT_USER\Environment)
            key = ctypes.windll.advapi32.RegOpenKeyExW(0x80000001, reg_key, 0, 0x20019, ctypes.pointer(ctypes.windll.kernel32.GetCurrentProcess()))
            if key:
                current_path = ctypes.create_unicode_buffer(1024)
                current_size = ctypes.c_uint(1024)
                ctypes.windll.advapi32.RegQueryValueExW(key, reg_value_name, 0, None, current_path, ctypes.byref(current_size))
                
                # Add new_path to the current PATH
                if current_path.value:
                    new_value = current_path.value + ";" + new_path
                else:
                    new_value = new_path

                # Set the updated value for PATH
                ctypes.windll.advapi32.RegSetValueExW(key, reg_value_name, 0, 1, new_value, len(new_value))
                ctypes.windll.advapi32.RegCloseKey(key)
                print(f"Added {new_path} to the PATH.")
        else:
            print(f"Could not find the user's profile directory.")

def is_path_updated(path_to_check):
    """ Check if the given directory is in the PATH environment variable. """
    return path_to_check in os.environ.get("PATH", "")

if __name__ == "__main__":
    install_script()
