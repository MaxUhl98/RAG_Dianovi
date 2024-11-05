import fitz
from collections import defaultdict
from typing import Any
import re

def contains_valid_word_like_sequence(input_string:str) -> bool:
    # This regex matches sequences of letters (a-z, A-Z) while ignoring whitespace and non-letter characters
    pattern = r'[a-zA-Z]+'
    # Search for any valid word-like sequence in the string
    return bool(re.search(pattern, input_string))

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
                    for span in line["spans"]:
                        text = span['text']
                        font = span['font']
                        if contains_valid_word_like_sequence(text) or not 'bold' in font.lower():
                            data.append({'text': text, 'font': font, 'page': page_num})
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
