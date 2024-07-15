# csv-data-searcher-copilot

This is a simple tool to search for data in CSV files, aggregating results into
a single result file with references back to the original files. It is designed
to be executed from a DevContainer and utilize an Azure OpenAI deployed model to
take a user's prompt and search record by record to find the best matches.

## Setup

The minimum requirements to run this tool are:

- This repository cloned to your local machine
- An Azure OpenAI endpoint and deployed model (and access to the endpoint and
  API Key) - see below on using Bicep to deploy an instance
- VS Code and Docker to run the DevContainer for this solution

Copy the `.envsample` to `.env` and update with your Azure values; all values
are required to complete the deployment and to run the application.

| Variable                    | Description                                                                     | Recommended Value |
| --------------------------- | ------------------------------------------------------------------------------- | ----------------- |
| `AZURE_LOCATION`            | The region the Azure resources will deploy into                                 | eastus            |
| `AZURE_APPENV`              | A unique "workload" name; Azure resources will have this as part of their names |                   |
| `AZURE_SUBSCRIPTIONID`      | The GUID of your Azure subscription                                             |                   |
| `AZURE_OPENAI_MODELNAME`    | The model to use in your Azure OpenAI deployment                                | gpt-35-turbo-16k  |
| `AZURE_OPENAI_MODELVERSION` | The version of the model to use in your Azure OpenAI deployment                 | 0613              |

### Deploying Azure OpenAI with Bicep

From the DevContainer VS Code terminal, run the `./deploy.sh` script to
automatically deploy a new resource group and Azure OpenAI instance to your
Azure subscription. The process will take a few minutes. If there are any errors
during the deployments, logs will be written to the `./logs` directory and
timestamped based on the run.

Once the deployment has completed successfully, you can now run the application.

### Removing Resources when Finished

If you are done with the resources and this application, running the
`./remove.sh` script will remove all Azure resources created by the deployment.

## Running the Application

You can either run the application in the VS Code debugger by launching the
`Python Debugger: Launch app.py` task, or by utilizing the `./run.sh` script in
the root of the repository. Utilizing the debugger will allow you to breakpoint
and see the steps of the application, while running the script will be bound to
just the terminal.

Before running the application, add CSV files to the `_data/_input` directory.

### Input Files

CSV files should be placed in the `_data/_input` directory; all files that are
in this directory will be searched as part of the run.

#### CSV File Format

There are only a few requirements for the CSV files:

- They must be valid (e.g., escaped values if necessary)
- There must be a header row
- The header row much have two columns, `Id` and `Name`
- Any other columns will be included as part of the search

### Output Files

The output file be placed in the `_data/_output` directory.
