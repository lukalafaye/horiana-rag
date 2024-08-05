from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import OpenAI
from dotenv import load_dotenv
import os

docker = False

def title_retriever(llm, title, context_objectives, population, methods):
    system = f"""
    You are a professional medical writer. You will help the user write the title of a medical paper based off a statistical study.
    The user will provide you with the context and objectives, population analysis, and methods of a statistical study titled {title}. 
    Your task is to write a concise accurate title and subtitle for the medical paper about the study.

    Title: Use the main focus of the study to create a concise and informative title that reflects the primary outcome or comparison being studied.
    Subtitle: Provide significant details or techniques from the study's population analysis or methods in the subtitle.
    """

    details = f"""
    Context and Objectives: {context_objectives}
    Population Analysis: {population}
    Methods: {methods}
    """

    title_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("user", details),
        ]
    )

    title_chain = title_prompt | llm | StrOutputParser()

    return title_chain.invoke({"system": system, "details": details})

def abstract_background_retriever(llm, title, context_objectives, population, methods, abstracts: list[str]):
    system = f"""
    You are a professional medical writer. You will help the user write the abstract background paragraph of a medical paper based off a statistical study.
    The user will provide you with the context, objectives, population analysis, and methods of a medical study titled {title}. 
    Additionally, they will provide you with several abstracts of related medical studies.

    Your task is to write a short concise and accurate one line background paragraph for the abstract of this study. 
    The background should incorporate the context, objectives, population analysis, methods, and insights from the related studies' abstracts. 
    Ensure to include the context and previous research that led to this study.
    """

    abstracts_str = "\n\n".join(abstracts)

    details = f"""
    Context and Objectives: {context_objectives}
    Population Analysis: {population}
    Methods: {methods}
    Abstracts: {abstracts_str}
    """

    abstract_background_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system),
                ("user", details),
            ]
    )

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
    context_objectives = "This study aims to evaluate the effectiveness of New Drug X in reducing blood pressure levels in patients diagnosed with hypertension."
    population = "The study involves 500 participants aged between 30 and 65, all diagnosed with stage 1 or stage 2 hypertension. Participants were randomly assigned to either the treatment group receiving New Drug X or the control group receiving a placebo."
    methods = "A double-blind, randomized, placebo-controlled trial was conducted over 12 weeks. Blood pressure levels were measured at baseline, week 6, and week 12. Statistical analysis was performed using a mixed-effects model for repeated measures."

    title = title_retriever(llm, title, context_objectives, population, methods)
    # fetch abstracts and crag...

    abstracts = [
        "Abstract 1: Previous studies have shown that Drug A significantly reduces systolic and diastolic blood pressure in hypertensive patients. However, the long-term effects of Drug A remain unclear.",
        "Abstract 2: The impact of Drug B on blood pressure variability was assessed in a randomized controlled trial involving 300 hypertensive patients. Results indicated a notable reduction in blood pressure fluctuations over a 24-hour period.",
        "Abstract 3: A comparative study between Drug C and Drug D demonstrated that both medications effectively lower blood pressure, with Drug C showing a slightly better safety profile in elderly patients."
    ]

    abstract_background = abstract_background_retriever(llm, title, context_objectives, population, methods, abstracts)

    print(title, abstract_background)

if __name__ == "__main__":
    main()