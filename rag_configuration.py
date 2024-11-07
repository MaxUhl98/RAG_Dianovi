from typing import Literal
class CFG:
    dataset_path:str = 'data/preprocessed_rag_chunks_no_embedding'
    embedding_model_name: str = 'jinaai/jina-embeddings-v3'
    number_of_retrieved_documents:int = 5
    task: Literal['retrieval.query', 'retrieval.passage', 'separation', 'classification', 'text-matching'] = 'retrieval.passage'
    retrieval_task = 'retrieval.query'
    embedding_size: Literal[32, 64, 128, 256, 512, 1024] = 1024
    data_dir: str = 'data'
    reranker_model_name: str = 'jinaai/jina-reranker-v2-base-multilingual'  #'Alibaba-NLP/gte-multilingual-reranker-base'
    index_dot_percentage_threshold: float = .25
    chapter_extraction_pattern: str = r"(?:(?:\b\d{1,2}\b|[IVXLCDM]+|[A-Z](?:\.\d+)?)[\.\)]?\s*)([A-ZÄÖÜa-zäöüß].*?)(?=\n|$)"
    filename_pattern: str = r'_(.*?)_\d{4}-\d{2}\.pdf'
    minimal_headline_length: int = 3
