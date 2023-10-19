# PromptRunner is a cli that allows you to run prompt for testing purposes.
# It accepts the following arguments:
# -p --prompt: the folder of the prompt to run
# -t --task: the task to run for the given prompt, task specific files must be in the prompt directory
# -o --output: the output file where to write the response
#
# Folder structure:
# {prompt_folder}/
#   - openai.json # contains the openai client configuration
#   - persona.md # contains the persona prompt
#   - task_template.md # contains the task template prompt
#   - {task}/ # folder of a task
#     - facts.json (optional) # array of fact items, contains the facts specific to this task
#     - facts_filter.json (optional) # array of fact tag ids to be filtered
#     - task_parameter_1.md (optional) # contains the task parameters  to be populated in the template
#     ...
#     - task_paramteer_n.md (optional) # n-th task parameter

import argparse
import json
import os
import re
import sys
from importlib import import_module
import time

from penpen import (
    OpenAIClient,
    PromptBuilder,
    GPTModel,
    OpenAICallKwargs,
    FunctionHandler,
)


def __openai_client_from_config(config, prompt_path):
    raw_model = config.get("model", "")
    gpt_model = GPTModel.from_string(raw_model)
    config["model"] = gpt_model

    # check if "functions.py" exists at prompt_path and import it
    functions_file = os.path.join(prompt_path, "functions.py")
    if os.path.isfile(functions_file):
        sys.path.append(prompt_path)  # Add directory to sys.path
        functions_module = import_module("functions")
        functions = functions_module.function_wrappers
        max_consecutive_function_calls = functions_module.max_consecutive_function_calls
        function_call = functions_module.function_call
        handler = FunctionHandler(
            functions=functions,
        )
        config["functions"] = handler.get_openai_json_schema()
        config["function_call"] = function_call
        config["function_callback"] = handler.function_handler
        config["max_consecutive_function_calls"] = max_consecutive_function_calls

        sys.path.remove(prompt_path)  # Optionally, remove directory from sys.path

    openai_call_kwargs = OpenAICallKwargs(**config)

    return OpenAIClient(openai_call_kwargs=openai_call_kwargs)


def __extract_task_parameters(template: str) -> list:
    return re.findall(r"\{(.*?)\}", template)


def __write_result_at_path(result, filename, path):


    def to_dict(s):
        if isinstance(s,dict):
            return s
        try:
            return json.loads(s)
        except ValueError:
            return None
        


    #check if path dir exists, if not create it
    if not os.path.isdir(path):
        os.mkdir(path)

    # if result is a dictionary, save it at path as result.json
    # otherwise save it at path as result.md

    result_dict = to_dict(result)
    if result_dict:
        with open(os.path.join(path, f"{filename}.json"), "w") as f:
            f.write(json.dumps(result_dict, indent=4))
    else:
        with open(os.path.join(path, f"{filename}.md"), "w", encoding='utf-8') as f:
            f.write(str(result))


