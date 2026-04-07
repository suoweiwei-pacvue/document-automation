"""ChromaDB vector store management."""

import logging
from typing import Optional

import chromadb
from langchain_chroma import Chroma
from langchain_core.documents import Document

from src.config import Settings
from src.rag.embeddings import get_embeddings

logger = logging.getLogger(__name__)


class VectorStoreManager:
    def __init__(self, settings: Settings):
        self.settings = settings
        self._store: Optional[Chroma] = None

    @property
    def store(self) -> Chroma:
        if self._store is None:
            embeddings = get_embeddings(self.settings)
            self._store = Chroma(
                collection_name=self.settings.chroma_collection_name,
                embedding_function=embeddings,
                persist_directory=str(self.settings.chroma_path),
            )
        return self._store

    def add_documents(
        self,
        documents: list[Document],
        batch_size: int = 100,
    ) -> int:
        """Add documents to the vector store in batches."""
        total = 0
        for i in range(0, len(documents), batch_size):
            batch = documents[i : i + batch_size]
            self.store.add_documents(batch)
            total += len(batch)
            logger.info("Indexed %d / %d documents", total, len(documents))
        return total

    def clear(self):
        """Delete the entire collection and recreate."""
        try:
            client = chromadb.PersistentClient(path=str(self.settings.chroma_path))
            client.delete_collection(self.settings.chroma_collection_name)
            self._store = None
            logger.info("Cleared vector store collection")
        except Exception as e:
            logger.warning("Failed to clear collection: %s", e)

    def clear_by_source(self, source_type: str):
        """Delete documents matching a specific source_type."""
        try:
            results = self.store.get(where={"source_type": source_type})
            ids = results["ids"]
            if ids:
                self.store.delete(ids=ids)
            logger.info("Cleared %d documents with source_type=%s", len(ids), source_type)
        except Exception as e:
            logger.warning("Failed to clear source_type=%s: %s", source_type, e)

    def get_stats(self) -> dict:
        """Return basic stats about the vector store."""
        try:
            count = self.store._collection.count()
            return {"total_documents": count}
        except Exception:
            return {"total_documents": 0}
