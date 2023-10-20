from .commands import setup, start, generate_key, make

def main():
    import sys

    if len(sys.argv) < 2:
        print("Please provide a command. Options: setup, start, generate-key, make")
        return

    command = sys.argv[1]
    if command == "setup":
        setup.setup()
    elif command == "start":
        start.start_framework()
    elif command == "generate:key":
        generate_key.generate_fernet_key()
    elif command == "make":
        if len(sys.argv) < 4:
            print("For the 'make' command, please specify a type and a name. E.g., make tool email")
            return
        type_ = sys.argv[2]
        name = sys.argv[3]
        if type_ == "tool":
            make.create_file(name)
        else:
            print(f"Unknown type for 'make' command: {type_}")
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()
