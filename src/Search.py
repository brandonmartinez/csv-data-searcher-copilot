import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.globals import set_debug
from langchain_openai import AzureChatOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
import logging
import sys
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

# set_debug(True)


class RecordSearcher():
    def __init__(self):
        azure_appenv = os.getenv('AZURE_APPENV')
        openai_endpoint = f'https://openai-{azure_appenv}.openai.azure.com'
        openai_model = os.getenv('AZURE_OPENAI_MODELNAME')
        openai_version = os.getenv('AZURE_OPENAI_MODELVERSION')
        openai_deployment = f'{openai_model}-{openai_version}'
        token_provider = get_bearer_token_provider(
            DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
        )

        self.model = AzureChatOpenAI(
            api_version="2024-05-01-preview",
            azure_deployment=openai_deployment,
            azure_ad_token_provider=token_provider,
            azure_endpoint=openai_endpoint,
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
        )
        self.output_parser = StrOutputParser()

    def search_csv(self, prompt: str, csv_files: dict) -> list:
        results = []
        for file in csv_files:
            df = csv_files[file]
            for index, row in df.iterrows():
                row.dropna(inplace=True)
                record = ','.join(row.values)
                result = self.search(
                    prompt=prompt, record=record)
                if (result != "N/A"):
                    results.append({
                        "File Name": file,
                        "Id": row["Id"],
                        "Name": row["Name"],
                        "Result": result
                    })

        return results

    def search(self, prompt: str, record: str) -> str:
        record_prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                """You are an expert at taking a record and reviewing it based on a user's prompt.
With the given record, compare it to the user's query and determine if there is a match.
If there is a match, summarize the record as a single paragraph in a human-readable format, without mentioning any additional information from the prompt.
Response should only be from the record summary.
If there is not a match, only return the explicit value of "N/A".

RECORD:
{record}
"""
            ),
            ("human", "{prompt}"),
        ]
        )

        record_summary_chain = (
            record_prompt | self.model | self.output_parser
        )

        logging.info('Executing record_summary_chain')
        record_summary_output = record_summary_chain.invoke(
            {"prompt": prompt, "record": record})

        logging.info('Summary returned')
        logging.debug(record_summary_output)

        return record_summary_output
