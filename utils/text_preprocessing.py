import fitz
from collections import defaultdict
from typing import Any
import re
from rag_configuration import CFG

def get_title(pdf_path: str, config: CFG = CFG()) -> str:
    """
    Extracts and formats the title of the document from the PDF file path
    based on a specified pattern in the configuration.

    :param pdf_path: The file path of the PDF document.
    :param config: A configuration object containing the filename pattern.
                   Defaults to an instance of CFG.
    :return: The title of the document, with hyphens and underscores replaced
             by spaces.
    """
    return re.search(config.filename_pattern, pdf_path).group(1).replace('-', ' ').replace('_', ' ')


def contains_valid_word_like_sequence(input_string: str) -> bool:
    """
    Checks if the input string contains any word-like sequence of letters,
    disregarding non-letter characters and whitespace.

    :param input_string: The string to be checked.
    :return: True if there is a sequence of letters (a-z or A-Z) in the string,
             otherwise False.
    """
    pattern = r'[a-zA-Z]+'
    return bool(re.search(pattern, input_string))


def extract_line_contents(line: Any, data: list[dict[str, Any]], page_num: int) -> list[dict[str, Any]]:
    """
    Extracts text and font information from each span within a line and
    appends valid spans to the data list if they contain word-like sequences
    or are not in bold font.

    :param line: A line object containing text spans, typically from a PDF page.
    :param data: A list of dictionaries holding extracted text data.
    :param page_num: The page number (0-indexed) from which the line was read.
    :return: The updated list of dictionaries, each representing a span with
             text, font, and page information.
    """
    for span in line["spans"]:
        text = span['text']
        font = span['font']
        if contains_valid_word_like_sequence(text) or 'bold' not in font.lower():
            data.append({'text': text, 'font': font, 'page': page_num})
    return data



def extract_document_data(pdf_path: str) -> list[dict[str, Any]]:
    """
    Extracts text data from each page of a PDF document, identifying the font
    and page number of each text span. Each entry in the list corresponds to a
    span of text with associated metadata.

    :param pdf_path: The file path of the PDF document to be read.
    :return: A list of dictionaries, each containing the text, font, and page
             number of a span within the document. Each dictionary has the keys:
             - 'text': The text content of the span.
             - 'font': The font name of the span.
             - 'page': The page number (0-indexed) where the span appears.
    """
    doc = fitz.open(pdf_path)
    data = []
    for page_num in range(doc.page_count):
        page = doc[page_num]
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    data = extract_line_contents(line,data, page_num)
    doc.close()
    return data



def get_section_maps(data: list[dict[str, Any]]) -> tuple[dict[str, Any], dict[str, Any]]:
    """
    Processes extracted document data to group content into sections based on
    bold headings. Creates mappings for section content and the page on which
    each section starts.

    :param data: A list of dictionaries containing text spans with their font
                 and page metadata, typically from `extract_document_data`.
    :return: A tuple containing two dictionaries:
             - sections: Maps each section title to its accumulated text content.
             - section_page_map: Maps each section title to the ending page
               number (0-indexed) in the document.
    """
    sections = defaultdict(lambda: '')
    current_section = ""
    last_was_bold = False
    section_page_map = {}
    for item in data:
        text = item['text'].strip()
        font = item['font']
        page = item['page']
        if 'bold' in font.lower():
            if not last_was_bold:
                current_section = ''
            current_section += ' ' + text
            last_was_bold = True
        else:
            section_page_map[current_section.strip()] = page
            sections[current_section.strip()] += '\n' + text
            last_was_bold = False
    return sections, section_page_map


def get_document_maps(filepath: str) -> tuple[dict[str, Any], dict[str, Any]]:
    """
    Reads a PDF document, extracts data, and generates section maps.

    :param filepath: The file path of the PDF document to be processed.
    :return: A tuple of two dictionaries:
             - sections: Maps each section title to its text content.
             - section_page_map: Maps each section title to its ending page.
    """
    return get_section_maps(extract_document_data(filepath))
