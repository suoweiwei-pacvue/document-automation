# document-automation 进度记录

## 项目概述
基于 Python + LangChain + RAG 自动生成 Custom Dashboard 知识库文档的独立工具项目。
位置: `/Users/wei/code/ai/document-automation`

## 已完成

### Phase 1: 项目骨架 + 数据采集层
- [x] 项目目录结构 (Harness 风格)
- [x] `requirements.txt` + `.env.example` + `.gitignore`
- [x] `README.md` + `ARCHITECTURE.md` + `AGENTS.md`
- [x] `src/config.py` - 配置管理，含 14 个模块定义
- [x] `src/sources/local_source.py` - 本地后端代码读取
- [x] `src/sources/github_source.py` - GitHub API 前端代码拉取
- [x] `src/sources/confluence_source.py` - Confluence 文档拉取

### Phase 2: 解析 + 向量化
- [x] `src/parsing/java_parser.py` - Java 代码语义解析（class/method 级别）
- [x] `src/parsing/vue_parser.py` - Vue SFC / JS 文件解析
- [x] `src/parsing/markdown_parser.py` - Confluence 文档按 heading 切分
- [x] `src/parsing/chunker.py` - 统一 chunker，输出 LangChain Document
- [x] `src/rag/embeddings.py` - OpenAI Embeddings 配置
- [x] `src/rag/vectorstore.py` - ChromaDB 管理
- [x] `src/rag/retriever.py` - 多源检索器 (含 source_type 过滤)

### Phase 3: 文档生成链
- [x] `src/chains/module_scanner.py` - 模块扫描生成骨架
- [x] `src/chains/doc_generator.py` - 文档生成（四源融合）
- [x] `src/chains/diagram_generator.py` - Mermaid 流程图
- [x] `src/chains/verifier.py` - 交叉验证
- [x] `prompts/` 4 个 Prompt 模板

### Phase 4: CLI + 输出
- [x] `src/main.py` - Typer CLI (index/generate/list-modules/stats)
- [x] `src/output/writer.py` - MD 文件输出 + 索引生成
- [x] `src/templates/module_doc.md.j2` - Jinja2 文档模板
- [x] 单元测试 8/8 通过
- [x] 端到端验证：后端代码解析 273 files → 340 chunks

### Phase 5: Harness 文档 + Cursor Skill
- [x] `docs/design-docs/` - 设计文档
- [x] `docs/exec-plans/` - 执行计划模板
- [x] Cursor Skill 创建 (`~/.cursor/skills/document-automation/SKILL.md`)

### Phase 6: Figma 数据源集成
- [x] `src/sources/figma_source.py` - Figma REST API 采集（文件树遍历 + 评论）
- [x] `src/config.py` - 新增 SourceType.FIGMA + Settings figma 配置字段
- [x] `src/parsing/chunker.py` - 新增 chunk_figma_nodes 分块函数
- [x] `src/main.py` - 新增 _index_figma + CLI index 命令接入
- [x] `src/rag/retriever.py` - retrieve_for_module 追加 figma 查询组
- [x] `src/chains/doc_generator.py` - 文档生成融合 Figma 设计上下文
- [x] `prompts/generate_doc.txt` - Prompt 模板增加 Figma 设计稿部分
- [x] `.env.example` / `requirements.txt` / `check_config.py` 更新
- [x] 单元测试新增 Figma 相关测试用例
- [x] README.md / ARCHITECTURE.md / SKILL.md / writer.py 文档更新

## 使用说明

```bash
cd /Users/wei/code/ai/document-automation
source .venv/bin/activate
cp .env.example .env  # 填入 API keys

python -m src.main index        # 索引数据源
python -m src.main generate     # 生成全部文档
python -m src.main generate --module core-api  # 单模块
python -m src.main list-modules # 列出模块
```
