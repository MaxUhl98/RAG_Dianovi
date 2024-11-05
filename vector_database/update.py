from psycopg2.extras import execute_values
from typing import Any
from vector_database import VectorStoreConfig
import traceback
from vector_database.query_paths import QueryPaths
from datasets import Dataset

def insert_rows(data:Dataset, config:VectorStoreConfig=VectorStoreConfig()) -> bool:
    try:
        conn, cursor = config.get_connection_items()
        insert_query = QueryPaths.INSERT.get_query()
        data = [(row['document_title'], row['section_title'], row['headings'], row['embedded_text'], row['embedding'], row['text_content'], row['is_table'], row['document_filename'], row['page_number']) for row in data]
        execute_values(cursor, insert_query, data)
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception:
        traceback.print_exc()
        return False
