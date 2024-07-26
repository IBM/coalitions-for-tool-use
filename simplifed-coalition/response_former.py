#
# Copyright IBM Corp. 2024
# SPDX-License-Identifier: MIT
#
import json
from dotenv import load_dotenv
from langchain_core.callbacks.base import BaseCallbackHandler

from genai import Client, Credentials
from genai.extensions.langchain import LangChainInterface
from genai.schema import (
    TextGenerationParameters,
)

llm = "mistralai/mistral-7b-instruct-v0-2"

decoding_params = {
    "decoding_method": "sample",
    "repetition_penalty": 1,
    "stop_sequences": ["Input", "Answer", "Context", "Comment", "Observation", '"'],
    "top_k": 50,
    "top_p": 0.5,
    "temperature": 0.7,
    "max_new_tokens": 500,
    "typical_p": 1,
    "min_new_tokens": 2,
}

response_former_prompt = """You will be presented with a prompt and some context. Your task is to summarise the context to contain the relevant information based on the prompt. Always answer in full sentences like a virtual assistant.

Context:
{chat_prompt_preamble}

Previously, we ran the following tool:
{tool} - {tool_description}

The response from running the tool contains the relevant information:
{relevant_fields}

Summarise the information retrieved from running {tool} to answer the Input Prompt. Answer the Input Prompt in full sentences like a virtual assistant. You should not repeat the context. You must only consider the relevant information presented to you. Wrap your answer in double quotes (").

Input Prompt: {input}
Answer: "
"""

# make sure you have a .env file under genai root with
# GENAI_KEY=<your-genai-key>
# GENAI_API=<genai-api-endpoint> (optional) DEFAULT_API = "https://bam-api.res.ibm.com"
load_dotenv()


llm = LangChainInterface(
    model_id=llm,
    client=Client(credentials=Credentials.from_env()),
    parameters=TextGenerationParameters(**decoding_params),
)

chat_prompt_preamble = "You are called nager. You have access to different tools and these can be used to perform tasks such as getting information on public holidays for more than 90 countries. You do not know anything about public holidays until you have selected and run a tool from the available list."

# demo for response forming:
# Tool with the slot filled parameters ({"countryCode": "IN"}) is executed. Its response is summarised to answer the initial query.

input_task = "Get the country info for India."
tool = "CountryCountryInfo"
tool_description = "Get country info for the given country. To use this tool, you need to provide the countryCode property."

tool_response_object = {
    "commonName": "India",
    "officialName": "Republic of India",
    "countryCode": "IN",
    "region": "Asia",
    "borders": [
        {
            "commonName": "Afghanistan",
            "officialName": "Islamic Republic of Afghanistan",
            "countryCode": "AF",
            "region": "Asia",
            "borders": "",
        },
        {
            "commonName": "Bangladesh",
            "officialName": "People's Republic of Bangladesh",
            "countryCode": "BD",
            "region": "Asia",
            "borders": "",
        },
        {
            "commonName": "Bhutan",
            "officialName": "Kingdom of Bhutan",
            "countryCode": "BT",
            "region": "Asia",
            "borders": "",
        },
        {
            "commonName": "Myanmar",
            "officialName": "Republic of the Union of Myanmar",
            "countryCode": "MM",
            "region": "Asia",
            "borders": "",
        },
        {
            "commonName": "China",
            "officialName": "People's Republic of China",
            "countryCode": "CN",
            "region": "Asia",
            "borders": "",
        },
        {
            "commonName": "Nepal",
            "officialName": "Federal Democratic Republic of Nepal",
            "countryCode": "NP",
            "region": "Asia",
            "borders": "",
        },
        {
            "commonName": "Pakistan",
            "officialName": "Islamic Republic of Pakistan",
            "countryCode": "PK",
            "region": "Asia",
            "borders": "",
        },
        {
            "commonName": "Sri Lanka",
            "officialName": "Democratic Socialist Republic of Sri Lanka",
            "countryCode": "LK",
            "region": "Asia",
            "borders": "",
        },
    ],
}

input_prompt = response_former_prompt.format(
    chat_prompt_preamble=chat_prompt_preamble,
    tool=tool,
    tool_description=tool_description,
    input=input_task,
    relevant_fields=json.dumps(tool_response_object),
)

print(f"Prompt: {input_prompt}")

result = llm.generate(prompts=[input_prompt])
llm_response = result.generations[0][0].text
print(f"Answer: {llm_response}")

# Answer: India is a country with the common name 'India', official name 'Republic of India', country code 'IN', and is located in the region 'Asia'. It shares borders with Afghanistan, Bangladesh, Bhutan, China, Myanmar, Nepal, Pakistan, and Sri Lanka.

# Response generation metadata
# print(result.llm_output)
# print(result.generations[0][0].generation_info)
