import torch
from transformers import AutoModelForSequenceClassification, AutoModel
from typing import Any
from rag_configuration import CFG

def load_models(config:CFG=CFG()) -> tuple[Any, Any]:
    """
    Loads and returns pretrained models for document embedding and reranking. This function is

    This function loads two models: an embedding model and a reranker model, using the model names
    specified in the provided configuration object. The embedding model is configured to run on GPU
    with `bfloat16` precision and is set up for efficient attention mechanisms where supported.
    The reranker model is loaded with automatic precision based on device compatibility.

    :param config: A configuration object of type `CFG` that specifies model parameters, including:
                   - `embedding_model_name`: The name or path of the pretrained embedding model to load.
                   - `reranker_model_name`: The name or path of the pretrained reranker model to load.

    :return: A tuple containing:
        - `embedder`: The loaded embedding model (`AutoModel`), configured for document similarity computation.
        - `reranker`: The loaded reranker model (`AutoModelForSequenceClassification`), configured for relevance scoring.
    """
    embedder = AutoModel.from_pretrained(config.embedding_model_name, trust_remote_code=True,
                                            torch_dtype=torch.bfloat16, use_flash_attn=False).to(torch.get_default_device())
    reranker = AutoModelForSequenceClassification.from_pretrained(
        config.reranker_model_name, trust_remote_code=True,
        torch_dtype='auto').to(torch.get_default_device())
    return embedder, reranker