from psycopg2.extras import execute_values
from typing import Any
from vector_database import VectorStoreConfig
import traceback
from vector_database.query_paths import QueryPaths
from datasets import Dataset

def insert_rows(data:Dataset, config:VectorStoreConfig=VectorStoreConfig()) -> None:
    """
    Inserts multiple rows into a vector store using a specified configuration.

    :param data: A dataset containing the rows to insert. Each row should be a dictionary with keys:
                 - 'document_title': The title of the document.
                 - 'section_title': The title of the document section.
                 - 'headings': The hierarchical headings of the document section.
                 - 'embedded_text': The text for which the embeddings get calculated.
                 - 'embedding': The embedding vector representing the text content.
                 - 'text_content': The original text content.
                 - 'is_table': A boolean indicating if the content is in table format.
                 - 'document_filename': The filename of the document.
                 - 'page_number': The page number from which the text was extracted.
    :param config: The configuration for the vector store, used to establish a connection. Defaults to an instance of VectorStoreConfig.
    :return: None
    """
    conn, cursor = config.get_connection_items()
    insert_query = QueryPaths.INSERT.get_query()
    data = [(row['document_title'], row['section_title'], row['headings'], row['embedded_text'], row['embedding'], row['text_content'], row['is_table'], row['document_filename'], row['page_number']) for row in data]
    execute_values(cursor, insert_query, data)
    conn.commit()
    cursor.close()
    conn.close()

