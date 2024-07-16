import json
import sys
from pprint import pprint
import pickle

from rag.extractors.utils import process_files  # Updated import path

def preprocess(pdf_path, doc_path, output_path):
    document = process_files(pdf_path, doc_path)

    with open(output_path, 'wb') as f:
        pickle.dump(document, f)

def main():
    if len(sys.argv) != 4:
        print("Usage: preprocess <pdf_path> <doc_path> <output_path>")
        sys.exit(1)

    pdf_path = sys.argv[1]
    doc_path = sys.argv[2]
    output_path = sys.argv[3]

    preprocess(pdf_path, doc_path, output_path)

if __name__ == "__main__":
    main()
