from __future__ import annotations

import enum
import logging
import uuid, json, re
import numpy as np
from urllib.parse import urlparse

from langchain.utils import get_from_dict_or_env
from langchain.docstore.document import Document
from langchain.schema.embeddings import Embeddings
from langchain.schema.vectorstore import VectorStore
from fsevector.fsedocstore.docstore import FseDoc

from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Generator,
    Iterable,
    List,
    Optional,
    Tuple,
    Type,
)

class DistanceStrategy(str, enum.Enum):
    """Enumerator of the Distance strategies."""
    EUCLIDEAN = "l2"
    COSINE = "cosine"
    MAX_INNER_PRODUCT = "inner"

DEFAULT_DISTANCE_STRATEGY = DistanceStrategy.COSINE
_LANGCHAIN_DEFAULT_COLLECTION_NAME = "langchain"

def _results_to_docs(docs_and_scores: Any) -> List[Document]:
    """Return docs from docs and scores."""
    return [doc for doc, _ in docs_and_scores]

class FseVector(VectorStore):
    """`Postgres`/`FseVector` vector store.

    To use, you should have the ``FseVector`` python package installed.

    Args:
        fsedoc_connection_string: Postgres connection string.
        fseaddr_connection_string: fse connection string.
        embedding_function: Any embedding function implementing
            `langchain.embeddings.base.Embeddings` interface.
        collection_name: The name of the collection to use. (default: langchain)
            NOTE: This is not the name of the table, but the name of the collection.
            The tables will be created when initializing the store (if not exists)
            So, make sure the user has the right permissions to create tables.
        distance_strategy: The distance strategy to use. (default: COSINE)
        pre_delete_collection: If True, will delete the collection if it exists.
            (default: False). Useful for testing.

    Example:
        .. code-block:: python

            from langchain.vectorstores import FseVector
            from langchain.embeddings.openai import OpenAIEmbeddings

            FSEDOC_CONNECTION_STRING = "fsedoc://user:passwd@localhost:port"
            FSEADDR_CONNECTION_STRING = "fseaddr://localhost:port"
            COLLECTION_NAME = "langchain"
            embedding_function = OpenAIEmbeddings()
            vectorestore = FseVector.from_documents(
                embedding=embeddings,
                documents=docs,
                collection_name=COLLECTION_NAME,
                fsedoc_connection_string=FSEDOC_CONNECTION_STRING,
                fseaddr_connection_string=FSEADDR_CONNECTION_STRING
            )
    """

    def __init__(
        self,
        fsedoc_connection_string: str,
        fseaddr_connection_string: str,
        embedding_function: Embeddings,
        collection_name: str = _LANGCHAIN_DEFAULT_COLLECTION_NAME,
        distance_strategy: DistanceStrategy = DEFAULT_DISTANCE_STRATEGY,
        pre_delete_collection: bool = False,
        logger: Optional[logging.Logger] = None,
        relevance_score_fn: Optional[Callable[[float], float]] = None,
    ) -> None:
        self.fsedoc_connection_string = fsedoc_connection_string
        self.fseaddr_connection_string = fseaddr_connection_string
        self.embedding_function = embedding_function
        self.collection_name = collection_name
        self._distance_strategy = distance_strategy
        self.pre_delete_collection = pre_delete_collection
        self.logger = logger or logging.getLogger(__name__)
        self.logger.info('fsevector init entry')
        self.override_relevance_score_fn = relevance_score_fn
        self.__post_init__()

    def __post_init__(
        self,
    ) -> None:
        self.logger.debug('fsedoc: %s, fseaddr: %s', self.fsedoc_connection_string, self.fseaddr_connection_string)
        pgurl = urlparse(self.fsedoc_connection_string)
        fseurl = urlparse(self.fseaddr_connection_string)
        self.fsedoc = FseDoc(dbhost=pgurl.hostname, dbport=pgurl.port, user=pgurl.username, password=pgurl.password,
                             fsehost=fseurl.hostname, fseport=fseurl.port, repo=self.collection_name)
        if self.pre_delete_collection:
            self.fsedoc.clear()

    @classmethod
    def from_documents(
        cls: Type[FseVector],
        embedding: Embeddings,
        documents: List[Document],
        collection_name: str = _LANGCHAIN_DEFAULT_COLLECTION_NAME,
        distance_strategy: DistanceStrategy = DEFAULT_DISTANCE_STRATEGY,
        ids: Optional[List[str]] = None,
        pre_delete_collection: bool = False,
        **kwargs: Any,
    ) -> FseVector:
        """
        Return VectorStore initialized from documents and embeddings.
        Postgres connection string is required
        "Either pass it as a parameter
        or set the FSEVECTOR_CONNECTION_STRING environment variable.
        """

        texts = [d.page_content for d in documents]
        metadatas = [d.metadata for d in documents]
        fsedoc_connection_string = cls.get_fsedoc_connection_string(kwargs)
        fseaddr_connection_string = cls.get_fseaddr_connection_string(kwargs)

        kwargs["fsedoc_connection_string"] = fsedoc_connection_string
        kwargs["fseaddr_connection_string"] = fseaddr_connection_string

        return cls.from_texts(
            texts=texts,
            pre_delete_collection=pre_delete_collection,
            embedding=embedding,
            distance_strategy=distance_strategy,
            metadatas=metadatas,
            ids=ids,
            collection_name=collection_name,
            **kwargs,
        )

    @property
    def embeddings(self) -> Embeddings:
        return self.embedding_function

    @classmethod
    def __from(
        cls,
        texts: List[str],
        embeddings: List[List[float]],
        embedding: Embeddings,
        metadatas: Optional[List[dict]] = None,
        ids: Optional[List[str]] = None,
        collection_name: str = _LANGCHAIN_DEFAULT_COLLECTION_NAME,
        distance_strategy: DistanceStrategy = DEFAULT_DISTANCE_STRATEGY,
        fsedoc_connection_string: Optional[str] = None,
        fseaddr_connection_string: Optional[str] = None,
        pre_delete_collection: bool = False,
        **kwargs: Any,
    ) -> FseVector:
        if ids is None:
            ids = [str(uuid.uuid1()) for _ in texts]

        if not metadatas:
            metadatas = [{} for _ in texts]
        if fsedoc_connection_string is None:
            fsedoc_connection_string = cls.get_fsedoc_connection_string(kwargs)
        if fseaddr_connection_string is None:
            fseaddr_connection_string = cls.get_fseaddr_connection_string(kwargs)

        store = cls(
            fsedoc_connection_string=fsedoc_connection_string,
            fseaddr_connection_string=fseaddr_connection_string,
            collection_name=collection_name,
            embedding_function=embedding,
            distance_strategy=distance_strategy,
            pre_delete_collection=pre_delete_collection,
            **kwargs,
        )

        store.add_embeddings(
            texts=texts, embeddings=embeddings, metadatas=metadatas, ids=ids, **kwargs
        )

        return store

    def remove_surrogates(self, text):
        return re.sub(r'[\ud800-\udfff]', '', text)

    def remove_null(self, text):
        return text.replace('\x00', '')

    def add_embeddings(
        self,
        texts: Iterable[str],
        embeddings: List[List[float]],
        metadatas: Optional[List[dict]] = None,
        ids: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> List[str]:
        if ids is None:
            ids = [str(uuid.uuid1()) for _ in texts]

        if not metadatas:
            metadatas = [{} for _ in texts]

        for text, metadata, text_embedding, id in zip(texts, metadatas, embeddings, ids):
            key_list = self.get_key_list_string(metadata)
            text = self.remove_surrogates(text)
            text = self.remove_null(text)
            metadata_json = json.dumps(metadata)
            if len(key_list) != 0:
                key_embeddings = self.embedding_function.embed_documents(key_list)
                self.fsedoc.add_doc(id, text, text_embedding, metadata_json, key_list, key_embeddings)
            else:
                self.fsedoc.add_doc(id, text, text_embedding, metadata_json)

        return ids

    def add_texts(
        self,
        texts: Iterable[str],
        metadatas: Optional[List[dict]] = None,
        ids: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> List[str]:
        """Run more texts through the embeddings and add to the vectorstore.

        Args:
            texts: Iterable of strings to add to the vectorstore.
            metadatas: Optional list of metadatas associated with the texts.
            kwargs: vectorstore specific parameters

        Returns:
            List of ids from adding the texts into the vectorstore.
        """
        embeddings = self.embedding_function.embed_documents(list(texts))
        return self.add_embeddings(
            texts=texts, embeddings=embeddings, metadatas=metadatas, ids=ids, **kwargs
        )

    def similarity_search(
        self,
        query: str,
        k: int = 4,
        filter: Optional[dict] = None,
        **kwargs: Any,
    ) -> List[Document]:
        """Run similarity search with FseVector with distance.

        Args:
            query (str): Query text to search for.
            k (int): Number of results to return. Defaults to 4.
            filter (Optional[Dict[str, str]]): Filter by metadata. Defaults to None.

        Returns:
            List of Documents most similar to the query.
        """
        embedding = self.embedding_function.embed_query(text=query)
        return self.similarity_search_by_vector(
            embedding=embedding,
            k=k,
            filter=filter,
        )

    def similarity_search_with_score(
        self,
        query: str,
        k: int = 4,
        filter: Optional[dict] = None,
    ) -> List[Tuple[Document, float]]:
        """Return docs most similar to query.

        Args:
            query: Text to look up documents similar to.
            k: Number of Documents to return. Defaults to 4.
            filter (Optional[Dict[str, str]]): Filter by metadata. Defaults to None.

        Returns:
            List of Documents most similar to the query and score for each.
        """
        embedding = self.embedding_function.embed_query(query)
        docs = self.similarity_search_with_score_by_vector(
            embedding=embedding, k=k, filter=filter
        )
        return docs

    @property
    def distance_strategy(self) -> Any:
        if self._distance_strategy == DistanceStrategy.EUCLIDEAN:
            return self.EmbeddingStore.embedding.l2_distance
        elif self._distance_strategy == DistanceStrategy.COSINE:
            return self.EmbeddingStore.embedding.cosine_distance
        elif self._distance_strategy == DistanceStrategy.MAX_INNER_PRODUCT:
            return self.EmbeddingStore.embedding.max_inner_product
        else:
            raise ValueError(
                f"Got unexpected value for distance: {self._distance_strategy}. "
                f"Should be one of {', '.join([ds.value for ds in DistanceStrategy])}."
            )

    def similarity_search_with_score_by_vector(
        self,
        embedding: List[float],
        k: int = 4,
        filter: Optional[dict] = None,
    ) -> List[Tuple[Document, float]]:
        results = self.fsedoc.search(embedding=embedding, type="fulltext", topk=k)

        return self._results_to_docs_and_scores(results)

    def _results_to_docs_and_scores(self, results: Dict) -> List[Tuple[Document, float]]:
        """Return docs and scores from results."""
        if results["errorcode"] != "ok":
            self.logger.error('_results_to_docs_and_scores get errorcode: %s', results["errorcode"])
            return []
        
        docs = [
            (
                Document(
                    page_content=result["content"],
                    metadata=json.loads(result["metadata"]),
                ),
                1 - result["similarity"] if self.embedding_function is not None else None,
            )
            for result in results["results"]
        ]
        return docs

    def similarity_search_by_vector(
        self,
        embedding: List[float],
        k: int = 4,
        filter: Optional[dict] = None,
        **kwargs: Any,
    ) -> List[Document]:
        """Return docs most similar to embedding vector.

        Args:
            embedding: Embedding to look up documents similar to.
            k: Number of Documents to return. Defaults to 4.
            filter (Optional[Dict[str, str]]): Filter by metadata. Defaults to None.

        Returns:
            List of Documents most similar to the query vector.
        """
        docs_and_scores = self.similarity_search_with_score_by_vector(
            embedding=embedding, k=k, filter=filter
        )
        return _results_to_docs(docs_and_scores)

    @classmethod
    def from_texts(
        cls: Type[FseVector],
        texts: List[str],
        embedding: Embeddings,
        metadatas: Optional[List[dict]] = None,
        collection_name: str = _LANGCHAIN_DEFAULT_COLLECTION_NAME,
        distance_strategy: DistanceStrategy = DEFAULT_DISTANCE_STRATEGY,
        ids: Optional[List[str]] = None,
        pre_delete_collection: bool = False,
        **kwargs: Any,
    ) -> FseVector:
        """
        Return VectorStore initialized from texts and embeddings.
        Postgres connection string is required
        "Either pass it as a parameter
        or set the PGVECTOR_CONNECTION_STRING environment variable.
        """
        embeddings = embedding.embed_documents(list(texts))

        return cls.__from(
            texts,
            embeddings,
            embedding,
            metadatas=metadatas,
            ids=ids,
            collection_name=collection_name,
            distance_strategy=distance_strategy,
            pre_delete_collection=pre_delete_collection,
            **kwargs,
        )

    @classmethod
    def from_embeddings(
        cls,
        text_embeddings: List[Tuple[str, List[float]]],
        embedding: Embeddings,
        metadatas: Optional[List[dict]] = None,
        collection_name: str = _LANGCHAIN_DEFAULT_COLLECTION_NAME,
        distance_strategy: DistanceStrategy = DEFAULT_DISTANCE_STRATEGY,
        ids: Optional[List[str]] = None,
        pre_delete_collection: bool = False,
        **kwargs: Any,
    ) -> FseVector:
        """Construct FseVector wrapper from raw documents and pre-
        generated embeddings.

        Return VectorStore initialized from documents and embeddings.
        Postgres connection string is required
        "Either pass it as a parameter
        or set the PGVECTOR_CONNECTION_STRING environment variable.

        Example:
            .. code-block:: python

                from langchain.vectorstores import FseVector
                from langchain.embeddings import OpenAIEmbeddings
                embeddings = OpenAIEmbeddings()
                text_embeddings = embeddings.embed_documents(texts)
                text_embedding_pairs = list(zip(texts, text_embeddings))
                faiss = FseVector.from_embeddings(text_embedding_pairs, embeddings)
        """
        texts = [t[0] for t in text_embeddings]
        embeddings = [t[1] for t in text_embeddings]

        return cls.__from(
            texts,
            embeddings,
            embedding,
            metadatas=metadatas,
            ids=ids,
            collection_name=collection_name,
            distance_strategy=distance_strategy,
            pre_delete_collection=pre_delete_collection,
            **kwargs,
        )

    @classmethod
    def from_index(
        cls: Type[FseVector],
        embedding: Embeddings,
        collection_name: str = _LANGCHAIN_DEFAULT_COLLECTION_NAME,
        distance_strategy: DistanceStrategy = DEFAULT_DISTANCE_STRATEGY,
        pre_delete_collection: bool = False,
        **kwargs: Any,
    ) -> FseVector:
        """
        Get instance of an existing FseVector store.This method will
        return the instance of the store without inserting any new
        embeddings
        """

        fsedoc_connection_string = cls.get_fsedoc_connection_string(kwargs)
        fseaddr_connection_string = cls.get_fseaddr_connection_string(kwargs)
        kwargs["fsedoc_connection_string"] = fsedoc_connection_string
        kwargs["fseaddr_connection_string"] = fseaddr_connection_string

        store = cls(
            fsedoc_connection_string=fsedoc_connection_string,
            fseaddr_connection_string=fseaddr_connection_string,
            collection_name=collection_name,
            embedding_function=embedding,
            distance_strategy=distance_strategy,
            pre_delete_collection=pre_delete_collection,
        )

        return store

    @classmethod
    def get_fsedoc_connection_string(cls, kwargs: Dict[str, Any]) -> str:
        fsedoc_connection_string: str = get_from_dict_or_env(
            data=kwargs,
            key="fsedoc_connection_string",
            env_key="FSEDOC_CONNECTION_STRING",
        )

        if not fsedoc_connection_string:
            raise ValueError(
                "Postgres connection string is required"
                "Either pass it as a parameter"
                "or set the FSEDOC_CONNECTION_STRING environment variable."
            )

        return fsedoc_connection_string

    @classmethod
    def get_fseaddr_connection_string(cls, kwargs: Dict[str, Any]) -> str:
        fseaddr_connection_string: str = get_from_dict_or_env(
            data=kwargs,
            key="fseaddr_connection_string",
            env_key="FSEADDR_CONNECTION_STRING",
        )

        if not fseaddr_connection_string:
            raise ValueError(
                "fse connection string is required"
                "Either pass it as a parameter"
                "or set the FSEADDR_CONNECTION_STRING environment variable."
            )

        return fseaddr_connection_string

    @classmethod
    def get_key_list_string(cls, metadata: Dict[str, Any]) -> list[str]:
        key_list = []
        if "key_list" in metadata and metadata["key_list"]:
            key_list = metadata["key_list"]

        return key_list

    def _select_relevance_score_fn(self) -> Callable[[float], float]:
        """
        The 'correct' relevance function
        may differ depending on a few things, including:
        - the distance / similarity metric used by the VectorStore
        - the scale of your embeddings (OpenAI's are unit normed. Many others are not!)
        - embedding dimensionality
        - etc.
        """
        if self.override_relevance_score_fn is not None:
            return self.override_relevance_score_fn

        # Default strategy is to rely on distance strategy provided
        # in vectorstore constructor
        if self._distance_strategy == DistanceStrategy.COSINE:
            return self._cosine_relevance_score_fn
        elif self._distance_strategy == DistanceStrategy.EUCLIDEAN:
            return self._euclidean_relevance_score_fn
        elif self._distance_strategy == DistanceStrategy.MAX_INNER_PRODUCT:
            return self._max_inner_product_relevance_score_fn
        else:
            raise ValueError(
                "No supported normalization function"
                f" for distance_strategy of {self._distance_strategy}."
                "Consider providing relevance_score_fn to PGVector constructor."
            )
