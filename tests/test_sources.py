"""Tests for data sources."""

from pathlib import Path

from src.sources.local_source import collect_files


def test_collect_backend_files():
    """Test that local source can collect files from the backend project."""
    backend_path = Path("/Users/wei/code/pacvue/custom-dashboard")
    if not backend_path.exists():
        return  # skip if backend not available

    files = collect_files(backend_path, modules=["custom-dashboard-api"])
    assert len(files) > 0

    java_files = [f for f in files if f.file_type == "java"]
    assert len(java_files) > 0

    for f in java_files[:3]:
        assert f.source_type == "backend"
        assert f.module == "custom-dashboard-api"
        assert f.content


def test_collect_nonexistent_path():
    files = collect_files(Path("/nonexistent/path"))
    assert len(files) == 0
