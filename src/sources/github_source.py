"""GitHub source for fetching frontend code via GitHub API."""

import base64
import logging
from typing import Optional

from github import Github, GithubException
from pydantic import BaseModel

logger = logging.getLogger(__name__)

FRONTEND_EXTENSIONS = {".vue", ".js", ".ts", ".jsx", ".tsx", ".scss", ".css", ".json"}
SKIP_DIRS = {"node_modules", "dist", ".git", "coverage", ".husky"}


class GitHubFile(BaseModel):
    path: str
    content: str
    file_type: str  # "vue", "js", "ts", "scss", "json"
    source_type: str = "frontend"
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
    ) -> list[GitHubFile]:
        """Fetch files from the GitHub repository."""
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
            if ext not in FRONTEND_EXTENSIONS:
                continue

            if target_dirs and "*" not in target_dirs:
                top_dir = item.path.split("/")[0] if "/" in item.path else ""
                if top_dir and top_dir not in target_dirs and item.path not in target_dirs:
                    continue

            if item.size and item.size > max_file_size:
                logger.warning("Skipping large file %s (%d bytes)", item.path, item.size)
                continue

            content = self._fetch_content(item.path)
            if content is not None:
                file_type = ext.lstrip(".")
                files.append(GitHubFile(
                    path=item.path,
                    content=content,
                    file_type=file_type,
                    size=item.size or len(content),
                ))

        logger.info("Collected %d frontend files from GitHub", len(files))
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
