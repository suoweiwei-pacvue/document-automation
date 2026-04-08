"""Confluence source for fetching tech review and PRD documents."""

import logging
from typing import Optional

from atlassian import Confluence
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class ConfluencePage(BaseModel):
    page_id: str
    title: str
    content: str
    parent_id: Optional[str] = None
    source_type: str = "confluence"
    doc_type: str = "tech_review"  # "tech_review" or "prd"
    url: str = ""


class ConfluenceSource:
    def __init__(self, url: str, username: str, api_token: str):
        self.client = Confluence(
            url=url,
            username=username,
            password=api_token,
            cloud=True,
        )

    def collect_pages(
        self,
        root_page_id: str,
        doc_type: str = "tech_review",
    ) -> list[ConfluencePage]:
        """Fetch a page and all its descendants.

        Tries CQL ancestor query first; falls back to recursive
        get_page_child_by_type if CQL is unavailable (e.g. 500 error).
        """
        pages: list[ConfluencePage] = []

        self._fetch_and_append(root_page_id, doc_type, pages)

        cql_ok = self._collect_via_cql(root_page_id, doc_type, pages)
        if not cql_ok:
            logger.info(
                "CQL unavailable, falling back to recursive child-page traversal for %s",
                root_page_id,
            )
            self._collect_children_recursive(root_page_id, doc_type, pages)

        logger.info(
            "Collected %d Confluence pages (type=%s) under page %s",
            len(pages), doc_type, root_page_id,
        )
        return pages

    def _collect_via_cql(
        self,
        root_page_id: str,
        doc_type: str,
        pages: list[ConfluencePage],
    ) -> bool:
        """Try to collect descendant pages via CQL. Returns False if CQL fails."""
        start = 0
        limit = 50
        while True:
            try:
                results = self.client.cql(
                    f"ancestor = {root_page_id} and type = page",
                    start=start,
                    limit=limit,
                    expand="body.storage,version",
                )
            except Exception as e:
                logger.warning("CQL query failed for ancestor=%s: %s", root_page_id, e)
                return False

            items = results.get("results", [])
            if not items:
                break

            for item in items:
                content_obj = item.get("content", item)
                pid = str(content_obj.get("id", ""))
                if pid:
                    self._fetch_and_append(pid, doc_type, pages)

            total = results.get("totalSize", 0)
            start += limit
            if start >= total:
                break

        return True

    def _collect_children_recursive(
        self,
        page_id: str,
        doc_type: str,
        pages: list[ConfluencePage],
        max_depth: int = 5,
        depth: int = 0,
    ):
        """Fallback: recursively get child pages when CQL is unavailable."""
        if depth >= max_depth:
            return
        try:
            children = self.client.get_page_child_by_type(
                page_id, type="page", start=0, limit=100,
            )
        except Exception as e:
            logger.warning("Failed to get children of page %s: %s", page_id, e)
            return

        for child in children:
            child_id = str(child.get("id", ""))
            if child_id:
                self._fetch_and_append(child_id, doc_type, pages)
                self._collect_children_recursive(
                    child_id, doc_type, pages, max_depth, depth + 1,
                )

    def _fetch_and_append(
        self,
        page_id: str,
        doc_type: str,
        pages: list[ConfluencePage],
    ):
        try:
            page = self.client.get_page_by_id(
                page_id,
                expand="body.storage,version",
            )
        except Exception as e:
            logger.warning("Failed to fetch page %s: %s", page_id, e)
            return

        body_html = page.get("body", {}).get("storage", {}).get("value", "")
        title = page.get("title", "")
        web_url = (
            page.get("_links", {}).get("base", "")
            + page.get("_links", {}).get("webui", "")
        )

        content = _html_to_text(body_html)

        if content.strip():
            pages.append(ConfluencePage(
                page_id=str(page_id),
                title=title,
                content=content,
                doc_type=doc_type,
                url=web_url,
            ))


def _html_to_text(html: str) -> str:
    """Simple HTML to text conversion; strips tags for RAG indexing."""
    import re
    text = re.sub(r"<br\s*/?>", "\n", html)
    text = re.sub(r"</?p[^>]*>", "\n", text)
    text = re.sub(r"</?li[^>]*>", "\n- ", text)
    text = re.sub(r"</?(?:h[1-6])[^>]*>", "\n## ", text)
    text = re.sub(r"</?tr[^>]*>", "\n", text)
    text = re.sub(r"</?td[^>]*>", " | ", text)
    text = re.sub(r"</?th[^>]*>", " | ", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"&nbsp;", " ", text)
    text = re.sub(r"&amp;", "&", text)
    text = re.sub(r"&lt;", "<", text)
    text = re.sub(r"&gt;", ">", text)
    text = re.sub(r"&#\d+;", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()
