import pickle
import json
import os
from src.healthdraft.extractors.utils import process_files  # Updated import path
from src.healthdraft.extractors.abstracts_extractor import fetch_from_keywords

from src.healthdraft.utils import validate_params

docker = False


@validate_params
def preprocess(pdf_path, docx_path, synopsis_path, document_output_path):
    """
    Extracts document info using pdf and docx in a dictionnary
    Saves dictionnary to pickle file
    """

    document = process_files(pdf_path, docx_path, synopsis_path)

    with open(document_output_path, "wb") as f:
        pickle.dump(document, f)


@validate_params
def extract_tables_chunks(pickle_file, tables_output_path):
    """
    Saves tables from pickle document to new pickle file.
    """
    with open(pickle_file, "rb") as f:
        document = pickle.load(f)

    text_chunks = [
        (
            " ".join(document["tables"][key][:2])
            + "\n".join(document["tables"][key][2].iloc[:, 0].astype(str).tolist()),
            key,
        )
        for key in document["tables"].keys()
    ]

    with open(tables_output_path, "wb") as f:
        pickle.dump(text_chunks, f)


@validate_params
def fetch_abstracts(keywords, abstracts_output_path):
    articlesPD = fetch_from_keywords(keywords)
    articlesPD.to_csv(abstracts_output_path, index=None, header=True)
    return articlesPD


def main():
    # Chemin vers le fichier de configuration JSON
    rag_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(rag_dir, "..", "config.json")

    if docker:
        config_path = "/app/" + config_path
    # Lire le fichier de configuration JSON

    with open(config_path, "r") as f:
        config = json.load(f)

    pdf_path = config.get("pdf_path")
    pdf_path = os.path.join(rag_dir, "..", pdf_path)

    docx_path = config.get("docx_path")
    docx_path = os.path.join(rag_dir, "..", docx_path)

    synopsis_path = config.get("synopsis_path")
    synopsis_path = os.path.join(rag_dir, "..", synopsis_path)

    document_output_path = config.get("document_output_path")
    document_output_path = os.path.join(rag_dir, "..", document_output_path)

    tables_output_path = config.get("tables_output_path")
    tables_output_path = os.path.join(rag_dir, "..", tables_output_path)

    abstracts_output_path = config.get("abstracts_output_path")
    abstracts_output_path = os.path.join(rag_dir, "..", abstracts_output_path)

    if not pdf_path or not docx_path or not document_output_path:
        raise ValueError(
            "Le fichier de configuration JSON doit contenir les clés 'pdf_path', 'docx_path', et 'output_path'."
        )

    # 1. Save document to pickle file
    # Exécuter la fonction preprocess
    preprocess(pdf_path, docx_path, synopsis_path, document_output_path)

    # 2. Extract table chunks from document pickle and save them to tables pickle file
    # -> tables_output_path
    # Exécuter la fonction read pour afficher le contenu du fichier pickle
    extract_tables_chunks(document_output_path, tables_output_path)
    # document_output_path is a pickle file
    # tables_output_path is a pickle file

    keywords = ["knee", "bucket"]
    # 3. Fetch abstracts and save to csv
    fetch_abstracts(keywords, abstracts_output_path)
    # saves abstracts to csv abstracts_output_path


if __name__ == "__main__":
    main()
