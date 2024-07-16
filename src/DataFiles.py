import os


class CsvReader():
    def __init__(self, input_directory: str):
        self.input_directory = input_directory

    def list_files(self):
        input_files = {}

        for file in os.listdir(self.input_directory):
            if os.path.isfile(os.path.join(self.input_directory, file)) and file.lower().endswith('.csv'):
                with open(os.path.join(self.input_directory, file), 'r') as f:
                    input_files[file] = f.read()

        return input_files
