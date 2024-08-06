from langchain_core.output_parsers import StrOutputParser

from src.rag.agents.general_functions import (
    fetch_system_prompt,
    build_details_string,
    create_final_prompt,
)

# METHODS #################


# Methods Study design & Participants retriever
def methods_study_design_participants_retriever(
    llm, title, context_objectives, population, methods, ethics
):
    system = fetch_system_prompt(
        key="methods_study_design_participants_prompt", title=title
    )
    details = build_details_string(
        context_objectives=context_objectives,
        population=population,
        methods=methods,
        ethics=ethics,
    )
    methods_study_design_participants_prompt = create_final_prompt(system, details)
    methods_study_design_participants_chain = (
        methods_study_design_participants_prompt | llm | StrOutputParser()
    )
    return methods_study_design_participants_chain.invoke(
        {"system": system, "details": details}
    )


# Methods Surgical Technique retriever : to do
def methods_surgical_technique_retriever(llm):
    return


# Methods Postoperative Rehabilitation Protocol retriever : to do
def methods_postoperative_rehabilitation_protocol_retriever(llm):
    return llm


# Methods Follow-up and data Collection retriever : to do
def methods_follow_up_data_collection_retriever(llm):
    return llm


# Methods Follow-up and data Collection retriever : to do
def methods_statistical_analysis_retriever(
    llm, title, context_objectives, population, methods, ethics
):
    system = fetch_system_prompt(key="methods_statistical_analysis_prompt", title=title)
    details = build_details_string(
        context_objectives=context_objectives,
        population=population,
        methods=methods,
        ethics=ethics,
    )
    methods_statistical_study_prompt = create_final_prompt(system, details)
    methods_statistical_study_chain = (
        methods_statistical_study_prompt | llm | StrOutputParser()
    )
    return methods_statistical_study_chain.invoke(
        {"system": system, "details": details}
    )