def __run_prompt(prompt_path: str, task: str, data_to_append: str = None):
    # check if prompt folder exists
    if not os.path.isdir(prompt_path):
        raise Exception(f"Prompt folder {prompt_path} does not exist")

    # check if task folder exists
    task_folder = os.path.join(prompt_path, task)
    if not os.path.isdir(task_folder):
        raise Exception(f"Task folder {task_folder} does not exist")

    # check mandatory files exist
    openai_config_file = os.path.join(prompt_path, "openai.json")
    if not os.path.isfile(openai_config_file):
        raise Exception(
            f"OpenAI configuration file {openai_config_file} does not exist"
        )

    persona_file = os.path.join(prompt_path, "persona.md")
    if not os.path.isfile(persona_file):
        raise Exception(f"Persona file {persona_file} does not exist")

    task_template_file = os.path.join(prompt_path, "task_template.md")
    if not os.path.isfile(task_template_file):
        raise Exception(f"Task template file {task_template_file} does not exist")

    # load persona
    with open(persona_file, "r") as f:
        persona = f.read()

    # load task specific files
    facts_file = os.path.join(task_folder, "facts.json")
    if os.path.isfile(facts_file):
        with open(facts_file, "r") as f:
            facts = json.load(f)
    else:
        facts = []

    facts_filter_file = os.path.join(task_folder, "facts_filter.json")
    if os.path.isfile(facts_filter_file):
        with open(facts_filter_file, "r") as f:
            facts_filter = json.load(f)
    else:
        facts_filter = []

    # load task template
    with open(task_template_file, "r") as f:
        task_template = f.read()

    # load task parameters:
    param_keys = __extract_task_parameters(task_template)

    if data_to_append:
        task_template += "\n\n" + data_to_append

    # load param values from files param_key.md for each param_key in param_keys
    task_parameters = {}
    for param_key in param_keys:
        param_file = os.path.join(task_folder, f"{param_key}.md")
        if os.path.isfile(param_file):
            with open(param_file, "r") as f:
                task_parameters[param_key] = f.read()
        else:
            raise Exception(f"Task parameter file {param_file} does not exist")

    # build prompt
    prompt = PromptBuilder(
        facts=facts,
        fact_tag_filter=facts_filter,
        persona=persona,
        task_parameters=task_parameters,
        task_template=task_template,
    )

    # load openai config and init OpenAIClient
    with open(openai_config_file, "r") as f:
        openai_config = json.load(f)
        client = __openai_client_from_config(openai_config, prompt_path)

    # get response
    result = ""
    openai_response = client.get_openai_response(prompt.getOpenAIPrompt())
    is_streaming = openai_config.get("stream", False)

    if is_streaming:
        for chunk in openai_response:
            print(chunk, end="", flush=True)
            result += chunk
    else:
        result = openai_response

    expenses = client.get_expenses()
    return result, expenses

def run_command(args):
    prompt_path = args.prompt
    task = args.task
    task_folder = os.path.join(prompt_path, task)
    result, expenses = __run_prompt(prompt_path, task)

    print("\n\n---\nTask Execution Expenses\n---\n\n")
    for expense in expenses:
        print(expense)

    # write result
    if args.output_dir:
        output_folder = args.output_dir
    else:
        output_folder = os.path.join(task_folder, "output")
    
    __write_result_at_path(result, "result", output_folder)
    
def chain_command(args):
    tasks = args.tasks
    
    if args.output_dir:
        output_dir = args.output_dir
    else:
        output_dir = os.path.join(os.getcwd(), f"chain_output_{int(time.time())}")
        

    result = None
    for task in tasks:
        prompt_path, task_name = task.split(",")
        prompt_name = os.path.basename(prompt_path)
        print(f"\nRunning task {task_name} for prompt {prompt_name}\n----\n")
        result, expenses = __run_prompt(prompt_path, task_name, result)

        print("\n\n---\nTask Execution Expenses\n---\n\n")
        for expense in expenses:
            print(expense)

        # store result as {prompt_name}_{task_name}.json in output_dir
        __write_result_at_path(result, f"{prompt_name}_{task_name}", output_dir)

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(
        title="commands",
        description="valid commands",
        help="specify one of the following commands",
    )

    run_parser = subparsers.add_parser(
        "run", help="run a prompt from a specified folder"
    )
    run_parser.add_argument(
        "-p",
        "--prompt",
        help=f"the path to the prompt to run",
        required=True,
    )
    run_parser.add_argument(
        "-t",
        "--task",
        help=f"the name of the task to execute for this prompt",
        required=True,
    )
    run_parser.add_argument(
        "-o",
        "--output-dir",
        help="optionally specify an output directory, if not specified the output will be stored in the output folder of the specified task",
        default=None,
    )
    run_parser.set_defaults(func=run_command)

    chain_parser = subparsers.add_parser(
        "chain", help="chain multiple prompts and tasks"
    )
    chain_parser.add_argument(
        "tasks",
        nargs='+',
        help="specify tasks in the format {prompt_path},{task_name}",
    )
    chain_parser.add_argument(
        "-o",
        "--output-dir",
        help="specify an output directory",
        required=False,
    )
    chain_parser.set_defaults(func=chain_command)

    args = parser.parse_args()
    if vars(args) == {}:
        parser.print_help()
        exit(0)

    args.func(args)


if __name__ == "__main__":
    main()
