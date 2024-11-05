from torch import Tensor
from typing import Any
from vector_database import VectorStoreConfig
from vector_database.query_paths import QueryPaths
from rag_configuration import CFG







def retrieve_elements(user_query:str, model:Any, config:VectorStoreConfig=VectorStoreConfig(), general_config:CFG=CFG()) -> Any:
    """Finds the configured amount of most semantically similar documents to the input embeddings.

    :param user_query: Query string to find the most similar documents.
    :param model: Embedding Model.
    :param config: VectorStoreConfig object holding vector store settings.
    :param general_config: CFG object holding general settings.
    :return: Query Results
    """
    embedding = model.encode(user_query, task=general_config.retrieval_task)
    connection, cursor = config.get_connection_items()
    query = QueryPaths.RETRIEVE.get_query().format(str(embedding.tolist()), config.number_of_retrieved_documents)
    cursor.execute(query)
    elements = cursor.fetchall()
    cursor.close()
    connection.close()
    return elements