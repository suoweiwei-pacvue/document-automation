"""CLI entry point for document-automation."""

import logging
import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.logging import RichHandler
from rich.progress import Progress, SpinnerColumn, TextColumn

from src.config import INDEXABLE_SOURCES, MODULE_DEFINITIONS, Settings, SourceType

app = typer.Typer(
    name="document-automation",
    help="基于 RAG + LangChain 的知识库文档自动生成工具",
)
console = Console()


def _setup_logging(verbose: bool = False):
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(message)s",
        handlers=[RichHandler(console=console, rich_tracebacks=True)],
    )


def _get_settings() -> Settings:
    env_path = Path(".env")
    if not env_path.exists():
        console.print("[red]Error: .env file not found. Copy .env.example to .env and fill in your keys.[/red]")
        raise typer.Exit(1)
    return Settings()


def _expand_source(source: Optional[SourceType]) -> list[str]:
    """Expand a SourceType value into a list of indexable source keys."""
    if source is None or source == SourceType.ALL:
        return list(INDEXABLE_SOURCES)
    if source == SourceType.CONFLUENCE:
        return [SourceType.CONFLUENCE_TECH.value, SourceType.CONFLUENCE_PRD.value]
    return [source.value]


@app.command()
def index(
    source: Optional[SourceType] = typer.Option(
        None,
        help="Index specific source: backend, frontend, confluence-tech, confluence-prd, confluence (both), or all (default)",
    ),
    clear: bool = typer.Option(False, help="Clear existing index before indexing"),
    verbose: bool = typer.Option(False, "--verbose", "-v"),
):
    """Index data sources into the vector store."""
    _setup_logging(verbose)
    settings = _get_settings()

    from src.rag.vectorstore import VectorStoreManager
    store = VectorStoreManager(settings)

    if clear:
        console.print("[yellow]Clearing existing index...[/yellow]")
        store.clear()

    sources_to_index = _expand_source(source)

    if source and source != SourceType.ALL and not clear:
        for st in sources_to_index:
            console.print(f"[yellow]Clearing old {st} index...[/yellow]")
            store.clear_by_source(st)

    with Progress(
        SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console,
    ) as progress:

        if SourceType.BACKEND.value in sources_to_index:
            task = progress.add_task("Indexing backend code...", total=None)
            docs = _index_backend(settings)
            count = store.add_documents(docs)
            progress.update(task, description=f"Backend: indexed {count} documents")

        if SourceType.FRONTEND.value in sources_to_index:
            task = progress.add_task("Indexing frontend code...", total=None)
            docs = _index_frontend(settings)
            count = store.add_documents(docs)
            progress.update(task, description=f"Frontend: indexed {count} documents")

        if SourceType.CONFLUENCE_TECH.value in sources_to_index:
            task = progress.add_task("Indexing Confluence tech docs...", total=None)
            docs = _index_confluence_tech(settings)
            count = store.add_documents(docs)
            progress.update(task, description=f"Confluence-tech: indexed {count} documents")

        if SourceType.CONFLUENCE_PRD.value in sources_to_index:
            task = progress.add_task("Indexing Confluence PRD docs...", total=None)
            docs = _index_confluence_prd(settings)
            count = store.add_documents(docs)
            progress.update(task, description=f"Confluence-prd: indexed {count} documents")

    stats = store.get_stats()
    console.print(f"\n[green]Indexing complete. Total documents: {stats['total_documents']}[/green]")


