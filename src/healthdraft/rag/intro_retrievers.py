from langchain_core.output_parsers import StrOutputParser

from src.healthdraft.rag.prompt_setup import (
    fetch_system_prompt,
    build_details_string
)

from src.healthdraft.rag.config import prompt

# Specific Agents


# Title retriever
def title_retriever(llm, title, context_objectives, population, methods):
    system = fetch_system_prompt(key="title_prompt", title=title)
    details = build_details_string(
        context_objectives=context_objectives, population=population, methods=methods
    )
    title_chain = prompt | llm | StrOutputParser()
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

    abstract_background_chain = prompt | llm | StrOutputParser()
    return abstract_background_chain.invoke({"system": system, "details": details})


# Abstract Purpose/Hypothesis retriever
def abstract_purpose_hypothesis_retriever(
    llm, title, context_objectives, population, methods
):
    system = fetch_system_prompt(key="abstract_purpose_hypothesis_prompt", title=title)
    details = build_details_string(
        context_objectives=context_objectives, population=population, methods=methods
    )
    abstract_purpose_hypothesis_chain = (
        prompt | llm | StrOutputParser()
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
    abstract_methods_chain = prompt | llm | StrOutputParser()
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
    abstract_results_chain = prompt | llm | StrOutputParser()
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
    abstract_conclusion_chain = prompt | llm | StrOutputParser()
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
    introduction_chain = prompt | llm | StrOutputParser()
    return introduction_chain.invoke({"system": system, "details": details})
