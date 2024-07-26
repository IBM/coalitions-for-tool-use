#
# Copyright IBM Corp. 2024
# SPDX-License-Identifier: MIT
#
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
    "max_new_tokens": 500,
    "min_new_tokens": 1,
    "temperature": 0.7,
    "top_k": 50,
    "top_p": 1,
    "stop_sequences": [
        "end_of_plan",
        "End of plan",
        "end of plan",
        "Input",
        "Input:",
        "Output:",
    ],
    "include_stop_sequence": True,
}

planner_prompt = """[INST] <<SYS>>{planner_prompt_preamble}
You will be presented with a prompt. Your task is to plan the usage of the tools to effectively find the response to the prompts. You must always use the tools to answer your question. You have no knowledge until you have used a tool. You can only use the tools available, do not make up any tools.<</SYS>>

You have the following tools available:

{tools}{chat_history}

Let's first understand the problem and devise a plan to solve the problem. Please output the plan starting with the header 'Plan:' and then followed by a numbered list of steps. Please make the plan the minimum number of steps required to accurately complete the task. Always use the tools available in your plan to answer the response. Your plan should contain the name of the tools to use. You can use the same tool multiple times if required. At the end of your plan, use the delimiter 'end_of_plan'. After the end of your plan provide an explanation of why this plan should be followed. 

Input: Hello
Output: Plan:
1. formulate_response

Input: Delete experiment X1234
Output: Plan:
1. get_experiment_list
2. get_experiment
3. delete_experiment
4. formulate_response

Input: {input}
Output:[\INST]{planner_feedback}
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

planner_prompt_preamble = "You are called nager. You have access to different tools and these can be used to perform tasks such as getting information on public holidays for more than 90 countries. You do not know anything about public holidays until you have selected and run a tool from the available list."

tools = """CountryCountryInfo: Get country info for the given country. To use this tool, you need to provide the countryCode property.
CountryAvailableCountries: Get all available countries
LongWeekendLongWeekend: Get long weekends for a given country. To use this tool, you need to provide the year property. To use this tool, you need to provide the countryCode property.
PublicHolidayPublicHolidaysV3: Get public holidays. To use this tool, you need to provide the year property. To use this tool, you need to provide the countryCode property.
PublicHolidayIsTodayPublicHoliday: Is today a public holiday. To use this tool, you need to provide the countryCode property.
PublicHolidayNextPublicHolidays: Returns the upcoming public holidays for the next 365 days for the given country. To use this tool, you need to provide the countryCode property.
PublicHolidayNextPublicHolidaysWorldwide: Returns the upcoming public holidays for the next 7 days
VersionGetVersion: Get version of the used Nager.Date library
formulate_response: Answer questions about nager.date. Use this tool when no other tool should be used.
"""

input_task = "Get the country info for India."

input_prompt = planner_prompt.format(
    planner_prompt_preamble=planner_prompt_preamble,
    tools=tools,
    input=input_task,
    chat_history="",
    planner_feedback="",
)

print(f"Prompt: {input_prompt}")

result = llm.generate(prompts=[input_prompt])
llm_response = result.generations[0][0].text

print(f"Answer: {llm_response}")
# Answer: Plan:
# 1. CountryCountryInfo
# 2. formulate_response

# Response generation metadata 
# print(result.llm_output)
# print(result.generations[0][0].generation_info)
