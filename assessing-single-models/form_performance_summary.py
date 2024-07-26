#
# Copyright IBM Corp. 2024
# SPDX-License-Identifier: MIT
#
import json
import os
from copy import deepcopy
from rouge_score import rouge_scorer
from rouge_score.scoring import Score
from sentence_transformers import SentenceTransformer, util

# Specify directory containing results:
DIRECTORY=file_path = os.path.dirname(os.path.realpath(__file__))
RAW_DATA_FILE_NAME="corrected_result.json"
TEST_DATA="data"

# Different coalition configurations

# TEST_CASE="codellama34-all"
# TEST_CASE="llama70b-all"
# TEST_CASE="mistral_all"
# TEST_CASE="mixtral-all"
# TEST_CASE="flan_all"

# TEST_CASE="mistral_codellama_flan_codellama_mistral"
# TEST_CASE="mistral_llama70_flan_codellama_mistral"
# TEST_CASE="mistral_mistral_flan_codellama_mistral"
# TEST_CASE="mistral_mixtral_flan_codellama_mistral"

# TEST_CASE="mistral_mixtral_flan_llama70b_mistral"
# TEST_CASE="mistral_mixtral_flan_mistral_mistral"
# TEST_CASE="mistral_mixtral_flan_mixtral_mistral"
# TEST_CASE="llama2_mixtral_flan_mixtral_mistral"

TEST_CASE=os.getenv("TEST_CASE", "flan_all")

QUALIFIED_TEST_DATA_PATH = os.path.join(DIRECTORY, TEST_DATA, TEST_CASE, RAW_DATA_FILE_NAME)

MODEL = SentenceTransformer('all-MiniLM-L6-v2')
scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL', 'rougeLsum'])

with open(QUALIFIED_TEST_DATA_PATH, "r") as read_file:
    raw_results_data = json.load(read_file)

results = []
additional_planner_steps_tracker = []
additional_planner_steps_taken = 0
error_in_parsing_count = 0
planner_failure_count = 0
slot_filling_failure_count = 0
planner_and_slot_filling_pass_count = 0
similarity_score_store = {
    "cosine_similarity_scores": [],
    "rougeL_precision_scores": [],
    "rougeL_recall_scores": [],
    "rougeL_fmeasure_scores": []
}

def planner_eval_passed(expected_plan, actual_plan):
    if actual_plan == expected_plan:
        return True
    else:
        # # check if the expected plan is last part of the actual plan
        # print("------------------------------------------------")
        # print("ACTUAL PLAN", actual_plan)
        # print("EXPECTED PLAN", expected_plan)
        # print("PASSED PLANNER EVAL", actual_plan[-len(expected_plan):] == expected_plan)
        # print("------------------------------------------------")
        # print("")
        return actual_plan[-len(expected_plan):] == expected_plan
    

