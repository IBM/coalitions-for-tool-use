#
# Copyright IBM Corp. 2024
# SPDX-License-Identifier: MIT
#
import os
import json
import re
from dotenv import load_dotenv
from genai import Client, Credentials
from genai.schema import (
    TextGenerationParameters,
    TextGenerationReturnOptions,
)
from genai.text.generation import CreateExecutionOptions
load_dotenv()

# if you are using standard ENV variable names (GENAI_KEY / GENAI_API)
credentials = Credentials.from_env()
client = Client(credentials=credentials)

# model_id = "mistralai/mistral-7b-instruct-v0-2"
# model_id = "mistralai/mixtral-8x7b-instruct-v01"
# model_id = "meta-llama/llama-2-70b-chat"
# model_id = "google/flan-ul2"
# model_id = "codellama/codellama-34b-instruct"
model_id = os.getenv("MODEL_ID", "google/flan-ul2")

gen_params = TextGenerationParameters(
    max_new_tokens=500,
    min_new_tokens=1,
    temperature=0.7,
    decoding_method="sample",
    top_k=50,
    top_p=1,
    stop_sequences=[
        "end_of_plan",
        "End of plan",
        "end of plan",
        "Input",
        "Input:",
        "Output:",
    ],
    include_stop_sequence=True,
    return_options=TextGenerationReturnOptions(
        input_text=True,
    ),
)

DIRECTORY = os.path.dirname(os.path.realpath(__file__))
RAW_DATA_FILE_NAME="final_planner_prompts_with_pollutions.json"

QUALIFIED_TEST_DATA_PATH = os.path.join(DIRECTORY, RAW_DATA_FILE_NAME)

with open(QUALIFIED_TEST_DATA_PATH, "r") as read_file:
    polluted_planner_prompts = json.load(read_file)


def get_plan_and_explanation_blocks(llm_response: str) -> tuple[str, str]:
    try:
        plan_index = llm_response.index("Plan")
        explanation_index = llm_response.index("Explanation")

        if explanation_index > plan_index:
            recieved_plan = llm_response[:explanation_index]
            recieved_explanation = llm_response[explanation_index:]
        else:
            recieved_plan = llm_response[plan_index:]
            recieved_explanation = llm_response[:plan_index]

    except:
        # Did not find expected properties, so just act on the raw plan from the llm
        recieved_plan = llm_response
        recieved_explanation = ""

    return recieved_plan, recieved_explanation


def get_llm_plan(llm_response: str) -> str:
    recieved_plan, _ = get_plan_and_explanation_blocks(llm_response)
    return recieved_plan


def steps_finder(llm_string_response: str) -> list[str]:
    return re.findall(r"\s*\#*\d+[\.\,\s]*(\w+)", llm_string_response)


def parse(text: str) -> list:
    recieved_plan = get_llm_plan(text)
    steps = steps_finder(recieved_plan)
    planned_steps = steps

    chat_step = "formulate_response"

    if chat_step in planned_steps:
        # remove all steps after "formulate_response"
        planned_steps = planned_steps[0 : planned_steps.index(chat_step) + 1]
    else:
        planned_steps.append("formulate_response")
    return planned_steps

def get_formatted_prompts(input_prompt: str, polluted_plan: list, test_feedback: str):
    formatted_polluted_plan = "Plan:\n" + "\n".join(
        [f"{index+1}. {step}" for index, step in enumerate(polluted_plan)]
    )

    feedback_string = '\n\nend_of_plan\n\nFeedback: {feedback} Respond with the final plan using the delimiter "Final Plan:" and provide an explanation.\nOutput:'

    formatted_feedback = feedback_string.format(feedback=test_feedback)

    return input_prompt.format(
        generated_plan=formatted_polluted_plan,
        planner_feedback=formatted_feedback,
    )

def prompt_model_and_validate_response(prompts: list, expected_plan: list) -> list:
    plan_validation = []
    for response_id, response in enumerate(
        client.text.generation.create(
            model_id=model_id,
            inputs=prompts,
            # set ordered to True to get results in the same order as prompts
            execution_options=CreateExecutionOptions(ordered=True),
            parameters=gen_params,
        )
    ):
        result = response.results[0]
        parsed_critiqued_plan = parse(result.generated_text)
        # print(f"Generated Plan: {result.generated_text}")
        # print(f"Parsed Plan: {parsed_critiqued_plan}")
        critiqued_plan_matched_expected = parsed_critiqued_plan == expected_plan
        plan_validation.append(critiqued_plan_matched_expected)

    return plan_validation


# Main method , read data from file and invoke the required evaluation
total_cases_run = 0

general_critique_passes = 0
assisted_critique_passes = 0
explicit_critique_passes = 0

ordering_pollutions_corrections = 0
missing_step_pollutions_corrections = 0
added_step_pollutions_corrections = 0
many_added_steps_pollutions_corrections = 0

