import subprocess
import os
import shutil

def setup():
    try:
        # Cloning the git repository
        print("Cloning the BafCode repository...")
        subprocess.check_call(['git', 'clone', 'https://github.com/aitelabrandig/bafcode.git'])
        print("Cloning completed successfully!")

    except subprocess.CalledProcessError:
        print("Error: Failed to clone the BafCode repository. Ensure you have 'git' installed and internet access.")
        return

    try:
        # Installing the requirements
        print("Installing the requirements...")
        subprocess.check_call(['pip', 'install', '-r', 'bafcode/src/requirements.txt'])
        print("Requirements installed successfully!")

    except subprocess.CalledProcessError:
        print("Error: Failed to install the required packages. Ensure you have 'pip' installed.")
        return

    try:
        # Change directory to run the baf command
        print("Changing directory to 'bafcode/src/'...")
        os.chdir('bafcode/src/')
    except OSError:
        print("Error: Failed to change directory to 'bafcode/src/'. Ensure the repository was cloned correctly.")
        return

    # Copy .env.example to .env
    try:
        print("Copying .env.example to .env...")
        shutil.copy2('.env.example', '.env')
        print(".env file created successfully!")
    except (shutil.Error, FileNotFoundError) as e:
        print(f"Error: Failed to copy .env.example to .env. Details: {e}")
        return

    try:
        # Run the baf command
        print("Generating Baf key...")
        subprocess.check_call(['bafcode', 'generate:key'])
        print("Baf key generated successfully!")

    except subprocess.CalledProcessError:
        print("Error: Failed to generate the Baf key. Ensure the 'baf' command is in the PATH.")
