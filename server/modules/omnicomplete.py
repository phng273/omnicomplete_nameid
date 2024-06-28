import json
import os
from dotenv import load_dotenv

load_dotenv()  # Tải các biến môi trường từ tệp .env

PROMPT_ROOT_DIR = os.getenv("PROMPT_ROOT_DIR")
if not PROMPT_ROOT_DIR:
    raise ValueError("Environment variable PROMPT_ROOT_DIR is not set.")


def build_omni_complete_prompt(input_value):
    try:
        with open(os.path.join(PROMPT_ROOT_DIR, "prompt.txt"), "r") as prompt_file:
            prompt = prompt_file.read()

        with open(os.path.join(PROMPT_ROOT_DIR, "knowledge_bases/previous_completions.json"), "r") as pc_file:
            previous_completions = pc_file.read()

        with open(os.path.join(PROMPT_ROOT_DIR, "knowledge_bases/domain_knowledge.csv"), "r") as dk_file:
            domain_knowledge = dk_file.read()

        prompt = prompt.replace("{{previous_completions}}", previous_completions)
        prompt = prompt.replace("{{domain_knowledge}}", domain_knowledge)
        prompt = prompt.replace("{{input_value}}", input_value)

        return prompt

    except FileNotFoundError as e:
        print(f"Error: {e}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise


def increment_or_create_previous_completions(input_value, completion):
    previous_completions_file = os.path.join(PROMPT_ROOT_DIR, "knowledge_bases/previous_completions.json")

    try:
        with open(previous_completions_file, "r") as pc_file:
            previous_completions = json.load(pc_file)
        if input_value is int or completion is int:
            matching_icase = [
                item for item in previous_completions
                if item["input"].lower() == input_value.lower()
                and completion == item["completions"]
            ]

            if matching_icase:
                matching_icase[0]["hits"] += 1
            else:
                new_completion = {
                    "input": input_value, "completions": completion, "hits": 1
                    }
                previous_completions.append(new_completion)

            completions_sorted_by_hits = sorted(previous_completions, key=lambda x: x["hits"], reverse=True)

            with open(previous_completions_file, "w") as pc_file:
                json.dump(completions_sorted_by_hits, pc_file, indent=4)

    except FileNotFoundError as e:
        print(f"Error: {e}")
        raise
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise
