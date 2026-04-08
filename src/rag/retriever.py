"""Multi-source retriever with source_type filtering."""

import logging
from typing import Optional

from langchain_core.documents import Document

from src.rag.vectorstore import VectorStoreManager

logger = logging.getLogger(__name__)


class MultiSourceRetriever:
    """Retriever that supports filtering by source_type and keyword matching."""

    def __init__(self, store_manager: VectorStoreManager):
        self.store_manager = store_manager

    def retrieve(
        self,
        query: str,
        k: int = 20,
        source_types: Optional[list[str]] = None,
        module_filter: Optional[str] = None,
        doc_type_filter: Optional[str] = None,
    ) -> list[Document]:
        """Retrieve relevant documents with optional metadata filters."""
        where_filter = self._build_filter(source_types, module_filter, doc_type_filter)

        if where_filter:
            results = self.store_manager.store.similarity_search(
                query, k=k, filter=where_filter,
            )
        else:
            results = self.store_manager.store.similarity_search(query, k=k)

        logger.debug(
            "Retrieved %d docs for query='%s' (filters=%s)",
            len(results), query[:50], where_filter,
        )
        return results

    def retrieve_for_module(
        self,
        module_id: str,
        keywords: list[str],
        backend_modules: Optional[list[str]] = None,
        k_per_query: int = 10,
        max_total: int = 60,
    ) -> list[Document]:
        """Retrieve documents relevant to a specific documentation module.

        Runs multiple queries (one per keyword group) and merges results.
        """
        all_docs: list[Document] = []
        seen_contents: set[int] = set()

        query_groups = [
            (keywords[:3], None),
            (keywords[:3], ["backend"]),
            (keywords[:3], ["frontend"]),
            (keywords[:3], ["confluence"]),
            (keywords[:3], ["figma"]),
        ]

        for kw_group, source_types in query_groups:
            query = " ".join(kw_group)

            module_f = None
            if backend_modules and "*" not in backend_modules and source_types == ["backend"]:
                module_f = backend_modules[0] if len(backend_modules) == 1 else None

            docs = self.retrieve(
                query=query,
                k=k_per_query,
                source_types=source_types,
                module_filter=module_f,
            )

            for doc in docs:
                h = hash(doc.page_content[:200])
                if h not in seen_contents:
                    seen_contents.add(h)
                    all_docs.append(doc)

            if len(all_docs) >= max_total:
                break

        return all_docs[:max_total]

    def _build_filter(
        self,
        source_types: Optional[list[str]],
        module_filter: Optional[str],
        doc_type_filter: Optional[str],
    ) -> Optional[dict]:
        conditions = []

        if source_types and len(source_types) == 1:
            conditions.append({"source_type": {"$eq": source_types[0]}})
        elif source_types and len(source_types) > 1:
            conditions.append({"source_type": {"$in": source_types}})

        if module_filter:
            conditions.append({"module": {"$eq": module_filter}})

        if doc_type_filter:
            conditions.append({"doc_type": {"$eq": doc_type_filter}})

        if not conditions:
            return None
        if len(conditions) == 1:
            return conditions[0]
        return {"$and": conditions}
