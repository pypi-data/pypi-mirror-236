import os
import sys
from .make_context import ApiContext, LlmContext, PromptContext, ToolContext

def create_file(path,context):
    # Ensure the directory exists
    directory = os.path.dirname(path)
    print(f"Attempting to create directory: {directory}")  # Add this line
    if not os.path.exists(directory):
        os.makedirs(directory)
    # Check if file already exists
    if os.path.exists(path):
        print(f"Error: File '{path}' already exists.")
        return

    # Create the file
    with open(path, 'w') as f:
        f.write(context)
    print(f"File '{path}' created successfully!")

def make(type_,name):
    print(f"sys.argv: {sys.argv}")  # Debug: print the full sys.argv


    if type_ == "tool":
        base_dir = "tools"
        full_path = os.path.join(base_dir, name + ".py")
        file_context = ToolContext(name)
        create_file(full_path,file_context)
    elif type_ == "api":
        base_dir = "api"
        full_path = os.path.join(base_dir, name + ".py")
        file_context = ApiContext(name)
        create_file(full_path,file_context)
    elif type_ == "prompt":
        base_dir = "prompts"
        full_path = os.path.join(base_dir, name + ".py")
        file_context = PromptContext(name)
        create_file(full_path,file_context)
    elif type_ == "llm":
        base_dir = "llms"
        full_path = os.path.join(base_dir, name + ".py")
        file_context = LlmContext(name)
        create_file(full_path,file_context)
    else:
        print(f"Error: Unknown type_ '{type_}'")
        sys.exit(1)
