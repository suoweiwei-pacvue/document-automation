# Architecture

## 系统架构

```
┌─────────────────────────────────────────────────────────┐
│                     CLI (typer)                          │
│                   src/main.py                            │
├─────────────────────────────────────────────────────────┤
│                  Chains Layer                            │
│  module_scanner → doc_generator → diagram → verifier    │
├─────────────────────────────────────────────────────────┤
│                   RAG Layer                              │
│        embeddings / vectorstore / retriever              │
├─────────────────────────────────────────────────────────┤
│                 Parsing Layer                            │
│     java_parser / vue_parser / markdown_parser           │
├─────────────────────────────────────────────────────────┤
│                 Sources Layer                            │
│  local_source / github_source / confluence_source        │
│  figma_source                                            │
└─────────────────────────────────────────────────────────┘
```

## 数据流

1. **Sources** 从本地文件系统、GitHub API、Confluence API、Figma REST API 获取原始内容
2. **Parsing** 使用 tree-sitter（Java/JS）解析代码为语义块（class/method 级别）
3. **RAG** 将语义块向量化后存入 ChromaDB，每个块带有 `source_type` 元数据标签
4. **Chains** 按模块配置，通过 LangChain 编排 LLM 调用链：
   - Scanner: 扫描模块边界，生成骨架
   - Generator: 基于 RAG 检索 + 模板生成文档
   - Diagram: 生成 Mermaid 流程图
   - Verifier: 交叉验证文档与代码一致性
5. **Output** 按模块输出 Markdown 文件

## 目录结构

- `src/sources/` - 数据源采集层
- `src/parsing/` - 代码与文档解析层
- `src/rag/` - 向量化与检索层
- `src/chains/` - LLM 生成链层
- `src/templates/` - Jinja2 文档模板
- `prompts/` - LLM Prompt 模板（可独立迭代）
- `output/` - 生成的知识库文档
