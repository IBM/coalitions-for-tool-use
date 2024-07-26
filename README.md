# coalitions-for-tool-use

## Introduction

This repository stores the data, assessment scripts and simplified code used for assessing if coalitions of pretrained Large Language Models (LLMs) can work together and enhance the performance of tool using, LLM powered, agents. 

This research was performed by IBM Research UK and investigates if coalitions of open-sourced, pretrained (non-fine-tuned) Large Language Models, can work together to assist in complex workflows through agentic augmentation with external tools. 

## Overview

The research focused on assessing if a coalition of models: 
1. Offered comparable performance to single fine-tuned (for tool use) models.
1. Outperformed single open-source, pretrained models in the domain of tool use.
1. Offered any cost savings by relying on smaller models for specific tasks. 

The hypothesis behind this research was asking if:
"Different LLMs exhibit different traits, enabling them to be more accurate at specific tasks".

The motivation behind this research was to challenge the status quo of "bigger models are better" and also considering alternative means to fine-tuning for LLM applications. 

The assessment of this coalition was performed using the ToolAlpaca [test data set](https://github.com/tangqiaoyu/ToolAlpaca/blob/main/data/eval_real.json). This dataset exhibited the following qualities:
- 114 test cases requiring 11 different services
- Requiring an average of 1.25 steps (requiring different APIs/tool from the service), offering a non-trivial challenge in planning for tool use
- Each service was well-documented and came with an OpenAPI documenting the different APIs and parameters in a standadised way. 
- An accompanying dataset was used by the ToolAlpaca team to fine-tune the [Vicuna](https://lmsys.org/blog/2023-03-30-vicuna/) models, giving way to a direct comparison of fine-tuned models for tool use versus the coalition of non-fine-tuned models approach.

This repo contains:
This repo contains:
1. Assessment of the coalition against the finetuned ToolAlpaca 7B and 13B models. See [assessing-fine-tuned-models](./assessing-fine-tuned-models/).
1. Assessment of the coalition against single, un-fine-tuned models. See [assessing-single-models](./assessing-single-models/).
1. Assessment of which LLMs are the best at critiquing for improving plans. See [assessing-critiquing](./assessing-critiquing/).
1. Assessment of which LLMs are the best at tool response filtering. See [assessing-jsonrag](./assessing-jsonrag/).

For each assessment, the collected datasets and evaluation scripts are provided. 

A simplified version of the coalition system, broken up into different scripts is shared to demonstrate the inner workings of the coalition system and to demonstrate how the datasets were collected. See [simplified-coalition](./simplifed-coalition/).

## Reproducing the results
To run the accompanying evaluation scripts and the example prompting scripts we require Python 3.10. Follow the steps below to setup the local environment and then proceed to the subdirectory READMEs to run the relevant scripts. 

1. Setup a local virtual environment:
    ```
    python3.10 -m venv .venv
    ```
2. Start the venv
    ```
    source .venv/bin/activate
    ```
3. Install required dependencies
    ```
    pip install -r requirements.txt
    ```
4. Proceed to subdirectory READMEs to run the relevant scripts.

For any queries or feedback please email: prattyush.mangal@ibm.com

## Contributors

This package is written and maintained by Prattyush Mangal at IBM Research as part of the AI-Enriched Simulation team. Please contact Prattyush Mangal (<prattyush.mangal@ibm.com>) or Edward Pyzer-Knapp (<EPyzerK3@uk.ibm.com>) for questions about how to use and/or contribute.

## License

This repository is an open-source repository licensed under the MIT License. Check the details in the [`LICENSE`](./LICENSE) file.

## Authors

- Author: Prattyush Mangal <prattyush.mangal@ibm.com>

[issues]: https://github.com/IBM/coalitions-for-tool-use/issues/new
