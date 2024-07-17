import pickle
from pathlib import Path
from pprint import pprint
import json 

from rag.extractors.utils import process_files  # Updated import path


def preprocess(pdf_path, doc_path, output_path):
    """
    Extracts document info using pdf and docx in a dictionnary
    Saves dictionnary to pickle file
    """
    document = process_files(pdf_path, doc_path)

    with open(output_path, "wb") as f:
        pickle.dump(document, f)

def extract_tables_chunks(pickle_file, tables_output_path):
    """
    Saves tables from pickle document to new pickle file.
    """
    with open(pickle_file, "rb") as f:
        document = pickle.load(f)

    text_chunks = [(" ".join(document["tables"][key][:2]) + '\n'.join(document["tables"][key][2].iloc[:, 0].astype(str).tolist()), key) for key in document["tables"].keys()]

    with open(tables_output_path, "wb") as f:
        pickle.dump(text_chunks, f)

def main():
    # Chemin vers le fichier de configuration JSON
    config_path = Path('.vscode/config.json')

    # Lire le fichier de configuration JSON
    with open(config_path, 'r') as f:
        config = json.load(f)

    pdf_path = config.get('pdf_path')
    doc_path = config.get('doc_path')
    output_path = config.get('output_path')
    tables_path = config.get("tables_path")

    if not pdf_path or not doc_path or not output_path:
        raise ValueError("Le fichier de configuration JSON doit contenir les clés 'pdf_path', 'doc_path', et 'output_path'.")

    # Assurez-vous que les chemins sont valides
    pdf_path = Path(pdf_path)
    doc_path = Path(doc_path)
    output_path = Path(output_path)


    # Exécuter la fonction preprocess
    preprocess(pdf_path, doc_path, output_path)

    # Exécuter la fonction read pour afficher le contenu du fichier pickle
    extract_tables_chunks(output_path, tables_path)
    
if __name__ == "__main__":
    main()
