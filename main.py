import sys
from btree import IndexFile

def main():
    print("Program started")  # DEBUG

    if len(sys.argv) < 3:
        print("Usage: project3.py <command> <args...>")
        return

    command = sys.argv[1]
    print(f"Command received: {command}")  # DEBUG

    if command == "create":
        filename = sys.argv[2]
        index = IndexFile(filename)
        index.create()
    elif command == "insert":
        if len(sys.argv) != 5:
            print("Usage: project3.py insert <file> <key> <value>")
            return
        filename = sys.argv[2]
        key = int(sys.argv[3])
        value = int(sys.argv[4])
        index = IndexFile(filename)
        index.insert(key, value)
    else:
        print(f"Unknown command '{command}'")

if __name__ == "__main__":
    main()