def slot_filling_eval_passed(service_name, expected_execution_and_inputs, actual_execution_and_inputs: list, slot_filling_eval_details: list[str]):
    # for every expected action and action input block, block was found in the actual action and action inputs
    for expected_step_and_inputs in expected_execution_and_inputs:
        expected_step = expected_step_and_inputs["step_name"]
        expected_step_inputs = expected_step_and_inputs["step_inputs"]
        formatted_expected_inputs: dict = expected_step_inputs
        formatted_expected_inputs.pop("appid", None)
        formatted_expected_inputs.pop("api_key", None)
        formatted_expected_inputs.pop("access_key", None)

        # process dataset to match the specification from the OpenAPI
        if service_name == "currencybeacon":
            if "symbols" in formatted_expected_inputs.keys():
                if isinstance(formatted_expected_inputs["symbols"], list):
                    formatted_expected_inputs["symbols"] = ",".join(formatted_expected_inputs["symbols"])
                    slot_filling_eval_details.append("CurrencyBeacon: symbols expected property converted to string")
            
            if "amount" in formatted_expected_inputs.keys():
                formatted_expected_inputs["amount"] = str(formatted_expected_inputs["amount"])
                slot_filling_eval_details.append("CurrencyBeacon: amount expected property converted to string")            


        passed = False

        for index, actual_step_and_inputs in enumerate(actual_execution_and_inputs):
            actual_step = actual_step_and_inputs["step_name"]
            actual_step_inputs = actual_step_and_inputs["step_inputs"]
            formatted_actual_inputs: dict = actual_step_inputs
            formatted_actual_inputs.pop("appid", None)
            formatted_actual_inputs.pop("api_key", None)
            formatted_actual_inputs.pop("access_key", None)

            if service_name == "wolframalpha":
                if "i" in formatted_expected_inputs.keys() and "i" in formatted_actual_inputs.keys():
                    passed_semantic_check = wolfram_query_semantic_match(formatted_expected_inputs["i"], formatted_actual_inputs["i"], slot_filling_eval_details=slot_filling_eval_details)
                    formatted_expected_inputs.pop("i", None)
                    formatted_actual_inputs.pop("i", None)
                    # For wolfram, timeout is an optional param and defaults to 5, 
                    # If Actual inputs contain this default 
                    # but expected inputs do not, we do not penalise that as a failure
                    formatted_expected_inputs.pop("timeout", None)
                    formatted_actual_inputs.pop("timeout", None)
                    if passed_semantic_check and expected_step == actual_step and formatted_expected_inputs == formatted_actual_inputs:
                        actual_execution_and_inputs[index] = {"step_name":"already_found", "step_inputs": {}}
                        passed = True
                        break
                else:
                    passed = False
            else:
                if expected_step == actual_step and formatted_expected_inputs == formatted_actual_inputs:
                    actual_execution_and_inputs[index] = {"step_name":"already_found", "step_inputs": {}}
                    passed = True
                    break
                else: 
                    passed = False

        if passed == False:
            return False
    
    return True

def wolfram_query_semantic_match(expected_query: str, actual_query: str, slot_filling_eval_details: list[str]):
    # if we find query in the wolfram service tests, then perform
    # semantic text sim on the expected and actual query
    unencoded_actual_query = actual_query.replace("%20", " ").replace("+", " ")
    query_cos_similarity_measure = util.cos_sim(MODEL.encode(expected_query), MODEL.encode(unencoded_actual_query)).item()

    if query_cos_similarity_measure > 0.87:
        slot_filling_eval_details.append("WolframAlpha: Query passed semantic similarity threshold of 0.87 with value: " + query_cos_similarity_measure.__str__() +". Strings compared: " + expected_query + " AND " + unencoded_actual_query)
        return True
    else: 
        slot_filling_eval_details.append("WolframAlpha: Query failed semantic similarity threshold of 0.87 with value: " + query_cos_similarity_measure.__str__())
        return False

def response_former_eval(similarity_score_store: dict, expected_response_stub: str, actual_response_stub: str):
    # Cosine similarity is used to determine some "closeness" in a semantic sense, between the expected and actual responses using
    # vector embeddings made available through OpenSource embeddings. The `.item()` is used to convert Tensor to a single Number
    cos_similarity_measure = util.cos_sim(MODEL.encode(actual_response_stub), MODEL.encode(expected_response_stub)).item()
    # Rouge scores pay attention to subsets of words being featured in the test string
    scores_rouge: Score = scorer.score(actual_response_stub, expected_response_stub)["rougeL"] # this is a Score object and we are using LCS (Longest Common Substring)

    # A Score Class contains a list of lists, we just flatten those into one array containing all similarity metrics.
    # In the future we should come back to this, to either weight or pay more attention to specific metrics
    scores = list(scores_rouge._asdict().values())

    scores.append(cos_similarity_measure)


    similarity_score_store["cosine_similarity_scores"].append(cos_similarity_measure)
    similarity_score_store["rougeL_precision_scores"].append(scores_rouge.precision)
    similarity_score_store["rougeL_recall_scores"].append(scores_rouge.recall)
    similarity_score_store["rougeL_fmeasure_scores"].append(scores_rouge.fmeasure)

