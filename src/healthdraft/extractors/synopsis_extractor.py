from docx import Document
from pprint import pprint
import unicodedata
import json
from src.config import (
    get_absolute_path,
)  # will also run config.py, setting up env variables

docker = False


def extract_content(path):
    doc = Document(path)

    tables_text = []
    for table in doc.tables:
        for row in table.rows:
            row_text = [cell.text for cell in row.cells]
            tables_text.append(row_text)

    content = [(tables_text[i][0], tables_text[i][1]) for i in range(len(tables_text))]
    content = dict(content)

    return content


def remove_accents(input_str):
    """
    Remove accents from a given string.
    """
    normalized_str = unicodedata.normalize("NFD", input_str)
    return "".join(c for c in normalized_str if unicodedata.category(c) != "Mn")


def extract_section(content, identifier):
    """
    Extrait la section: Titre/Acronyme
    """
    identifier = remove_accents(identifier.lower())

    for key in content.keys():
        key_normalized = remove_accents(key.strip().lower())
        identifier_normalized = remove_accents(identifier.strip().lower())
        if identifier_normalized in key_normalized:
            # print(identifier + ': \n' + content[key] + '\n\n')
            return content[key]

    print(f"Section {identifier} not found")
    return None


def main():
    config_path = get_absolute_path("config.json")

    if docker:
        config_path = "/app/" + config_path

    # Lire le fichier de configuration JSON
    with open(config_path, "r") as f:
        config = json.load(f)

    synopsis_path = get_absolute_path(config.get("synopsis_path"))

    content = extract_content(synopsis_path)

    sections = {
        "title": "Titre",
        "team": "équipe",
        "context_objectives": "contexte",
        "ethics": "ethique",
        "public_interest": "intérêt",
        "publication": "publication",
        "required_data": "requises",
        "population": "cohorte",
        "methods": "analyses",
        "circulation": "circulation",
        "calendar": "calendrier",
        "protection": "protection",
    }

    extracted_data = {
        key: extract_section(content, value) for key, value in sections.items()
    }
    pprint(extracted_data)


if __name__ == "__main__":
    main()
