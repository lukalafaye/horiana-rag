from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import OpenAI
from dotenv import load_dotenv
import os
import yaml


def load_prompts(yaml_file_path):
    with open(yaml_file_path, "r", encoding="utf-8") as file:
        prompts = yaml.safe_load(file)
    return prompts


# Global variables

yaml_prompts = "prompts/prompts.yaml"
prompts = load_prompts(yaml_prompts)

docker = False

# General functions


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


def create_final_prompt(system, details):
    user_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("user", details),
        ]
    )
    return user_prompt


# Specific Agents


def title_retriever(llm, title, context_objectives, population, methods):
    system = fetch_system_prompt(key="title_prompt", title=title)

    details = f"""
    Context and Objectives: {context_objectives}
    Population Analysis: {population}
    Methods: {methods}
    """

    title_prompt = create_final_prompt(system, details)
    title_chain = title_prompt | llm | StrOutputParser()

    return title_chain.invoke({"system": system, "details": details})


def abstract_background_retriever(
    llm, title, context_objectives, population, methods, abstracts: list[str]
):
    system = fetch_system_prompt(key="abstract_background_prompt", title=title)

    abstracts_str = "\n\n".join(abstracts)

    details = f"""
    Context and Objectives: {context_objectives}
    Population Analysis: {population}
    Methods: {methods}
    Abstracts: {abstracts_str}
    """

    abstract_background_prompt = create_final_prompt(system, details)
    abstract_background_chain = abstract_background_prompt | llm | StrOutputParser()

    return abstract_background_chain.invoke({"system": system, "details": details})


def main():
    openai_env = ".openai_env"
    if docker:
        openai_env = "/app/" + openai_env

    if os.path.exists(openai_env):
        load_dotenv(openai_env)
    else:
        print(openai_env + " not found.")

    api_key = os.getenv("OPENAI_API_KEY")

    if api_key is None:
        raise ValueError("OPENAI_API_KEY environment variable is not set")

    llm = OpenAI(api_key=api_key)

    title = "Effectiveness of New Drug X in Treating Hypertension"
    context_objectives = """
    This study aims to evaluate the effectiveness of New Drug X in reducing blood
    pressure levels in patients diagnosed with hypertension.
    """

    population = """The study involves 500 participants aged between 30 and 65,
    all diagnosed with stage 1 or stage 2 hypertension. Participants were randomly
    assigned to either the treatment group receiving New Drug X or the control
    group receiving a placebo.
    """

    methods = """A double-blind, randomized, placebo-controlled trial was conducted
    over 12 weeks. Blood pressure levels were measured at baseline, week 6, and week 12.
    Statistical analysis was performed using a mixed-effects model for repeated measures.
    """

    title = title_retriever(llm, title, context_objectives, population, methods)
    # fetch abstracts and crag...

    abstracts = [
        "Abstract 1: Previous studies have shown that Drug A significantly reduces systolic \
        and diastolic blood pressure in hypertensive patients. \
        However, the long-term effects of Drug A remain unclear.",
        "Abstract 2: The impact of Drug B on blood pressure variability was assessed in a \
        randomized controlled trial involving 300 hypertensive patients. \
        Results indicated a notable reduction in blood pressure fluctuations over a 24-hour period.",
        "Abstract 3: A comparative study between Drug C and Drug D demonstrated that both \
        medications effectively lower blood pressure, with Drug C showing a slightly \
        better safety profile in elderly patients.",
    ]

    abstract_background = abstract_background_retriever(
        llm, title, context_objectives, population, methods, abstracts
    )

    print(title, abstract_background)


if __name__ == "__main__":
    main()