@app.command()
def generate(
    module: Optional[str] = typer.Option(
        None, help="Generate docs for specific module (e.g., core-api). Default: all modules.",
    ),
    skip_verify: bool = typer.Option(False, help="Skip verification step"),
    skip_diagrams: bool = typer.Option(False, help="Skip diagram generation"),
    verbose: bool = typer.Option(False, "--verbose", "-v"),
):
    """Generate knowledge base documentation."""
    _setup_logging(verbose)
    settings = _get_settings()

    from src.chains.diagram_generator import generate_diagrams, inject_diagrams
    from src.chains.doc_generator import generate_module_doc
    from src.chains.module_scanner import scan_module
    from src.chains.verifier import apply_corrections, verify_document
    from src.output.writer import write_index, write_module_doc
    from src.rag.retriever import MultiSourceRetriever
    from src.rag.vectorstore import VectorStoreManager

    store = VectorStoreManager(settings)
    stats = store.get_stats()
    if stats["total_documents"] == 0:
        console.print("[red]Vector store is empty. Run 'index' command first.[/red]")
        raise typer.Exit(1)

    retriever = MultiSourceRetriever(store)

    if module:
        modules_to_generate = [module]
        if module not in MODULE_DEFINITIONS:
            console.print(f"[red]Unknown module: {module}[/red]")
            console.print(f"Available modules: {', '.join(MODULE_DEFINITIONS.keys())}")
            raise typer.Exit(1)
    else:
        modules_to_generate = list(MODULE_DEFINITIONS.keys())

    generated: list[str] = []

    for mod_key in modules_to_generate:
        console.print(f"\n[bold blue]{'='*60}[/bold blue]")
        console.print(f"[bold]Generating: {MODULE_DEFINITIONS[mod_key]['title']}[/bold]")
        console.print(f"[bold blue]{'='*60}[/bold blue]")

        try:
            console.print("  [dim]Step 1/4: Scanning module...[/dim]")
            skeleton = scan_module(mod_key, retriever, settings)

            console.print("  [dim]Step 2/4: Generating documentation...[/dim]")
            doc_content = generate_module_doc(mod_key, skeleton, retriever, settings)

            if not skip_diagrams:
                console.print("  [dim]Step 3/4: Generating diagrams...[/dim]")
                diagrams = generate_diagrams(doc_content[:3000], settings)
                doc_content = inject_diagrams(doc_content, diagrams)
            else:
                console.print("  [dim]Step 3/4: Skipping diagrams[/dim]")

            accuracy = -1
            if not skip_verify:
                console.print("  [dim]Step 4/4: Verifying...[/dim]")
                verification = verify_document(doc_content, mod_key, retriever, settings)
                accuracy = verification.get("accuracy_score", -1)
                doc_content = apply_corrections(doc_content, verification)
            else:
                console.print("  [dim]Step 4/4: Skipping verification[/dim]")

            filepath = write_module_doc(mod_key, doc_content, settings, accuracy)
            generated.append(mod_key)
            console.print(f"  [green]Done: {filepath}[/green]")

        except Exception as e:
            console.print(f"  [red]Error generating {mod_key}: {e}[/red]")
            logging.exception("Failed to generate %s", mod_key)

    if generated:
        write_index(settings, generated)
        console.print(f"\n[bold green]Successfully generated {len(generated)} module documents.[/bold green]")
    else:
        console.print("\n[yellow]No documents were generated.[/yellow]")


@app.command()
def list_modules():
    """List all available documentation modules."""
    console.print("\n[bold]Available modules:[/bold]\n")
    for key, mod in MODULE_DEFINITIONS.items():
        console.print(f"  [cyan]{key:20s}[/cyan] {mod['id']} - {mod['title']}")
    console.print(f"\n  Total: {len(MODULE_DEFINITIONS)} modules")


@app.command()
def stats(verbose: bool = typer.Option(False, "--verbose", "-v")):
    """Show vector store statistics."""
    _setup_logging(verbose)
    settings = _get_settings()

    from src.rag.vectorstore import VectorStoreManager
    store = VectorStoreManager(settings)
    s = store.get_stats()
    console.print(f"\n[bold]Vector Store Stats:[/bold]")
    console.print(f"  Total documents: {s['total_documents']}")
    console.print(f"  Persist dir: {settings.chroma_persist_dir}")
    console.print(f"  Collection: {settings.chroma_collection_name}")


def _index_backend(settings: Settings):
    from src.parsing.chunker import chunk_backend_files
    from src.sources.github_source import BACKEND_EXTENSIONS, GitHubSource
    gh = GitHubSource(
        token=settings.github_token,
        owner=settings.github_owner,
        repo=settings.github_repo_backend,
        branch=settings.github_backend_branch,
    )
    files = gh.collect_files(extensions=BACKEND_EXTENSIONS, source_type="backend")
    return chunk_backend_files(files)


def _index_frontend(settings: Settings):
    from src.parsing.chunker import chunk_frontend_files
    from src.sources.github_source import GitHubSource
    gh = GitHubSource(
        token=settings.github_token,
        owner=settings.github_owner,
        repo=settings.github_repo_frontend,
        branch=settings.github_frontend_branch,
    )
    files = gh.collect_files()
    return chunk_frontend_files(files)


def _get_confluence_source(settings: Settings):
    from src.sources.confluence_source import ConfluenceSource
    return ConfluenceSource(
        url=settings.confluence_url,
        username=settings.confluence_username,
        api_token=settings.confluence_api_token,
    )


def _index_confluence_tech(settings: Settings):
    from src.parsing.chunker import chunk_confluence_pages
    conf = _get_confluence_source(settings)
    pages = []
    for page_id in settings.confluence_tech_page_ids:
        pages.extend(conf.collect_pages(page_id, doc_type="tech_review"))
    return chunk_confluence_pages(pages)


def _index_confluence_prd(settings: Settings):
    from src.parsing.chunker import chunk_confluence_pages
    conf = _get_confluence_source(settings)
    pages = []
    for page_id in settings.confluence_prd_page_ids:
        pages.extend(conf.collect_pages(page_id, doc_type="prd"))
    return chunk_confluence_pages(pages)


if __name__ == "__main__":
    app()
