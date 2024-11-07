import pandas as pd
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


def get_reranked_documents(query: str, embedder: Any, reranker: Any, config: CFG = CFG()) -> pd.DataFrame:
    """
    Retrieves and reranks documents based on their relevance to the specified query.

    This function first retrieves a list of documents using an embedding-based retrieval model
    by calculating cosine similarities between the query and document embeddings. After retrieval,
    it uses a reranker model to score each document based on its relevance to the query.
    The top-k documents, determined by the `number_of_retrieved_documents` setting in the `config`
    object, are then selected, sorted by their reranking scores in descending order, and returned
    in a DataFrame format.

    :param query: A string containing the search query for retrieving relevant documents.
    :param embedder: An embedding model or function that computes document embeddings and retrieves
                     a list of documents similar to the query based on cosine similarity.
    :param reranker: A reranker model or function that computes relevance scores for each document
                     based on its relationship to the query.
    :param config: A configuration object of type `CFG` that specifies retrieval and reranking settings,
                   such as `number_of_retrieved_documents`, which determines the number of top documents to return.

    :return: A DataFrame containing the top-k retrieved and reranked documents, with the following columns:
        - "document_filename": The filename of the document retrieved.
        - "title": The title of the document, if available.
        - "section": The section of the document where the retrieved content is located.
        - "heading": The heading associated with the retrieved content.
        - "text": The actual text of the retrieved document portion.
        - "table_flag": A boolean flag indicating whether the content is in table format.
        - "page_number": The page number where the retrieved content is found.
        - "cosine_similarity": The cosine similarity score between the query and the retrieved document.
        - "reranking_score": The relevance score assigned by the reranker model, used to determine the final ranking.

    The DataFrame is sorted by `reranking_score` in descending order and reset to ensure a zero-based index.

    Example:
        >>> get_reranked_documents("machine learning in healthcare", embedder, reranker, config)
        returns a DataFrame with the top-k documents most relevant to the query, ranked by `reranking_score`.

    """
    
    results = retrieve_elements(query, embedder)
    document_filename, titles, sections, headings, texts, table_flags, page_numbers, cosine_similarities = zip(*results)
    scores = reranker.compute_score([[query, text] for text in texts])
    top_k_scores = scores.copy()
    top_k_scores.sort(reverse=True)
    top_k_scores = top_k_scores[:config.number_of_retrieved_documents]
    top_k_results = [
        (doc, title, section, heading, text, flag, page, similarity, score)
        for doc, title, section, heading, text, flag, page, similarity, score in zip(
            document_filename, titles, sections, headings, texts, table_flags, page_numbers, cosine_similarities, scores
        )
        if score in top_k_scores
    ]
    df_top_k = pd.DataFrame(top_k_results, columns=[
        "document_filename", "title", "section", "heading", "text", "table_flag", "page_number", "cosine_similarity",
        "reranking_score"
    ])
    df_top_k = df_top_k.sort_values(by="reranking_score", ascending=False).reset_index(drop=True)
    return df_top_k
