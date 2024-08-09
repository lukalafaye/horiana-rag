from src.healthdraft.extractors.pdf_extractor import get_table_id
from docx import Document
import pandas as pd


def fix_encoding_issues(text):
    """
    Fix encoding issues after docx parsing.
    ³ -> >=
    ³  unicode characters by docx

    Args:

    Returns:

    """
    replacements = {"³": ">=", "£": "<="}
    for wrong, correct in replacements.items():
        text = text.replace(wrong, correct)
    return text


def extract_tables_from_doc(path):
    doc = Document(path)
    tables = []
    for table in doc.tables:
        num_columns = len(table.columns)
        num_rows = len(table.rows)
        df = [["" for i in range(num_columns)] for j in range(num_rows)]
        for i, row in enumerate(table.rows):
            for j, cell in enumerate(row.cells):
                if cell.text:
                    df[i][j] = fix_encoding_issues(cell.text)
        tables.append(pd.DataFrame(df))
    return tables


def tooSmall(table):
    """
    Checks if table is too small to be a statistical table
    """
    lineCount, columnCount = table.shape[0], table.shape[1]
    return (lineCount <= 1) or (columnCount <= 1)


def addRelevantDocTable(relevant_tables, table, title):
    """
    Adds table to dictionnary using specific id
    If unique id -> 1.1.1.1
    If duplicate id -> 1.1.1.1-Page1 / 1.1.1.1-Page2 ...
    """
    idcheck = ""
    newid = ""

    id = get_table_id(title)

    if id in relevant_tables.keys():
        # ("table id already in")
        idcheck = f"{id}-Page1"
        if idcheck not in relevant_tables.keys():
            # ("ID Page 1 and 2 don't exist")
            relevant_tables[idcheck] = relevant_tables.pop(id)
            newid = f"{id}-Page2"
            relevant_tables[newid] = table
        else:  # ID Page 1 and 2 already in dict
            # ("Page 1 and 2 already exist")
            i = 1
            while f"{id}-Page{i}" in relevant_tables.keys():
                i += 1
            newid = f"{id}-Page{i}"
            relevant_tables[newid] = table
    else:
        # ("Not a duplicate, adding...")
        relevant_tables[id] = table

    return relevant_tables


def fetch_relevant_tables(tables):
    """
    Retrieves all relevant statistical tables as well
    as their id (obtained using title)
    Returns dictionnary {"idPagei": tabledf}
    """
    relevant_tables = {}
    title = ""

    addBool = False

    startIndex = 0
    indexTableNotFound = True
    # look for index table

    j = 0
    while indexTableNotFound:
        table = tables[j]
        if (
            table.shape[0] >= 1
            and table.shape[1] >= 1
            and (
                "List of tables" in table.iloc[0, 0]
                or "Liste des tables" in table.iloc[0, 0]
            )
        ):
            # look for next table
            current = j + 1
            while tooSmall(tables[current]):
                current += 1
            # current corresponds to index table
            indexTableNotFound = False
        j += 1

    startIndex = current + 1
    # we start looking for tables just after table index
    # (otherwise we don't retrieve the first table)

    for i in range(startIndex, len(tables)):
        table = tables[i]
        if table.shape[0] >= 1 and table.shape[1] >= 1:
            if "Table" in table.iloc[0, 0]:
                title = table.iloc[0, 0].strip()
                addBool = True

            if "Table" in table.iloc[-1, 0]:
                title = table.iloc[-1, 0].strip()
                addBool = True

            if table.shape[0] >= 2 and "Table" in table.iloc[-2, 0]:
                title = table.iloc[-2, 0].strip()
                addBool = True

        if addBool:
            current = i + 1
            while tooSmall(tables[current]):
                current += 1
            # current is the index of a correct sized table containing values
            relevant_tables = addRelevantDocTable(
                relevant_tables, tables[current], title
            )
            addBool = False

    return relevant_tables
