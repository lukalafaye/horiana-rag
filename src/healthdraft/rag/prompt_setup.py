import yaml
from src.config import (
    get_absolute_path,
)  # will also run config.py, setting up env variables

# General functions


def load_prompts(yaml_file_path="prompts/prompts.yaml"):
    yaml_file_path = get_absolute_path(yaml_file_path)
    with open(yaml_file_path, "r", encoding="utf-8") as file:
        prompts = yaml.safe_load(file)
    return prompts


prompts = load_prompts()
docker = False


# Generate system prompt
def fetch_system_prompt(key, **kwargs):
    if key not in prompts:
        raise KeyError(f"Prompt key '{key}' not found in possible prompts list.")

    prompt_template = prompts[key]

    # Replace all placeholders with corresponding values
    try:
        system = prompt_template.format(**kwargs)
    except KeyError as e:
        raise KeyError(f"Missing key in format: {e}")

    return system


# Generate details prompt
def build_details_string(**kwargs):
    # Create a dictionary to store the key-value pairs
    details_dict = {
        "context_objectives": "Context and Objectives",
        "population": "Population Analysis",
        "methods": "Methods",
        "abstracts_str": "Abstracts",
        "keyresults": "Key results",
        "related_abstracts": "Related abstracts",
        "title": "Title",
        "ethics": "Ethical considerations",
    }

    # Initialize the details string
    details = "\n"

    # Loop through the provided keyword arguments
    for key, value in kwargs.items():
        if key in details_dict:
            details += f"{details_dict[key]}: \n{value}\n"

    # Close the string
    details += "\n"

    return details