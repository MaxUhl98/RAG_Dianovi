from vector_database import VectorStoreConfig
import traceback
from vector_database.query_paths import QueryPaths


def create_vectorstore(config:VectorStoreConfig=VectorStoreConfig()) -> None:
    """
    Initializes and creates the required tables in the vector store database.

    :param config: The configuration for the vector store, used to establish a database connection.
                   Defaults to a new instance of VectorStoreConfig.
    :return: None
    """
    conn, db_cursor = config.get_connection_items()
    with open(QueryPaths.INIT.value, 'r', encoding='utf-8') as file:
        db_cursor.execute(file.read())
    db_cursor.close()
    conn.commit()
    conn.close()


