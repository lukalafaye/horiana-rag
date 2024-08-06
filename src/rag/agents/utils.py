import os
from langchain_openai import OpenAI
from pprint import pprint

from src.rag.agents.intro_retrievers import (
    title_retriever,
    abstract_background_retriever,
    abstract_purpose_hypothesis_retriever,
    abstract_study_design_retriever,
    abstract_methods_retriever,
    abstract_results_retriever,
    abstract_conclusion_retriever,
    abstract_keywords_retriever,  # todo
    introduction_retriever,
)

from src.rag.agents.methods_retriever import (
    methods_study_design_participants_retriever,
    methods_surgical_technique_retriever,  # todo
    methods_postoperative_rehabilitation_protocol_retriever,  # todo
    methods_follow_up_data_collection_retriever,  # todo
    methods_statistical_analysis_retriever,
)

docker = False


def generate_sample_data():
    title = "Effectiveness of New Drug X in Treating Hypertension"

    context_objectives = """This study aims to evaluate the effectiveness of New Drug X in reducing blood
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

    abstracts_str = "\n\n".join(abstracts)

    keyresults = ""
    keywords = ""
    ethics = ""

    return (
        title,
        context_objectives,
        population,
        methods,
        abstracts_str,
        keyresults,
        keywords,
        ethics,
    )


def create_llm_instance():
    open_api_key = os.getenv("OPENAI_API_KEY")

    if open_api_key is None:
        raise ValueError("OPENAI_API_KEY environment variable is not set")

    llm = OpenAI(api_key=open_api_key)
    return llm


def generate_sample_article():
    (
        title,
        context_objectives,
        population,
        methods,
        abstracts_str,
        keyresults,
        keywords,
        ethics,
    ) = generate_sample_data()
    llm = create_llm_instance()

    article = {
        "title": None,
        "abstract_background": None,
        "abstract_purpose_hypothesis": None,
        "abstract_study_design": None,
        "abstract_methods": None,
        "abstract_results": None,
        "abstract_conclusion": None,
        "abstract_keywords": None,  # todo
        "introduction": None,
        "methods_study_design_participants": None,
        "methods_surgical_technique": None,  # todo
        "methods_postoperative_rehabilitation_protocol": None,  # todo
        "methods_follow_up_data_collection": None,  # todo
        "methods_statistical_analysis": None,
    }

    # Populating the article dictionary
    article["title"] = title_retriever(
        llm, title, context_objectives, population, methods
    )
    article["abstract_background"] = abstract_background_retriever(
        llm, title, context_objectives, population, methods, abstracts_str
    )
    article["abstract_purpose_hypothesis"] = abstract_purpose_hypothesis_retriever(
        llm, title, context_objectives, population, methods
    )
    article["abstract_study_design"] = abstract_study_design_retriever(llm)  # todo
    article["abstract_methods"] = abstract_methods_retriever(
        llm, title, context_objectives, population, methods
    )
    article["abstract_results"] = abstract_results_retriever(
        llm, title, context_objectives, population, methods, keyresults
    )
    generated_keyresults = article["abstract_results"]
    article["abstract_conclusion"] = abstract_conclusion_retriever(
        llm, title, context_objectives, population, methods, generated_keyresults
    )
    article["abstract_keywords"] = abstract_keywords_retriever(llm, keywords)  # todo
    related_abstracts = abstracts_str  # for now
    article["introduction"] = introduction_retriever(
        llm, title, context_objectives, population, methods, related_abstracts
    )
    article["methods_study_design_participants"] = (
        methods_study_design_participants_retriever(
            llm, title, context_objectives, population, methods, ethics
        )
    )
    article["methods_surgical_technique"] = methods_surgical_technique_retriever(
        llm
    )  # todo
    article["methods_postoperative_rehabilitation_protocol"] = (
        methods_postoperative_rehabilitation_protocol_retriever(llm)
    )  # todo
    article["methods_follow_up_data_collection"] = (
        methods_follow_up_data_collection_retriever(llm)
    )  # todo
    article["methods_statistical_analysis"] = methods_statistical_analysis_retriever(
        llm, title, context_objectives, population, methods, ethics
    )

    pprint(article)


if __name__ == "__main__":
    generate_sample_article()
