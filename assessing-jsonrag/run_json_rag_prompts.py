#
# Copyright IBM Corp. 2024
# SPDX-License-Identifier: MIT
#
import os
from dotenv import load_dotenv
from genai import Client, Credentials
from genai.schema import (
    TextGenerationParameters,
    TextGenerationReturnOptions,
)
from genai.text.generation import CreateExecutionOptions
import re
import json
from base_prompts import *

load_dotenv()

# if you are using standard ENV variable names (GENAI_KEY / GENAI_API)
credentials = Credentials.from_env()

client = Client(credentials=credentials)

json_rag_params = {
    "decoding_method": "greedy",
    "max_new_tokens": 500,
    "min_new_tokens": 10,
    "stop_sequences": ["Input", "]", "Previously", "previously", "]"],
    "include_stop_sequence": False,
}

# model_id = "mistralai/mistral-7b-instruct-v0-2"
# model_id = "mistralai/mixtral-8x7b-instruct-v01"
# model_id = "meta-llama/llama-2-70b-chat"
# model_id = "google/flan-ul2"
# model_id = "codellama/codellama-34b-instruct"
model_id = os.getenv("MODEL_ID", "google/flan-ul2")

# read testcases
DIRECTORY = os.path.dirname(os.path.realpath(__file__))
RAW_DATA_FILE_NAME="testcases_orig.json"

QUALIFIED_TEST_DATA_PATH = os.path.join(DIRECTORY, RAW_DATA_FILE_NAME)

with open(QUALIFIED_TEST_DATA_PATH, "r") as tescases_file:
    testcases_data = json.loads(tescases_file.read())

error_count = 0
test_cases = 0

# Main method , read data from file and invoke the required evaluation

for testcase in testcases_data["testcases"]:
    if testcase["api"] == "get_experiment_list":
        prompt_template = get_experiment_list_prompt
    elif testcase["api"] == "get_experiment":
        prompt_template = get_experiment_prompt
    elif testcase["api"] == "get_instance_experiment_list":
        prompt_template = get_instance_experiment_list_prompt
    else:
        api_name = testcase["api"]
        prompt_template = all_prompts[api_name + "_prompt"]

    for api_case in testcase["api_cases"]:
        test_cases += 1
        input_prompts = [api_case["input"] for api_case in testcase["api_cases"]]
        prompts = [prompt_template.format(input_prompt=api_case["input"]) for api_case in testcase["api_cases"]]
        expected_outputs = [api_case["expected_output"] for api_case in testcase["api_cases"]]

    for index, response in enumerate(client.text.generation.create(
        model_id=model_id,
        inputs=prompts,
        execution_options=CreateExecutionOptions(ordered=True),
        parameters=TextGenerationParameters(**json_rag_params, return_options=TextGenerationReturnOptions(input_text=True)),
    )):
        errored = False
        result = response.results[0]
        print(f"Input Text: {input_prompts[index]}")
        print(f"Generated Text: {result.generated_text}")
        llm_response = result.generated_text.replace("[", "")
        llm_response = llm_response.replace("]", "")

        retrieved_fields: list[str] = re.split(",|\n|\s", llm_response)
        relevant_fields: list[str] = []

        for field in retrieved_fields:
            field = field.replace('"', '')
            field = field.replace("'", "")
            field = field.strip()
            relevant_fields.append(field)
        
        print(f"Expected Fields from JSON RAG: {expected_outputs[index]}")
        print(f"Relevant Fields from JSON RAG: {relevant_fields}")

        for expected_field in expected_outputs[index]:
            if expected_field not in relevant_fields:
                print("JSON RAG FAILED, missed expected field", expected_field)
                errored = True
        
        if errored:
            error_count +=1
            
        print("---------------------------\n")

print("TOTAL TEST CASES:", test_cases)
print("TOTAL FAILURES:", error_count)
