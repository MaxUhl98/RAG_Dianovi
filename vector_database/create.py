from vector_database import VectorStoreConfig
import traceback
from vector_database.query_paths import QueryPaths


def create_vectorstore(config:VectorStoreConfig=VectorStoreConfig()) -> bool:
    try:
        conn, db_cursor = config.get_connection_items()
        with open(QueryPaths.INIT.value, 'r', encoding='utf-8') as file:
            db_cursor.execute(file.read())
        db_cursor.close()
        conn.commit()
        conn.close()
        return True
    except Exception:
        traceback.print_exc()
        return False

