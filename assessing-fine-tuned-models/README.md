# coalitions-for-tool-use - Assessing ToolAlpaca

This research was performed by IBM Research UK and investigates if coalitions of open-sourced, pretrained (non-fine-tuned) Large Language Models, can work together to assist in complex workflows through agentic augmentation with external tools. 

In this directory we share our assessment strategy for examining a coalition of non-fine-tuned models can offer comparable performance to single fine-tuned (for tool use) models.

For assessing a systems ability to operate in the tool use domain it has to excel in the following sub-tasks:
1. (Planning) Given an intent/prompt, plan the tools to use (LLM driven)
1. (Slot filling/Execution) Slot fill the parameters for the tools to be used (LLM driven)
1. (Slot filling/Execution) Execute the tool with the inferred parameters (System/programmatically driven)
1. (Response Forming) Formulate a meaningful response to the initial query, based on the responses of the executed tools (LLM driven)

The assessment of the overall systems (coalition and fine-tuned) tasks 1,2 and 4 are assessed as they represent the tasks which are allocated to LLMs. 

The distinction between a coalition versus the fine-tuned approach is that in the coalitions, tasks 1,2 and 4 can each by allocated to different models whereas the fine-tuned approaches relies on the same custom tuned models for all of the tasks. 

The ability to decompose and assign these sub tasks to different models, permits a more seperable approach and enables use of additional modules. As such our coalition utilises an additional module named JSON RAG which is used to filter large JSON responses from API executions. It is utilised both in the Executor and the Response Former.

## Experimental Setup
Dataset Used:
- ToolAlpaca Test data set - [link](https://github.com/tangqiaoyu/ToolAlpaca/blob/main/data/eval_real.json).

The fine-tuned models used:
- ToolAlpaca-7B
- ToolAlpaca-13B

The coalition used:
- Planner: `mistralai/mistral-7b-instruct-v0-2`
- Slot Filler/Executor: `mistralai/mixtral-8x7b-instruct-v0-1`
- JSON RAG: `google/flan-ul2`
- Response Former: `mistralai/mixtral-8x7b-instruct-v0-1`

## Strategy:

As described previously, the planning, slot filling and response formulation sub-tasks all need to be assessed to evaluate the performance of the coalition approach against the fine-tuned approach used by the ToolAlpaca 7B and 13B models.

### Planner Evaluation

The generated plan is considered as a correct plan or as passing the planner evaluation if either of the following criteria are met:

- Did the LLM generated plan match the expected plan exactly? Or 
- Did the LLM generated plan contain the expected plan as the last steps in the generated plan?

This second criteria to account for a desired behaviour:
- Agentic systems should not assume knowledge during processing. They should use additional preliminary APIs when required to form an understanding of the tools and data instead of using knowledge baked into any specific model by the pre-training.

For example: 

\quad Example Task: Convert \$100 dollars to pounds. 

\quad Expected Plan: Use \textit{ConvertAmount} API

\quad Generated Plan: Use \textit{GetLatestExchangeRates} API, Use \textit{ConvertAmount} API.\\

This plan is acceptable as it used a preliminary step in the plan but ultimately invoked the required and expected APIs as the final steps in the plan.

### Slot Filling Evaluation

The generated tool parameters are considered as a correct tool parameters and hence considered as passing the slot filling evaluation if the following criteria is met:

- Did the generated tool parameters match the expected tool parameters?

This can be thought of as evaluating whether the expected tool and tool inputs were found somewhere in the execution performed by the system, ignoring the order in which the tools were executed. 

Note this can be skewed by incorrect plans being executed by the system but this evaluation was used to get an approximate measure of a model's performance when used in the executor component. For an absolute evaluation the `Overall Procedural Accuracy` measurement should be considered. 

### Overall Procedural Accuracy

This measurement combines the Planner and Slot Filling evaluations to get a metric on the overall accuracy of the system. Specifically this evaluates how a system performs with respect to:

- Correctly generating the right plans (passing the planner evaluation) and
- Correctly generating the right tool parameters to use (passing the slot filler evaluation).

This is equivalent to a validating the overall processing of a prompt from selecting the relevant APIs, and invoking them in the right order, with the right parameters. 

Due to cases where tool parameters can only be inferred correctly if data from executing previous tool executions is utilised, this evaluation requires the evaluated systems to actually trigger the tools in its testing.


### Response Former Evaluation

This evaluation characterise the effectiveness of the final response provided by the agentic systems after processing an input prompt/query. 

The evaluation compares the final response from the systems against human crafted stubbed responses representing contents expected to be present in the final response. To perform this, we measure the similarity of the final response to the defined stub by calculating and reporting semantic cosine similarity and RougeL metrics. 

The cosine similarity is performed by using the `all-MiniLM-L6-v2` model to retrieve embeddings for the stubs and actual responses. Similarly, the RougeL Precision, Recall and fMearure metrics are measured and reported. 

This evaluation approach differs from using approaches such as LLMs-as-a-Judge. We believe that the LLM-as-a-Judge evaluation strategy lacks reproducibility and can be difficult to trust. 

Note this evaluation should only be considered in partnership with the evaluation of the overall system and can only provide an relative measure of the effectiveness of a response compared to response candidates generated by other models.

## Running the Evaluations

In this directory the data collected from locally running the ToolAlpaca system with the ToolAlpaca fine-tuned models and the pretrained Vicuna models is provided. 

Although the summarised results are provided already in the `data` directory with file name: `<test_case>-results.json`, these files can be regenerated by using the `form_results.py` script to recreate the evaluation and the metrics collected. 

### Reproducing the results:

1. Follow the guide in the root directory to setup your local environment
1. Change into this directory (if in the root directory): `cd assessing-fine-tuned-models`
1. Choose the test case to run:
    ```python
    # TEST_CASE="toolalpaca-13B"
    # TEST_CASE="toolalpaca-7B"
    # TEST_CASE="toolalpaca-vicuna-7b"
    # TEST_CASE="toolalpaca-vicuna-13b"
    ```
1. Run the evaluation script, for example:
    ```bash
    TEST_CASE="toolalpaca-13b" python form_results.py
    ```
1. Access the respective test case directory under the `data` directory. Eg `cd data/toolalpaca-13b`
1. Examine the generated results file: `final_summary_extra.json`. 

For any queries or feedback please email: prattyush.mangal@ibm.com
