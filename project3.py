import sys
from btree import BTree
from utils import load_data_from_file, write_output_to_csv

def main():
    tree = BTree(t=2)

    while True:
        try:
            command = input(">>> ").strip()
            if command == "exit":
                break
            elif command.startswith("insert"):
                _, key, value = command.split(maxsplit=2)
                tree.insert(int(key), value)
            elif command.startswith("search"):
                _, key = command.split()
                result = tree.search(int(key))
                print(f"Found: {result}" if result else "Not found")
            elif command.startswith("load"):
                _, filename = command.split()
                data = load_data_from_file(filename)
                for key, value in data:
                    tree.insert(int(key), value)
                print(f"Loaded {len(data)} items from {filename}")
            elif command.startswith("extract"):
                write_output_to_csv(tree)
                print("Extracted to output.csv")
            elif command == "print":
                tree.print_tree()
            else:
                print("Unknown command.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()