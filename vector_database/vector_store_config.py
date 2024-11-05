import psycopg2
from psycopg2._psycopg import connection, cursor
from ast import literal_eval


class VectorStoreConfig:
    number_of_retrieved_documents: int = 50
    number_of_reranked_documents:int = 5

    initialization_parameters_path: str = 'docker_stuff/db_parameters.eval'
    default_db_initialization_path: str = 'vector_database/queries/init.sql'

    @classmethod
    def get_connection_items(cls) -> tuple[connection, cursor]:
        with open(cls.initialization_parameters_path, 'r') as f:
            db_params = literal_eval(f.read())

        conn = psycopg2.connect(**db_params)
        new_cursor = conn.cursor()
        return conn, new_cursor