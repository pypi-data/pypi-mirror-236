# Embedder Node compatible with haystack framework
import os
import sys
from pathlib import Path
from typing import List, Union

import numpy as np
from haystack.nodes.retriever import EmbeddingRetriever
from haystack.nodes.retriever._base_embedding_encoder import _BaseEmbeddingEncoder
from haystack.schema import Document


class _JohnsnowlabsEmbeddingEncoder(_BaseEmbeddingEncoder):
    def __init__(self, retriever: "EmbeddingRetriever"):
        # 1) Check imports
        try:
            from johnsnowlabs import nlp
            from nlu.pipe.pipeline import NLUPipeline
        except ImportError as exc:
            raise ImportError(
                "Could not import johnsnowlabs python package. "
                "Please install it with `pip install johnsnowlabs`."
            ) from exc

        # 2) Start a Spark Session
        try:
            os.environ["PYSPARK_PYTHON"] = sys.executable
            os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable
            nlp.start(hardware_target="gpu" if retriever.use_gpu else "cpu")
        except Exception as exc:
            raise Exception("Failure starting Spark Session") from exc
            # 3) Load the model
        try:
            self.embedding_model = nlp.load(retriever.embedding_model)
        except Exception as exc:
            raise Exception("Failure loading model") from exc

    def embed(self, texts: Union[List[str], str]) -> np.ndarray:
        return np.asarray(
            self.embedding_model.predict_embeds(texts),
            dtype=float,
        )

    def embed_queries(self, queries: List[str]) -> np.ndarray:
        return self.embed(queries)

    def embed_documents(self, docs: List[Document]) -> np.ndarray:
        return self.embed([d.content for d in docs])

    def train(
        **kwargs,
    ):
        raise NotImplementedError("Training not supported")

    def save(self, save_dir: Union[Path, str]):
        raise NotImplementedError("Saving not supported")


class JohnsnowlabsEmbeddingRetriever(EmbeddingRetriever):
    def __init__(self, **kwargs):
        inject()
        super().__init__(**kwargs)


def inject():
    # inject the emd encoder into haystack
    from haystack.nodes.retriever import _embedding_encoder

    _embedding_encoder._EMBEDDING_ENCODERS[
        "johnsnowlabs"
    ] = _JohnsnowlabsEmbeddingEncoder
    # inject the retriever into haystack


inject()
