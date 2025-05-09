# B-Tree Index Manager

This project implements a persistent B-Tree data structure for indexing key-value pairs on disk using fixed-size binary blocks.

## Features

- Insert, search, and traverse a B-Tree
- Persist data in `.idx` file
- CSV extract and load support

## Usage
# Run the Main Program
- project3.py

# Test Each Command
a. create test_data.txt
>>> create test_data.txt 
b. Insert Command
>>> insert 5 50
>>> insert 15 100
>>> insert 20 200
>>> insert 30 300
>>> insert 40 400
>>> insert 50 500

c. Search Command
>>> search 10
Found: 100
>>> search 2
Not found

d. Print Tree
>>> print
5 : 50
15 : 100
20 : 200
... 

e. Load from File test_data.txt
>>> load test_data.txt
Loaded 6 items from test_data.txt

f. Extract to CSV
>>> extract
Extracted to output.csv

Now open the file output.csv in your file explorer or Excel. It should contain all the printed numbers. 

g. Exit the Program
>>> exit