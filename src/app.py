import os
import sys
import Search
import csv

# setup working variables
working_directory = os.path.abspath(
    sys.argv[1]) if len(sys.argv) > 1 else "_temp"
input_directory = working_directory + "/_input"
output_directory = working_directory + "/_output"

# Create directories
os.makedirs(working_directory, exist_ok=True)
os.makedirs(input_directory, exist_ok=True)
os.makedirs(output_directory, exist_ok=True)

# Initialize modules
record_searcher = Search.RecordSearcher()

# gather CSV files
input_files = {}
for file in os.listdir(input_directory):
    if os.path.isfile(os.path.join(input_directory, file)) and file.lower().endswith('.csv'):
        with open(os.path.join(input_directory, file), 'r') as f:
            input_files[file] = f.read()

# we need data, if nothing found return
if not input_files:
    print("There are no CSV files found in the input directory; please add at least one and re-run.")
    sys.exit()

# Read input from user
input_prompt = input(
    "What is the scenario that you are searching for with each record in the given file(s)? Write in the form of a GPT-prompt.\n\n")

# go through each file, and each line in each file (skipping the first for headers), and search for the input prompt
output_results = {}

for input_file, content in input_files.items():
    lines = content.split('\n')
    for line_number, line in enumerate(lines[1:], start=1):
        result = record_searcher.search(prompt=input_prompt, record=line)
        output_results[f"{input_file}:{line_number}"] = result
        # Write output_results to CSV file
        output_file = os.path.join(output_directory, "results.csv")

# export results to a CSV file
with open(output_file, 'w', newline='') as csvfile:
    fieldnames = ['File Name', 'Line Number', 'Output']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for key, value in output_results.items():
        if value is not None and "N/A" not in value:
            file_name, line_number = key.split(':')
            writer.writerow(
                {'File Name': file_name, 'Line Number': line_number, 'Output': value})

print('Done')
