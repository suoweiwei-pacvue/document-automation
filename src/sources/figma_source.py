"""Figma source for fetching UI design data via Figma REST API."""

import logging
from typing import Optional

import requests
from pydantic import BaseModel

logger = logging.getLogger(__name__)

FIGMA_API_BASE = "https://api.figma.com/v1"

RELEVANT_NODE_TYPES = {
    "CANVAS", "FRAME", "COMPONENT", "COMPONENT_SET", "INSTANCE",
    "TEXT", "SECTION", "GROUP", "BOOLEAN_OPERATION", "VECTOR",
    "RECTANGLE", "ELLIPSE", "LINE", "STAR", "POLYGON",
}

STRUCTURE_TYPES = {"CANVAS", "FRAME", "COMPONENT", "COMPONENT_SET", "SECTION", "GROUP"}


class FigmaNode(BaseModel):
    file_key: str
    file_name: str = ""
    node_id: str
    name: str
    node_type: str
    page_name: str = ""
    content: str
    source_type: str = "figma"


class FigmaSource:
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.session = requests.Session()
        self.session.headers.update({
            "X-Figma-Token": access_token,
        })

    def collect_nodes(
        self,
        file_key: str,
        depth: Optional[int] = None,
    ) -> list[FigmaNode]:
        """Fetch all meaningful nodes from a Figma file.

        Calls GET /v1/files/:key to retrieve the full document tree,
        then recursively extracts text content, component structure,
        and page-level summaries.
        """
        params = {}
        if depth is not None:
            params["depth"] = depth

        try:
            resp = self.session.get(
                f"{FIGMA_API_BASE}/files/{file_key}",
                params=params,
                timeout=120,
            )
            resp.raise_for_status()
        except requests.RequestException as e:
            logger.error("Failed to fetch Figma file %s: %s", file_key, e)
            return []

        data = resp.json()
        file_name = data.get("name", file_key)
        document = data.get("document", {})
        pages = document.get("children", [])

        nodes: list[FigmaNode] = []
        for page in pages:
            page_name = page.get("name", "")
            page_nodes = self._extract_page(page, file_key, file_name, page_name)
            nodes.extend(page_nodes)

        logger.info(
            "Collected %d nodes from Figma file %s (%s, %d pages)",
            len(nodes), file_key, file_name, len(pages),
        )
        return nodes

    def collect_comments(self, file_key: str) -> list[FigmaNode]:
        """Fetch comments from a Figma file via GET /v1/files/:key/comments."""
        try:
            resp = self.session.get(
                f"{FIGMA_API_BASE}/files/{file_key}/comments",
                timeout=30,
            )
            resp.raise_for_status()
        except requests.RequestException as e:
            logger.warning("Failed to fetch comments for %s: %s", file_key, e)
            return []

        data = resp.json()
        comments = data.get("comments", [])

        nodes: list[FigmaNode] = []
        for comment in comments:
            message = comment.get("message", "").strip()
            if not message:
                continue

            user = comment.get("user", {}).get("handle", "unknown")
            node_id = comment.get("client_meta", {}).get("node_id", "")
            resolved = comment.get("resolved_at") is not None

            content_parts = [
                f"Comment by {user}:",
                message,
            ]
            if resolved:
                content_parts.append("[RESOLVED]")

            nodes.append(FigmaNode(
                file_key=file_key,
                node_id=node_id or comment.get("id", ""),
                name=f"Comment: {message[:60]}",
                node_type="COMMENT",
                content="\n".join(content_parts),
            ))

        logger.info("Collected %d comments from Figma file %s", len(nodes), file_key)
        return nodes

    def _extract_page(
        self,
        page: dict,
        file_key: str,
        file_name: str,
        page_name: str,
    ) -> list[FigmaNode]:
        """Extract nodes from a single Figma page (CANVAS)."""
        nodes: list[FigmaNode] = []

        page_summary = self._build_page_summary(page)
        if page_summary:
            nodes.append(FigmaNode(
                file_key=file_key,
                file_name=file_name,
                node_id=page.get("id", ""),
                name=page_name,
                node_type="CANVAS",
                page_name=page_name,
                content=page_summary,
            ))

        self._walk_children(page, file_key, file_name, page_name, nodes, depth=0)
        return nodes

    def _walk_children(
        self,
        node: dict,
        file_key: str,
        file_name: str,
        page_name: str,
        nodes: list[FigmaNode],
        depth: int,
        parent_path: str = "",
    ):
        """Recursively walk the node tree and extract meaningful content."""
        children = node.get("children", [])
        for child in children:
            child_type = child.get("type", "")
            child_name = child.get("name", "")
            current_path = f"{parent_path}/{child_name}" if parent_path else child_name

            if child_type == "TEXT":
                text = child.get("characters", "").strip()
                if text and len(text) > 2:
                    nodes.append(FigmaNode(
                        file_key=file_key,
                        file_name=file_name,
                        node_id=child.get("id", ""),
                        name=current_path,
                        node_type="TEXT",
                        page_name=page_name,
                        content=text,
                    ))

            elif child_type in ("FRAME", "COMPONENT", "COMPONENT_SET", "SECTION"):
                summary = self._build_frame_summary(child, current_path)
                if summary:
                    nodes.append(FigmaNode(
                        file_key=file_key,
                        file_name=file_name,
                        node_id=child.get("id", ""),
                        name=current_path,
                        node_type=child_type,
                        page_name=page_name,
                        content=summary,
                    ))

            if child_type in STRUCTURE_TYPES and depth < 8:
                self._walk_children(
                    child, file_key, file_name, page_name,
                    nodes, depth + 1, current_path,
                )

    def _build_page_summary(self, page: dict) -> str:
        """Build a text summary for an entire page."""
        name = page.get("name", "Untitled")
        children = page.get("children", [])

        parts = [f"Figma Page: {name}"]
        parts.append(f"Top-level frames ({len(children)}):")
        for child in children[:50]:
            child_type = child.get("type", "")
            child_name = child.get("name", "")
            parts.append(f"  - [{child_type}] {child_name}")

        return "\n".join(parts)

    def _build_frame_summary(self, node: dict, path: str) -> str:
        """Build a text summary for a frame/component node."""
        children = node.get("children", [])
        if not children:
            return ""

        texts = _collect_texts(node, max_depth=4)
        child_names = [c.get("name", "") for c in children[:20]]

        parts = [f"[{node.get('type', 'FRAME')}] {path}"]

        if texts:
            parts.append("Text content:")
            for t in texts[:30]:
                parts.append(f"  {t}")

        if child_names:
            parts.append(f"Children ({len(children)}):")
            for cn in child_names:
                parts.append(f"  - {cn}")

        summary = "\n".join(parts)
        if len(summary) > 4000:
            summary = summary[:4000] + "\n... (truncated)"
        return summary


def _collect_texts(node: dict, max_depth: int = 4, current_depth: int = 0) -> list[str]:
    """Recursively collect all TEXT node characters from a subtree."""
    if current_depth > max_depth:
        return []

    texts: list[str] = []
    if node.get("type") == "TEXT":
        chars = node.get("characters", "").strip()
        if chars and len(chars) > 1:
            texts.append(chars)

    for child in node.get("children", []):
        texts.extend(_collect_texts(child, max_depth, current_depth + 1))

    return texts
