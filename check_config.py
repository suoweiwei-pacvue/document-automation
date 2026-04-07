"""Configuration and connectivity checker."""

import logging
import sys
from pathlib import Path

logging.getLogger("LiteLLM").setLevel(logging.WARNING)
logging.getLogger("litellm").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)


def main():
    print("=== document-automation 配置检查 ===\n")

    from src.config import Settings
    s = Settings()
    all_ok = True

    # 1. OpenAI
    key = s.openai_api_key
    ok = bool(key and len(key) > 10)
    print(f"1. OPENAI_API_KEY: {key[:8]}...{key[-4:]} ({len(key)} chars) {'✅' if ok else '❌'}")
    print(f"   LLM_MODEL: {s.llm_model} | EMBEDDING: {s.embedding_model}")
    all_ok &= ok

    # 2. GitHub Token
    gt = s.github_token
    ok = bool(gt and len(gt) > 10)
    print(f"\n2. GITHUB_TOKEN: {gt[:8]}...{gt[-4:]} ({len(gt)} chars) {'✅' if ok else '❌'}")
    all_ok &= ok

    # 3. Local backend
    exists = Path(s.local_backend_path).is_dir()
    print(f"\n3. LOCAL_BACKEND_PATH: {s.local_backend_path} {'✅' if exists else '❌'}")
    all_ok &= exists

    # 4. Confluence
    ct = s.confluence_api_token
    ok = bool(ct and len(ct) > 5)
    print(f"\n4. CONFLUENCE_API_TOKEN: {ct[:8]}...{ct[-4:]} ({len(ct)} chars) {'✅' if ok else '❌'}" if ok else f"\n4. CONFLUENCE_API_TOKEN: ❌ 未设置")
    all_ok &= ok

    print("\n" + "=" * 50)
    print("=== 连通性测试 ===\n")

    # Test 1: Local backend
    from src.sources.local_source import collect_files
    files = collect_files(Path(s.local_backend_path), modules=["custom-dashboard-api"])
    java_count = sum(1 for f in files if f.file_type == "java")
    print(f"1. 本地后端: {len(files)} 文件 (Java {java_count}) ✅")

    # Test 2: GitHub
    print("2. GitHub: 连接中...", end=" ", flush=True)
    try:
        from src.sources.github_source import GitHubSource
        gh = GitHubSource(s.github_token, s.github_owner, s.github_repo_frontend, s.github_branch)
        repo = gh.repo
        print(f"\n   {repo.full_name} (stars: {repo.stargazers_count}) ✅")
    except Exception as e:
        print(f"\n   ❌ {e}")
        all_ok = False

    # Test 3: Confluence
    print("3. Confluence: 连接中...", end=" ", flush=True)
    try:
        from src.sources.confluence_source import ConfluenceSource
        conf = ConfluenceSource(s.confluence_url, s.confluence_username, s.confluence_api_token)
        page = conf.client.get_page_by_id(s.confluence_tech_page_id, expand="version")
        print(f'\n   技术文档: "{page["title"]}" ✅')
        page2 = conf.client.get_page_by_id(s.confluence_prd_page_id, expand="version")
        print(f'   PRD 文档: "{page2["title"]}" ✅')
    except Exception as e:
        print(f"\n   ❌ {e}")
        all_ok = False

    # Test 4: OpenAI Embedding
    print("4. OpenAI Embedding: 连接中...", end=" ", flush=True)
    try:
        from src.rag.embeddings import get_embeddings
        emb = get_embeddings(s)
        result = emb.embed_query("test connection")
        print(f"\n   向量维度: {len(result)} ✅")
    except Exception as e:
        print(f"\n   ❌ {e}")
        all_ok = False

    print("\n" + "=" * 50)
    if all_ok:
        print("🎉 全部通过！可以开始运行:")
        print("   python -m src.main index")
        print("   python -m src.main generate")
    else:
        print("⚠️  部分检查未通过，请修复后重试。")

    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
