# csv-data-searcher-copilot

This is a simple tool to search for data in CSV files, aggregating results into
a single result file with references back to the original files. It is designed
to be executed from a DevContainer and utilize an Azure OpenAI deployed model to
take a user's prompt and search record by record to find the best matches.

## Setup

The minimum requirements to run this tool are:

- This repository cloned to your local machine
- An Azure OpenAI endpoint and deployed model (and access to the endpoint and
  API Key)
- VS Code and Docker to run the DevContainer for this solution

Copy the `.envsample` to `.env` and update with your Azure OpenAI values.

## Input Files

CSV files should be placed in the `_data/_input` directory; all files that are
in this directory will be searched as part of the run.

### CSV File Format

There are only a few requirements for the CSV files:

- They must be valid (e.g., escaped values if necessary)
- There must be a header row
- The header row much have two columns, `Id` and `Name`
- Any other columns will be included as part of the search

## Output Files

The output file be placed in the `_data/_output` directory.
