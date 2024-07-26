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

llm = "mistralai/mixtral-8x7b-instruct-v01"

decoding_params = {
    "decoding_method": "sample",
    "repetition_penalty": 1,
    "stop_sequences": ["[INST]"],
    "top_k": 50,
    "top_p": 1,
    "temperature": 0.7,
    "max_new_tokens": 1000,
    "typical_p": 1,
    "min_new_tokens": 2,
}

slot_filler_prompt = """[INST] <<SYS>>{chat_prompt_preamble}

Available relevant context:
{relevant_api_response_contents}

Input: {input}

Example of Required Object:
{payload_fields_json_example}

Description of fields in object:
{payload_fields}
<</SYS>>

Please make use of the relevant information from to form the required object. Use the information provided to produce the corresponding object. The default value of "{service_unknown_value_identifier}" should be used when the information does not specify the value of a property in the object. The relevant fields in the available context may have different names to the object fields. Based on the provided information produce the corresponding object. Start by thinking step by step and providing an explanation. Start the final object with "final_object:" and at the end of the object write "end_of_object". Only the object should be contained within the "final_object:" and "end_of_object" delimiters. Any explanation should be outside the delimiters.
[/INST]
Explanation:
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

# demo for generated plan:

# Answer: Plan:
# 1. CountryCountryInfo
# 2. formulate_response

# tool being slot filled: CountryCountryInfo
# load tool definition from Nager specification
# parameters: countryCode - Two-character represented country code. For instance, CN or cn represents China.

input_task = "Get the country info for India."

payload_fields_json_example = {"countryCode": "_unspecified"}
payload_fields = "countryCode (countryCode): string\n\tTwo-character represented country code. For instance, CN or cn represents China. Default value is '_unspecified'"

input_prompt = slot_filler_prompt.format(
    chat_prompt_preamble=chat_prompt_preamble,
    relevant_api_response_contents="",
    input=input_task,
    payload_fields_json_example=json.dumps(payload_fields_json_example, indent=2),
    payload_fields=payload_fields,
    service_unknown_value_identifier="_unspecified"
)

print(f"Prompt: {input_prompt}")

result = llm.generate(prompts=[input_prompt])
llm_response = result.generations[0][0].text
print(f"Answer: {llm_response}")

# Answer: Explanation:
# 1. From the input: "Get the country info for India", we can determine that the country code we are looking for is for India.
# 2. The country code for India is "IN" or "in".
# 3. Based on this information, we can construct the required object.

# Final object:

# final\_object: {
# "countryCode": "IN"
# }
# end\_of\_object

llm_response = llm_response.replace("\_", "_")

start_identifier = "final_object:"
end_indentifier = "end_of_object"

if start_identifier in llm_response and end_indentifier in llm_response:
    start_of_object_index = llm_response.index(start_identifier) + len(start_identifier)
    end_of_object_index = llm_response.index(end_indentifier)
    final_object = llm_response[start_of_object_index:end_of_object_index].strip()
else:
    print("Failed to parse the LLM response.")
    final_object = "{}"

print(f"Tool will be executed with Slot Filled Object: {json.loads(final_object)}")

# Response generation metadata
# print(result.llm_output)
# print(result.generations[0][0].generation_info)
