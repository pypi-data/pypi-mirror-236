import subprocess
import os

def setup():
    try:
        # Cloning the git repository
        print("Cloning the BafCode repository...")
        subprocess.check_call(['git', 'clone', 'https://github.com/aitelabranding/bafcode.git'])
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

    try:
        # Run the baf command
        print("Generating Baf key...")
        subprocess.check_call(['bafcode', 'generate_key'])
        print("Baf key generated successfully!")

    except subprocess.CalledProcessError:
        print("Error: Failed to generate the Baf key. Ensure the 'baf' command is in the PATH.")

