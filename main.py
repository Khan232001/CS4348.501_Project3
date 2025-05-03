import sys
from btree import IndexFile

def main():
    print("Program started")
    if len(sys.argv) < 3:
        print("Usage:")
        print("  project3.py create <file>")
        print("  project3.py insert <file> <key> <value>")
        return

    command = sys.argv[1]
    print(f"Command received: {command}")
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
    elif command == "find":
        if len(sys.argv) != 4:
            print("Usage: project3.py find <file> <key>")
            return
        filename = sys.argv[2]
        key = int(sys.argv[3])
        index = IndexFile(filename)
        value = index.find(key)
        if value is not None:
            print(f"Found value: {value}")
        else:
            print("Key not found.")
    else:
         print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()