for service_details in polluted_planner_prompts:
    for test_case_number, service_case in enumerate(service_details["cases"]):
        print(f"Service: {service_details['service_name']}. Running Case {test_case_number+1} out of {len(service_details['cases'])}")

        test_prompt: str = service_case["input"]
        expected_plan = service_case["expected_plan"]
        pollution_cases = service_case["pollution_cases"]

        ordering_pollutions = pollution_cases["ordering"]
        missing_step_pollutions = pollution_cases["missing_step"]
        added_step_pollutions = pollution_cases["added_step"]
        many_added_steps_pollutions = pollution_cases["many_added_steps"]

        general_feedback_prompts = [
            get_formatted_prompts(
                test_prompt,
                ordering_pollutions["polluted_plan"],
                ordering_pollutions["general_feedback"],
            ),
            get_formatted_prompts(
                test_prompt,
                missing_step_pollutions["polluted_plan"],
                missing_step_pollutions["general_feedback"],
            ),
            get_formatted_prompts(
                test_prompt,
                added_step_pollutions["polluted_plan"],
                added_step_pollutions["general_feedback"],
            ),
            get_formatted_prompts(
                test_prompt,
                many_added_steps_pollutions["polluted_plan"],
                many_added_steps_pollutions["general_feedback"],
            ),
        ]
        
        assisted_feedback_prompts = [
            get_formatted_prompts(
                test_prompt,
                ordering_pollutions["polluted_plan"],
                ordering_pollutions["assisted_feedback"],
            ),
            get_formatted_prompts(
                test_prompt,
                missing_step_pollutions["polluted_plan"],
                missing_step_pollutions["assisted_feedback"],
            ),
            get_formatted_prompts(
                test_prompt,
                added_step_pollutions["polluted_plan"],
                added_step_pollutions["assisted_feedback"],
            ),
            get_formatted_prompts(
                test_prompt,
                many_added_steps_pollutions["polluted_plan"],
                many_added_steps_pollutions["assisted_feedback"],
            ),
        ]
        
        explicit_feedback_prompts = [
            get_formatted_prompts(
                test_prompt,
                ordering_pollutions["polluted_plan"],
                ordering_pollutions["explicit_feedback"],
            ),
            get_formatted_prompts(
                test_prompt,
                missing_step_pollutions["polluted_plan"],
                missing_step_pollutions["explicit_feedback"],
            ),
            get_formatted_prompts(
                test_prompt,
                added_step_pollutions["polluted_plan"],
                added_step_pollutions["explicit_feedback"],
            ),
            get_formatted_prompts(
                test_prompt,
                many_added_steps_pollutions["polluted_plan"],
                many_added_steps_pollutions["explicit_feedback"],
            ),
        ]
        
        general_feeback_results = prompt_model_and_validate_response(prompts=general_feedback_prompts, expected_plan=expected_plan)
        assisted_feeback_results = prompt_model_and_validate_response(prompts=assisted_feedback_prompts, expected_plan=expected_plan)
        explicit_feeback_results = prompt_model_and_validate_response(prompts=explicit_feedback_prompts, expected_plan=expected_plan)

        total_cases_run += len(general_feeback_results) + len(assisted_feeback_results) + len(explicit_feeback_results)

        general_critique_passes += general_feeback_results.count(True)
        assisted_critique_passes += assisted_feeback_results.count(True)
        explicit_critique_passes += explicit_feeback_results.count(True)

        ordering_pollution_results = [general_feeback_results[0], assisted_feeback_results[0], explicit_feeback_results[0]]

        missing_step_pollution_results = [general_feeback_results[1], assisted_feeback_results[1], explicit_feeback_results[1]]

        added_step_pollution_results = [general_feeback_results[2], assisted_feeback_results[2], explicit_feeback_results[2]]

        many_added_steps_pollution_results = [general_feeback_results[3], assisted_feeback_results[3], explicit_feeback_results[3]]

        ordering_pollutions_corrections += ordering_pollution_results.count(True)
        missing_step_pollutions_corrections += missing_step_pollution_results.count(True)
        added_step_pollutions_corrections += added_step_pollution_results.count(True)
        many_added_steps_pollutions_corrections += many_added_steps_pollution_results.count(True)

print(f"-------------RESULTS for Critiquing with model: {model_id}---------------")
print("General Feedback Passes", general_critique_passes)
print("Assisted Feedback Passes", assisted_critique_passes)
print("Explicit Feedback Passes", explicit_critique_passes)

print("Ordering Passes", ordering_pollutions_corrections)
print("Missing_step Passes", missing_step_pollutions_corrections)
print("Added_step Passes", added_step_pollutions_corrections)
print("Many_added_steps Passes", many_added_steps_pollutions_corrections)

results = {
    "testcases_run": total_cases_run,
    "general_critique_passes": general_critique_passes,
    "assisted_critique_passes": assisted_critique_passes, 
    "explicit_critique_passes": explicit_critique_passes, 
    "ordering": {
        "number_of_cases": total_cases_run/4,
        "ordering_pollutions_corrections": ordering_pollutions_corrections
    },
    "missing_step": {
        "number_of_cases": total_cases_run/4,
        "missing_step_pollutions_corrections": missing_step_pollutions_corrections
    },
    "added_step": {
        "number_of_cases": total_cases_run/4,
        "added_step_pollutions_corrections": added_step_pollutions_corrections
    },
    "many_added_steps": {
        "number_of_cases": total_cases_run/4,
        "many_added_steps_pollutions_corrections": many_added_steps_pollutions_corrections
    }
}

with open(os.path.join(DIRECTORY, 'critique_prompting_results_rerun.json'), 'w') as fp:
    json.dump(results, fp, indent=4)
