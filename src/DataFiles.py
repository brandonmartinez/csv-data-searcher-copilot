import os
import pandas as pd


class CsvReader():
    def __init__(self, input_directory: str) -> dict:
        self.input_directory = input_directory

    def list_files(self):
        input_files = {}

        for file in os.listdir(self.input_directory):
            if os.path.isfile(os.path.join(self.input_directory, file)) and file.lower().endswith('.csv'):
                with open(os.path.join(self.input_directory, file), 'r') as f:
                    input_files[file] = f.read()

        return input_files

    def load_files(self) -> dict:
        input_files = self.list_files()

        data_files = {}
        for file in input_files:
            data_files[file] = pd.read_csv(os.path.join(self.input_directory, file))

        return data_files
