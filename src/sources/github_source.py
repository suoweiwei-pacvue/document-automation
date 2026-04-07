"""GitHub source for fetching code via GitHub API (frontend and backend)."""

import base64
import logging
from typing import Optional

from github import Github, GithubException
from pydantic import BaseModel

logger = logging.getLogger(__name__)

FRONTEND_EXTENSIONS = {".vue", ".js", ".ts", ".jsx", ".tsx", ".scss", ".css", ".json"}
BACKEND_EXTENSIONS = {".java", ".xml", ".yml", ".yaml", ".properties", ".sql"}
SKIP_DIRS = {"node_modules", "dist", ".git", "coverage", ".husky", "target", "build", ".idea", ".gradle"}


class GitHubFile(BaseModel):
    path: str
    content: str
    file_type: str
    source_type: str = "frontend"
    module: str = ""
    size: int = 0


class GitHubSource:
    def __init__(self, token: str, owner: str, repo: str, branch: str = "master"):
        self.gh = Github(token)
        self.owner = owner
        self.repo_name = repo
        self.branch = branch
        self._repo = None

    @property
    def repo(self):
        if self._repo is None:
            self._repo = self.gh.get_repo(f"{self.owner}/{self.repo_name}")
        return self._repo

    def collect_files(
        self,
        target_dirs: Optional[list[str]] = None,
        max_file_size: int = 200_000,
        extensions: Optional[set[str]] = None,
        source_type: str = "frontend",
    ) -> list[GitHubFile]:
        """Fetch files from the GitHub repository.

        Args:
            target_dirs: Only include files under these top-level directories.
            max_file_size: Skip files larger than this (bytes).
            extensions: File extensions to include. Defaults to FRONTEND_EXTENSIONS.
            source_type: Tag for metadata ("frontend" or "backend").
        """
        if extensions is None:
            extensions = FRONTEND_EXTENSIONS

        files: list[GitHubFile] = []
        try:
            tree = self.repo.get_git_tree(self.branch, recursive=True)
        except GithubException as e:
            logger.error("Failed to get repo tree: %s", e)
            return files

        for item in tree.tree:
            if item.type != "blob":
                continue
            if any(skip in item.path.split("/") for skip in SKIP_DIRS):
                continue

            ext = "." + item.path.rsplit(".", 1)[-1] if "." in item.path else ""
            if ext not in extensions:
                continue

            if target_dirs and "*" not in target_dirs:
                top_dir = item.path.split("/")[0] if "/" in item.path else ""
                if top_dir and top_dir not in target_dirs and item.path not in target_dirs:
                    continue

            if item.size and item.size > max_file_size:
                logger.warning("Skipping large file %s (%d bytes)", item.path, item.size)
                continue

            module = _extract_module(item.path) if source_type == "backend" else ""

            content = self._fetch_content(item.path)
            if content is not None:
                file_type = _classify_file_type(ext)
                files.append(GitHubFile(
                    path=item.path,
                    content=content,
                    file_type=file_type,
                    source_type=source_type,
                    module=module,
                    size=item.size or len(content),
                ))

        logger.info("Collected %d %s files from GitHub (%s/%s@%s)",
                     len(files), source_type, self.owner, self.repo_name, self.branch)
        return files

    def _fetch_content(self, path: str) -> Optional[str]:
        try:
            content_file = self.repo.get_contents(path, ref=self.branch)
            if content_file.encoding == "base64":
                return base64.b64decode(content_file.content).decode("utf-8", errors="replace")
            return content_file.decoded_content.decode("utf-8", errors="replace")
        except GithubException as e:
            logger.warning("Failed to fetch %s: %s", path, e)
            return None
        except Exception as e:
            logger.warning("Error decoding %s: %s", path, e)
            return None


def _extract_module(path: str) -> str:
    """Extract Maven module name from file path (first directory level)."""
    parts = path.split("/")
    if len(parts) >= 2:
        return parts[0]
    return "root"


def _classify_file_type(ext: str) -> str:
    ext = ext.lstrip(".")
    mapping = {
        "java": "java",
        "xml": "pom" if ext == "xml" else "resource",
        "yml": "resource",
        "yaml": "resource",
        "properties": "resource",
        "sql": "sql",
    }
    return mapping.get(ext, ext)
