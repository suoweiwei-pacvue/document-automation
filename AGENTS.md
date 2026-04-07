# AGENTS.md

## 项目简介

`document-automation` 是一个 Python CLI 工具，使用 RAG + LangChain 自动生成 Pacvue Custom Dashboard 的知识库文档。

## 仓库导航

- [ARCHITECTURE.md](ARCHITECTURE.md) - 系统架构
- [README.md](README.md) - 使用说明
- `src/` - 源代码
- `prompts/` - LLM Prompt 模板
- `src/templates/` - Jinja2 文档输出模板
- `output/` - 生成的文档

## 开工前先看

1. [ARCHITECTURE.md](ARCHITECTURE.md) 了解分层架构
2. `src/config.py` 了解配置项
3. `src/chains/` 了解文档生成链路
4. `prompts/` 了解 Prompt 设计

## 文档真相来源

- 生成的知识库文档在 `output/` 目录
- Prompt 模板在 `prompts/` 目录
- 文档输出模板在 `src/templates/` 目录

## 约束

- 初始化阶段不修改目标仓库的业务代码
- 所有不确定信息在生成文档中标注 "待确认" 或 "TBD"
- 不臆造代码中不存在的架构事实
