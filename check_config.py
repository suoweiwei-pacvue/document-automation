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
    print(f"   Backend: {s.github_owner}/{s.github_repo_backend}@{s.github_backend_branch}")
    print(f"   Frontend: {s.github_owner}/{s.github_repo_frontend}@{s.github_frontend_branch}")
    all_ok &= ok

    # 3. Confluence
    ct = s.confluence_api_token
    ok = bool(ct and len(ct) > 5)
    print(f"\n3. CONFLUENCE_API_TOKEN: {ct[:8]}...{ct[-4:]} ({len(ct)} chars) {'✅' if ok else '❌'}" if ok else f"\n3. CONFLUENCE_API_TOKEN: ❌ 未设置")
    all_ok &= ok

    # 4. Figma
    ft = s.figma_access_token
    ok = bool(ft and len(ft) > 5)
    print(f"\n4. FIGMA_ACCESS_TOKEN: {ft[:8]}...{ft[-4:]} ({len(ft)} chars) {'✅' if ok else '❌'}" if ok else f"\n4. FIGMA_ACCESS_TOKEN: ❌ 未设置")
    print(f"   File IDs: {s.figma_file_ids or '(none)'}")
    all_ok &= ok

    print("\n" + "=" * 50)
    print("=== 连通性测试 ===\n")

    # Test 1: GitHub Backend
    print("1. GitHub 后端代码: 连接中...", end=" ", flush=True)
    try:
        from src.sources.github_source import GitHubSource
        gh_be = GitHubSource(s.github_token, s.github_owner, s.github_repo_backend, s.github_backend_branch)
        repo_be = gh_be.repo
        print(f"\n   {repo_be.full_name}@{s.github_backend_branch} ✅")
    except Exception as e:
        print(f"\n   ❌ {e}")
        all_ok = False

    # Test 2: GitHub Frontend
    print("2. GitHub 前端代码: 连接中...", end=" ", flush=True)
    try:
        from src.sources.github_source import GitHubSource
        gh_fe = GitHubSource(s.github_token, s.github_owner, s.github_repo_frontend, s.github_frontend_branch)
        repo_fe = gh_fe.repo
        print(f"\n   {repo_fe.full_name}@{s.github_frontend_branch} ✅")
    except Exception as e:
        print(f"\n   ❌ {e}")
        all_ok = False

    # Test 3: Confluence
    print("3. Confluence: 连接中...", end=" ", flush=True)
    try:
        from src.sources.confluence_source import ConfluenceSource
        conf = ConfluenceSource(s.confluence_url, s.confluence_username, s.confluence_api_token)

        def _list_root_and_descendants(client, page_id, label):
            """List root page + all descendants. Falls back to recursive child traversal if CQL fails."""
            count = 0
            try:
                root = client.get_page_by_id(page_id, expand="version")
                print(f'\n   {label} [{page_id}]: "{root["title"]}" ✅')
                count += 1
            except Exception as e:
                print(f'\n   {label} [{page_id}]: ❌ {e}')
                return 0

            cql_ok = True
            start = 0
            limit = 50
            while True:
                try:
                    results = client.cql(
                        f"ancestor = {page_id} and type = page",
                        start=start, limit=limit,
                    )
                except Exception as e:
                    print(f'     ⚠️ CQL 查询失败，切换到递归模式: {e}')
                    cql_ok = False
                    break
                items = results.get("results", [])
                if not items:
                    break
                for item in items:
                    c = item.get("content", item)
                    title = c.get("title", "")
                    print(f'     └─ "{title}"')
                    count += 1
                total = results.get("totalSize", 0)
                start += limit
                if start >= total:
                    break

            if not cql_ok:
                count += _list_children_recursive(client, page_id, indent=5)

            return count

        def _list_children_recursive(client, page_id, indent=5, max_depth=5, depth=0):
            """Fallback: recursively list child pages."""
            if depth >= max_depth:
                return 0
            count = 0
            try:
                children = client.get_page_child_by_type(page_id, type="page", start=0, limit=100)
            except Exception as e:
                print(f'{" " * indent}⚠️ 获取子页面失败: {e}')
                return 0
            for child in children:
                title = child.get("title", "")
                print(f'{" " * indent}└─ "{title}"')
                count += 1
                child_id = str(child.get("id", ""))
                if child_id:
                    count += _list_children_recursive(client, child_id, indent + 2, max_depth, depth + 1)
            return count

        tech_count = 0
        for pid in s.confluence_tech_page_ids:
            tech_count += _list_root_and_descendants(conf.client, pid, "技术文档")
        prd_count = 0
        for pid in s.confluence_prd_page_ids:
            prd_count += _list_root_and_descendants(conf.client, pid, "PRD 文档")
        print(f'   共计: 技术文档 {tech_count} 页, PRD 文档 {prd_count} 页')
    except Exception as e:
        print(f"\n   ❌ {e}")
        all_ok = False

    # Test 4: Figma
    print("4. Figma: 连接中...", end=" ", flush=True)
    try:
        import requests as _req
        headers = {"X-Figma-Token": s.figma_access_token}
        for fid in s.figma_file_id_list:
            r = _req.get(
                f"https://api.figma.com/v1/files/{fid}?depth=2",
                headers=headers,
                timeout=120,
            )
            r.raise_for_status()
            fdata = r.json()
            fname = fdata.get("name", fid)
            pages = fdata.get("document", {}).get("children", [])
            print(f'\n   文件 [{fid}]: "{fname}" ({len(pages)} 页) ✅')
            for i, pg in enumerate(pages):
                pg_name = pg.get("name", "Untitled")
                pg_id = pg.get("id", "")
                children = pg.get("children", [])
                print(f'     {i+1:2d}. [{pg_id}] "{pg_name}" ({len(children)} frames)')
    except Exception as e:
        print(f"\n   ❌ {e}")
        all_ok = False

    # Test 5: OpenAI Embedding
    print("5. OpenAI Embedding: 连接中...", end=" ", flush=True)
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
