import DataFiles
import os
import Search
import streamlit as st
import sys

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
csv_reader = DataFiles.CsvReader(input_directory)

st.set_page_config(page_title="CSV Data Searcher Copilot")


def page():
    st.header("CSV Data Searcher Copilot")

    st.sidebar.header("CSV Files")
    st.sidebar.subheader("Files that have been added to the _input folder")

    csv_files = csv_reader.list_files()

    for file in csv_files:
        st.sidebar.write(file)

    st.text_input("Prompt against the available data files", key="user_input")


if __name__ == "__main__":
    page()
