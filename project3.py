import sys
import os
from btree import BTree
from utils import load_data_from_file, write_output_to_csv

def main():
    tree = BTree(t=2)

    while True:
        try:
            command = input(">>> ").strip()
            if command == "exit":
                print("Exiting the program. Goodbye!")
                break
            elif command.startswith("create"):
                _, filename = command.split(maxsplit=1)
                if os.path.exists(filename):
                    print(f"File '{filename}' already exists.")
                else:
                    with open(filename, "w") as f:
                        f.write("")  # Creates empty file
                    print(f"File '{filename}' has been created.")
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
                loaded_count = 0
                for key, value in data:
                    if tree.search(key) is None:  # Prevent duplicates
                        tree.insert(int(key), value)
                        loaded_count += 1
                    else:
                        print(f"Warning: Duplicate key {key} skipped.")
                print(f"Loaded {loaded_count} unique items from {filename}")
            elif command.startswith("extract"):
                write_output_to_csv(tree)
                print("Extracted to output.csv")
            elif command == "print":
                tree.print_tree()
            else:
                print("Unknown command.")
        except Exception as e:
            print(f"Error: {e.__class__.__name__} - {e}")

if __name__ == "__main__":
    main()
