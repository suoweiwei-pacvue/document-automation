"""Tests for data sources."""

from src.sources.github_source import (
    BACKEND_EXTENSIONS,
    FRONTEND_EXTENSIONS,
    GitHubFile,
    _classify_file_type,
    _extract_module,
)


def test_extract_module_from_path():
    assert _extract_module("custom-dashboard-api/src/main/java/Foo.java") == "custom-dashboard-api"
    assert _extract_module("custom-dashboard-base/pom.xml") == "custom-dashboard-base"
    assert _extract_module("pom.xml") == "root"


def test_classify_file_type():
    assert _classify_file_type(".java") == "java"
    assert _classify_file_type(".yml") == "resource"
    assert _classify_file_type(".yaml") == "resource"
    assert _classify_file_type(".properties") == "resource"
    assert _classify_file_type(".sql") == "sql"
    assert _classify_file_type(".vue") == "vue"


def test_github_file_model():
    f = GitHubFile(
        path="custom-dashboard-api/src/Main.java",
        content="public class Main {}",
        file_type="java",
        source_type="backend",
        module="custom-dashboard-api",
    )
    assert f.source_type == "backend"
    assert f.module == "custom-dashboard-api"


def test_extensions_sets():
    assert ".java" in BACKEND_EXTENSIONS
    assert ".xml" in BACKEND_EXTENSIONS
    assert ".vue" in FRONTEND_EXTENSIONS
    assert ".java" not in FRONTEND_EXTENSIONS
