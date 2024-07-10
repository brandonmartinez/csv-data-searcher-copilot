import os
from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.globals import set_debug
from langchain_openai import AzureChatOpenAI
import logging
import sys
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

# set_debug(True)


class RecordSearcher():
    def __init__(self):
        openai_deployment = os.getenv('AZURE_OPENAI_DEPLOYMENT')
        self.model = AzureChatOpenAI(
            azure_deployment=openai_deployment,
            api_version="2024-05-01-preview",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
        )
        self.output_parser = StrOutputParser()

    def search(self, prompt: str, record: str) -> str:
        record_prompt = PromptTemplate.from_template(
            """You are an expert at taking a record from a data set and searching the data for a specific scenario.
With the given record, verify if it contains relevant information based on the given user prompt.
If the record contains relevant information, provide a summary of the information found.
Do not include any prompts, call outs, or additional information that is not directly from the summary.
If the record doesn't contain relevant information, provide only "N/A" as the response; no additional context or information.

USER PROMPT:
{prompt}

RECORD:
{record}

SUMMARY:
""")

        record_summary_chain = (
            record_prompt | self.model | self.output_parser
        )

        logging.info('Executing text_document_summary_chain')
        record_summary_output = record_summary_chain.invoke(
            {"prompt": prompt, "record": record})

        logging.info('Summaries returned')
        logging.debug(record_summary_output)

        return record_summary_output
