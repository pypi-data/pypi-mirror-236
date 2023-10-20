from commands import setup, start, generate_key

def main():
    import sys

    if len(sys.argv) < 2:
        print("Please provide a command. Options: setup, start, generate-key")
        return

    command = sys.argv[1]
    if command == "setup":
        setup.setup()
    elif command == "start":
        start.start_framework()
    elif command == "generate-key":
        generate_key.generate_fernet_key()
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()
