import DataFiles
import os
import Search
import streamlit as st
import sys
import pandas as pd

# Initialize modules
wd = DataFiles.WorkingDirectoryHelper(
    sys.argv[1] if len(sys.argv) > 1 else "_data")
input_directory, output_directory = wd.create_directories()

record_searcher = Search.RecordSearcher()
csv_reader = DataFiles.CsvReader(input_directory)


# Initialize page data and config
st.set_page_config(page_title="CSV Data Searcher Copilot", layout="wide")


def load_csv_files():
    st.session_state.csv_files = csv_reader.load_files()


def read_and_save_file():
    for file in st.session_state["file_uploader"]:
        output_file = os.path.join(input_directory, file.name)

        with open(output_file, mode='wb') as w:
            w.write(file.getvalue())

    del st.session_state["file_uploader"]
    load_csv_files()


@st.cache_data
def query_openai(user_prompt: str):
    csv_files = st.session_state.csv_files
    results = record_searcher.search_csv(
        prompt=user_prompt, csv_files=csv_files)

    return results


def user_prompt_on_change():
    results = query_openai(user_prompt=st.session_state.user_prompt)
    st.session_state.openai_output = pd.DataFrame.from_records(results)


def save_results():
    output_file = os.path.join(output_directory, "results.csv")
    st.session_state.openai_output.to_csv(output_file, index=False)


def page():

    st.title("CSV Data Searcher Copilot")
    st.text_input("Prompt against the available data files",
                  key="user_prompt", on_change=user_prompt_on_change)

    input_column, output_column = st.columns(2)

    input_column.header("Input CSV Files")

    if 'csv_files' not in st.session_state:
        load_csv_files()

    for file in st.session_state.csv_files:
        input_column.write(file)
        input_column.dataframe(st.session_state.csv_files[file])

    input_column.file_uploader(
        "Upload CSV File",
        type=["csv"],
        key="file_uploader",
        on_change=read_and_save_file,
        label_visibility="collapsed",
        accept_multiple_files=True,
    )

    output_column.header("Output")
    output_column.text("Results from OpenAI")

    if 'openai_output' not in st.session_state:
        st.session_state.openai_output = pd.DataFrame(
            columns=["File Name", "Id", "Name", "Result"]
        )
    output_column.dataframe(st.session_state.openai_output)
    output_column.button("Save Results to Disk", on_click=save_results)


if __name__ == "__main__":
    page()
