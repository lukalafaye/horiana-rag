from pprint import pprint

from src.healthdraft.rag.intro_retrievers import (
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

from src.healthdraft.rag.methods_retriever import (
    methods_study_design_participants_retriever,
    methods_surgical_technique_retriever,  # todo
    methods_postoperative_rehabilitation_protocol_retriever,  # todo
    methods_follow_up_data_collection_retriever,  # todo
    methods_statistical_analysis_retriever,
)

from src.healthdraft.rag.generate_data import generate_sample_data

from src.healthdraft.rag.llama import create_llama_instance

docker = False

def generate_sample_article(title, context_objectives, population, methods, abstracts_str, keyresults, keywords, ethics):
    
    llm = create_llama_instance()

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

    return article


if __name__ == "__main__":
    title, context_objectives, population, methods, abstracts_str, keyresults, keywords, ethics = generate_sample_data()
    article = generate_sample_article(title, context_objectives, population, methods, abstracts_str, keyresults, keywords, ethics)
    pprint(article)