# Main method , read data from file and invoke the required evaluation
for service_details in raw_results_data:
    service_results = {}
    service_results["service_name"] = service_details["service"]
    service_tests = []


    for ind, prompt_result_detail in enumerate(service_details["results"]):
        # Find the expected response for this service from the response stub file (https://stackoverflow.com/questions/7079241/python-get-a-dict-from-a-list-based-on-something-inside-the-dict)
        
        test_details = {}
        test_details["test_run_uuid"] = prompt_result_detail["test_run_uuid"]
        test_details["input_prompt"] = prompt_result_detail["input_prompt"]
        
        test_details["expected_plan"] = prompt_result_detail["expected_planner_output"] 
        
        test_details["actual_plan"] = prompt_result_detail["recieved_planner_output"]
        
        test_details["expected_execution_and_inputs"] = prompt_result_detail["expected_executor_step_and_parameters"] 
        
        test_details["actual_execution_and_inputs"] = prompt_result_detail["recieved_executor_step_and_parameters"]

        expected_response_stub_for_test_case = prompt_result_detail["expected_magpie_output"]

        test_details["expected_output_stub"] = expected_response_stub_for_test_case

        print("Checking Expected Response:", expected_response_stub_for_test_case)

        if len(prompt_result_detail["execution_errors"]) > 0:
            print("There was a parsing error", prompt_result_detail["execution_errors"])
            test_details["errored"] = True
            test_details["error_type"] = "parsing"
            test_details["error_message"] = prompt_result_detail["execution_errors"]
            error_in_parsing_count += 1
            # test_details["planner_passed"] = False
            # test_details["slot_filling_passed"] = False
        else:
            formatted_plan_and_inputs = []
            test_details["actual_output"] = prompt_result_detail["recieved_magpie_output"]
            # print("Checking Test Details:", test_details)

            planner_passed = planner_eval_passed(deepcopy(test_details["expected_plan"]), deepcopy(test_details["actual_plan"]))

            if planner_passed:
                test_details["planner_passed"] = True
                additional_planner_steps = len(test_details["actual_plan"]) - len(test_details["expected_plan"])
                test_details["additional_planner_steps"] = additional_planner_steps
                additional_planner_steps_tracker.append(additional_planner_steps)
                additional_planner_steps_taken += additional_planner_steps
            else:
                test_details["planner_passed"] = False
                test_details["error_type"] = "planner"
                planner_failure_count += 1

            # print("Prompt", test_details["input_prompt"])

            test_details["slot_filling_evaluation_details"] = []

            slot_filling_passed = slot_filling_eval_passed(service_name=service_details["service"], expected_execution_and_inputs=deepcopy(test_details["expected_execution_and_inputs"]), actual_execution_and_inputs=deepcopy(test_details["actual_execution_and_inputs"]), slot_filling_eval_details=test_details["slot_filling_evaluation_details"])

            if slot_filling_passed:
                test_details["slot_filling_passed"] = True
            else:
                test_details["slot_filling_passed"] = False
                test_details["error_type"] = "slot_filling"
                slot_filling_failure_count += 1
            
            test_details["human_eval"] = ""

            if planner_passed and slot_filling_passed:
                test_details["planner_and_slot_filling_passed"] = True
                planner_and_slot_filling_pass_count += 1
            else:
                test_details["planner_and_slot_filling_passed"] = False

            response_former_eval(similarity_score_store=similarity_score_store, actual_response_stub=test_details["actual_output"], expected_response_stub=expected_response_stub_for_test_case)


        service_tests.append(test_details)
            
    service_results["tests"] = service_tests
    results.append(service_results)

final_eval_document = {
    "average_cosine_similarity_of_final_responses": sum(similarity_score_store["cosine_similarity_scores"])/len(similarity_score_store["cosine_similarity_scores"]),
    "average_rougeL_precision":sum(similarity_score_store["rougeL_precision_scores"])/len(similarity_score_store["rougeL_precision_scores"]),
    "average_rougeL_recall":sum(similarity_score_store["rougeL_recall_scores"])/len(similarity_score_store["rougeL_recall_scores"]),
    "average_rougeL_fmeasure":sum(similarity_score_store["rougeL_fmeasure_scores"])/len(similarity_score_store["rougeL_fmeasure_scores"]),
    "average_additional_planner_steps": sum(additional_planner_steps_tracker)/len(additional_planner_steps_tracker),
    "additional_planner_steps_taken": additional_planner_steps_taken,
    "error_in_parsing_count": error_in_parsing_count,
    "planner_failure_count": planner_failure_count,
    "slot_filling_failure_count": slot_filling_failure_count,
    "planner_and_slot_filling_pass_count": planner_and_slot_filling_pass_count,
    "results": results
}

with open(os.path.join(DIRECTORY, TEST_DATA, TEST_CASE, 'final_summary_extra_rerun.json'), 'w') as fp:
    json.dump(final_eval_document, fp, indent=4)