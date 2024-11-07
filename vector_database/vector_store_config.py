import psycopg2
from psycopg2._psycopg import connection, cursor
from ast import literal_eval


class VectorStoreConfig:
    """
        Configuration settings for connecting to and initializing the vector store database.

        Attributes:
            number_of_retrieved_documents (int): Number of documents to retrieve during search operations.
            number_of_reranked_documents (int): Number of documents to rerank for relevance after retrieval.
            initialization_parameters_path (str): Path to the file containing database connection parameters.
            default_db_initialization_path (str): Path to the SQL file for database initialization.

        Methods:
            get_connection_items() -> tuple[connection, cursor]:
                Establishes a connection to the database using parameters from `initialization_parameters_path`.
                Returns a tuple containing the database connection and a new cursor.
    """
    number_of_retrieved_documents: int = 100
    number_of_reranked_documents:int = 5

    initialization_parameters_path: str = 'docker_stuff/db_parameters.eval'
    default_db_initialization_path: str = 'vector_database/queries/init.sql'

    @classmethod
    def get_connection_items(cls) -> tuple[connection, cursor]:
        """
            Establishes a connection to the vector store database and returns the connection and cursor objects.

            :return: A tuple containing:
                     - conn (connection): The database connection object.
                     - new_cursor (cursor): The cursor object for executing database commands.

            The database connection parameters are read from the file specified by `initialization_parameters_path`.
            """
        with open(cls.initialization_parameters_path, 'r') as f:
            db_params = literal_eval(f.read())

        conn = psycopg2.connect(**db_params)
        new_cursor = conn.cursor()
        return conn, new_cursor