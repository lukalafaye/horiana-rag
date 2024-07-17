import pickle 
from pathlib import Path
import json 
from pprint import pprint 
from biobert_embedding.embedding import BiobertEmbedding


def display_tables(pickle_file):
    """
    Displays tables text chunks stored in pickle file.
    """
    with open(pickle_file, "rb") as f:
        tables = pickle.load(f)

    #pprint(tables[0])

def main():
    config_path = Path('.vscode/config.json')

    # Lire le fichier de configuration JSON
    with open(config_path, 'r') as f:
        config = json.load(f)

    tables_path = config.get("tables_path")    
    display_tables(tables_path)
    
if __name__ == "__main__":
    main()
