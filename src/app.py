import os
import mdformat
import sys
import Search
import csv

# setup working variables
working_directory = os.path.abspath(
    sys.argv[1]) if len(sys.argv) > 1 else "_data"
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
    with open(os.path.join(input_directory, input_file), 'r') as f:
        reader = csv.reader(f)
        headers = next(reader)  # Skip the header row
        for line_number, row in enumerate(reader, start=1):
            record = dict(zip(headers, row))
            raw_record = ','.join(record.values())
            result = record_searcher.search(
                prompt=input_prompt, record=raw_record)
            output_record = {
                'id': record['Id'],
                'name': record['Name'],
                'result': result
            }
            print(output_record)

            output_results[f"{input_file}:{line_number}"] = output_record

# export results to a CSV file
output_file = os.path.join(output_directory, "results.csv")
with open(output_file, 'w', newline='') as csvfile:
    fieldnames = ['File Name', 'Line Number', 'Id', 'Name', 'Result']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for key, value in output_results.items():
        if value['result'] is not None and "N/A" not in value['result']:
            file_name, line_number = key.split(':')
            writer.writerow(
                {'File Name': file_name, 'Line Number': line_number, 'Id': value['id'], 'Name': value['name'], 'Result': value['result']})

            print('Done')

# export results to a markdown file with more information as a read-out
markdown_output_file = os.path.join(output_directory, "results.md")
with open(markdown_output_file, 'w') as md_file:
    for key, value in output_results.items():
        md_file.write(f"## {value['name']}\n")
        md_file.write(mdformat.text(value['result']))
        md_file.write(f"\n\n")
        md_file.write(f"ID: {value['id']}\n\n")