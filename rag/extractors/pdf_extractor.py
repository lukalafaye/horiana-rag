from PyPDF2 import PdfReader
import re


def extract_metadata_pages(pdf_path):
    """
    Returns document metadata and content
    """
    with open(pdf_path, "rb") as f:
        reader = PdfReader(f)
        meta = reader.metadata
        number_of_pages = len(reader.pages)

        pages_text = []
        for n in range(number_of_pages):
            page = reader.pages[n]
            pages_text.append(page.extract_text())

    metadata = f"""
    Information about {pdf_path}:

    Author: {meta.author}
    Creator: {meta.creator}
    Producer: {meta.producer}
    Subject: {meta.subject}
    Title: {meta.title}
    Number of pages: {number_of_pages}
    """

    return metadata, pages_text


def extract_information(pages_text):
    # preprocess first page to remove all text before "AP"
    start = pages_text[0].find("AP ")  # AP not always in there
    if start == -1:
        start = pages_text[0].find(
            "ÉTUDE"
        )  # Add first word after title for each new doc type!!!!!

    if start == -1:
        start = pages_text[0].find(
            "STUDY"
        )  # Add first word after title for each new doc type!!!!!

    docinfot = pages_text[0][start:]

    docinfop = r"\s*(?P<key>[\w° ]+):\s*(?P<value>.*?\n)"
    docinfom = re.findall(docinfop, docinfot, re.DOTALL)
    information = {key.strip(): value.strip() for key, value in docinfom}

    return information


def extract_title(pages_text):
    titlep = r"(REPORT|STATISTIQUE)[ ]*\s+(?P<title>.*?)\n[ ]*(\n|AP)"
    # On suppose que la fin du titre = \n\n...!!!
    titlem = re.search(titlep, pages_text[0], re.DOTALL)
    title = titlem.group("title").strip()
    return title


def extract_methods(pages_text):
    # Preprocess index page to remove all text before "1."
    # so that title containing ":" is not a problem!!!

    start = pages_text[1].find("1.")
    indext = pages_text[1][start:]

    methodspagep = r"POPULATION.*?(?P<page>\d)"
    methodspagem = re.search(methodspagep, indext, re.DOTALL)
    methodspage = methodspagem.group("page").strip()

    methodspagenum = int(methodspage) - 1
    methodstext = pages_text[methodspagenum]

    methodsp = r"\s*\d\.\d\.\s+(?P<header>.*?) *\n\s*(?P<text>.*?)(?=1\.|$)"
    methodsm = re.findall(methodsp, methodstext, re.DOTALL)
    methods = {header.strip(): text.strip() for header, text in methodsm}

    return methods


def extract_keyresults(pages_text):
    text = " \n ".join(pages_text)

    start = text.rfind("KEY RESULTS")  # rfind checks for last occurence
    if start == -1:
        start = text.rfind("CHIFFRES CLES")

    if start != -1:
        keyResults = text[start:]
        return keyResults.strip()
    else:
        print("'KEY RESULTS' & 'CHIFFRES CLES' not found.")


def get_table_title(data):
    """
    Returns table title (table raw text is in data)
    """
    # Adjusted regex to stop at [-–] followed by Population or Analysis, or match the whole line otherwise
    tabletitlep = r"Table\s*\d+(?:\.\d+)*\.\s*(?P<title>.*?)(?=\s*[-–]\s*(Population|Analysis|Chronic|Included|Analyzed))|Table\s*\d+(?:\.\d+)*\.\s*(?P<title_full>.*)"
    tabletitlem = re.search(tabletitlep, data, re.DOTALL)
    title = tabletitlem.group(0).strip()

    return title


def get_table_id(title):
    """
    Extract Id from table
    """
    tableidp = r"Table\s+((\d+\.)*\d+)"
    tabletitlem = re.search(tableidp, title)
    id = tabletitlem.group(1).strip()
    return id.strip()


def isValueLine(line):
    """
    Returns True if line contains values/NR, False if it just contains text...
    """
    pattern = r"\s[-]*\d+\s|NR|\(\s*[-]*\d+|\[\s*[-]*\d+|\s\d+\.\d+\s"
    match = re.search(pattern, line)
    return match is not None


