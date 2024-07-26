# coalitions-for-tool-use - Example of simplified coalition system

This research was performed by IBM Research UK and investigates if coalitions of open-sourced, pretrained (non-fine-tuned) Large Language Models, can work together to assist in complex workflows through agentic augmentation with external tools. 

For assessing a systems ability to operate in the tool use domain it has to excel in the following sub-tasks:
1. (Planning) Given an intent/prompt, plan the tools to use (LLM driven)
1. (Slot filling/Execution) Slot fill the parameters for the tools to be used (LLM driven)
1. (Slot filling/Execution) Execute the tool with the inferred parameters (System/programmatically driven)
1. (Response Forming) Formulate a meaningful response to the initial query, based on the responses of the executed tools (LLM driven)

In this directory we share a simplified example of the coalition system and these decomposed subtasks for intent processing. The simplified system is provided to demonstrate how the end to end system we developed operates and this example is provided to share an understanding of how the reported raw data may be reproduced. 

## Running the Example scripts

1. Follow the guide in the root directory to setup your local environment
1. Change into this directory (if in the root directory): `cd simplified-coalition`
1. Based on your access, you may need to setup connection to a watsonx.ai deployment and update the provided `run_critique_prompts.py` script to utilise the `ibm-watsonx-ai` SDK - see [here](https://ibm.github.io/watsonx-ai-python-sdk/install.html).
1. Export connection to your watsonx.ai instance. For example:
    ```bash
    export GENAI_KEY=<apikey to connect to watsonx.ai instance>
    export GENAI_API=<address of watsonx.ai instance>
    ```
1. Running the planning script:
    ```bash
    python planner.py
    ```
1. Running the slot-filling script:
    ```bash
    python slot_filler.py
    ```
1. Running the response former script:
    ```bash
    python response_former.py
    ```

For any queries or feedback please email: prattyush.mangal@ibm.com
