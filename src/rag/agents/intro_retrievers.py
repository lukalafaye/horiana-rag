from langchain_core.output_parsers import StrOutputParser

from src.rag.agents.general_functions import (
    fetch_system_prompt,
    build_details_string,
    create_final_prompt,
)

# Specific Agents


# Title retriever
def title_retriever(llm, title, context_objectives, population, methods):
    system = fetch_system_prompt(key="title_prompt", title=title)
    details = build_details_string(
        context_objectives=context_objectives, population=population, methods=methods
    )
    title_prompt = create_final_prompt(system, details)
    title_chain = title_prompt | llm | StrOutputParser()
    return title_chain.invoke({"system": system, "details": details})


# ABSTRACT #################


# Abstract Background retriever
def abstract_background_retriever(
    llm, title, context_objectives, population, methods, abstracts_str
):
    system = fetch_system_prompt(key="abstract_background_prompt", title=title)
    details = build_details_string(
        context_objectives=context_objectives,
        population=population,
        methods=methods,
        abstracts_str=abstracts_str,
    )

    print("SYSTEME: ", system)

    abstract_background_prompt = create_final_prompt(system, details)
    abstract_background_chain = abstract_background_prompt | llm | StrOutputParser()
    return abstract_background_chain.invoke({"system": system, "details": details})


# Abstract Purpose/Hypothesis retriever
def abstract_purpose_hypothesis_retriever(
    llm, title, context_objectives, population, methods
):
    system = fetch_system_prompt(key="abstract_purpose_hypothesis_prompt", title=title)
    details = build_details_string(
        context_objectives=context_objectives, population=population, methods=methods
    )
    abstract_purpose_hypothesis_prompt = create_final_prompt(system, details)
    abstract_purpose_hypothesis_chain = (
        abstract_purpose_hypothesis_prompt | llm | StrOutputParser()
    )
    return abstract_purpose_hypothesis_chain.invoke(
        {"system": system, "details": details}
    )


# Abstract Study design retriever : to do
def abstract_study_design_retriever(llm):
    return


# Abstract Methods retriever
def abstract_methods_retriever(llm, title, context_objectives, population, methods):
    system = fetch_system_prompt(key="abstract_methods_prompt", title=title)
    details = build_details_string(
        context_objectives=context_objectives, population=population, methods=methods
    )
    abstract_methods_prompt = create_final_prompt(system, details)
    abstract_methods_chain = abstract_methods_prompt | llm | StrOutputParser()
    return abstract_methods_chain.invoke({"system": system, "details": details})


# Abstract Results retriever
def abstract_results_retriever(
    llm, title, context_objectives, population, methods, keyresults
):
    system = fetch_system_prompt(key="abstract_results_prompt", title=title)
    details = build_details_string(
        context_objectives=context_objectives,
        population=population,
        methods=methods,
        keyresults=keyresults,
    )
    abstract_results_prompt = create_final_prompt(system, details)
    abstract_results_chain = abstract_results_prompt | llm | StrOutputParser()
    return abstract_results_chain.invoke({"system": system, "details": details})


# Abstract Conclusion retriever
def abstract_conclusion_retriever(
    llm, title, context_objectives, population, methods, generated_keyresults
):
    system = fetch_system_prompt(key="abstract_conclusion_prompt", title=title)
    details = build_details_string(
        context_objectives=context_objectives,
        population=population,
        methods=methods,
        keyresults=generated_keyresults,
    )
    abstract_conclusion_prompt = create_final_prompt(system, details)
    abstract_conclusion_chain = abstract_conclusion_prompt | llm | StrOutputParser()
    return abstract_conclusion_chain.invoke({"system": system, "details": details})


# Abstract Keywords retriever : to do
def abstract_keywords_retriever(llm, keywords):
    return


# INTRODUCTION #################


# Introduction retriever
def introduction_retriever(
    llm, title, context_objectives, population, methods, related_abstracts
):
    system = fetch_system_prompt(key="introduction_prompt", title=title)
    details = build_details_string(
        context_objectives=context_objectives,
        population=population,
        methods=methods,
        related_abstracts=related_abstracts,
    )
    introduction_prompt = create_final_prompt(system, details)
    introduction_chain = introduction_prompt | llm | StrOutputParser()
    return introduction_chain.invoke({"system": system, "details": details})