def remove_spaces(match):  # Used by preprocessDataLine
    if match.group("parenthese") is not None:
        text = match.group("parenthese")
        opening_bracket, closing_bracket = "(", ")"
    if match.group("sbracket") is not None:
        text = match.group("sbracket")
        opening_bracket, closing_bracket = "[", "]"

    no_spaces_text = text.replace(" ", "")

    return f"{opening_bracket}{no_spaces_text}{closing_bracket}"


def preprocessDataLine(data):
    """
    Supprime les espaces au sein de () et [] dans la ligne data
    """
    pattern = r"\((?P<parenthese>.*?)\)|\[(?P<sbracket>.*?)\]"
    result = re.sub(
        pattern, remove_spaces, data
    )  # enlever les espaces au sein de ( ) ou [ ]
    return result


def get_table_title_description(table_text):
    """
    Returns title and description for given table
    """
    lines = table_text.strip().split("\n")
    lines = [line for line in lines if line.strip()]

    title = get_table_title("".join(lines[0:3]))

    description = ""
    endDesc = False
    # if "ADSL" in line ---> True,
    # ADSL is the end of a table!!!!
    endValLine = 0  # Index of last line containing values

    for line_num in range(1, len(lines)):
        line = preprocessDataLine(lines[line_num])
        if isValueLine(line):
            endValLine = line_num

    for line_num in range(min(endValLine + 1, len(lines)), len(lines)):
        line = preprocessDataLine(lines[line_num])

        if "Page" in line.strip() or "Analysis" in line.strip():
            continue

        if not endDesc and len(line) >= 20:
            description += line
            if "ADSL" in line:
                endDesc = True
    return title, description


def list_page_tables(page_text):
    """
    Returns list of table text strings
    """
    tables = []
    start = page_text.find("Table")

    while start != -1:
        table_text = page_text[start:]
        next_start = table_text.find("Table", 1)

        if next_start != -1:
            tables.append(table_text[:next_start].strip())
            start = start + next_start
        else:
            tables.append(table_text.strip())
            break

    filtered_tables = []
    for table in tables:
        figure_index = table.find(
            "Figure"
        )  # Des fois le texte déborde sur la figure d'après
        if figure_index != -1:
            filtered_tables.append(table[:figure_index].strip())
        else:
            filtered_tables.append(table.strip())

    return filtered_tables


def findFirstTablePageNum(pages_text):
    text = " \n ".join(pages_text)

    start = text.find("List of table")

    if start == -1:  # fr document
        start = text.find("INDEX")  # texte juste avant table indices

    textWithIndex = text[start:]

    firstPageWithTablep = r"\s+(?P<pagenum>\d+)\s+"
    firstPageWithTablem = re.search(firstPageWithTablep, textWithIndex)

    firstPage = int(firstPageWithTablem.group("pagenum")) - 1
    return firstPage


def addRelevantPdfTable(relevant_tables, title, description):
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
            relevant_tables[newid] = [title, description]
        else:  # ID Page 1 and 2 already in dict
            # ("Page 1 and 2 already exist")
            i = 1
            while f"{id}-Page{i}" in relevant_tables.keys():
                i += 1
            newid = f"{id}-Page{i}"
            relevant_tables[newid] = [title, description]
    else:
        # ("Not a duplicate, adding...")
        relevant_tables[id] = [title, description]

    return relevant_tables


def extract_tables(pages_text):
    """
    Stores tables in tables_dict using ids
    id: title, description
    id = 1.1.1Page1 / 1.1.1Page2 and so on if duplicate titles exist...
    """
    tables_dict = {}
    firstPage = findFirstTablePageNum(pages_text)

    for i in range(firstPage, len(pages_text)):
        table_list = list_page_tables(pages_text[i])
        for t in table_list:
            title, description = get_table_title_description(t)
            tables_dict = addRelevantPdfTable(tables_dict, title, description)

    return tables_dict
