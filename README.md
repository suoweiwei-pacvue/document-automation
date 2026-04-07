# document-automation

基于 RAG + LangChain 的知识库文档自动生成工具，专为 Pacvue Custom Dashboard 项目设计。

融合四个数据源（后端代码、前端代码、技术评审文档、PRD 文档），按业务模块自动生成结构化 Markdown 知识库文档。

## 快速开始

### 环境要求

- Python 3.10+
- OpenAI API Key（或 Anthropic API Key）

### 安装

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 配置

```bash
cp .env.example .env
# 编辑 .env 填入你的 API Keys 和配置
```

### 使用

```bash
# 1. 索引所有数据源
python -m src.main index

# 2. 生成全部模块文档
python -m src.main generate

# 3. 生成指定模块文档
python -m src.main generate --module core-api

# 4. 仅索引特定数据源
python -m src.main index --source backend
python -m src.main index --source frontend
python -m src.main index --source confluence
```

## 数据源

| 数据源 | 类型 | 位置 |
|--------|------|------|
| 后端代码 | Java/Spring Boot | 本地目录 或 GitHub |
| 前端代码 | Vue | GitHub `Pacvue/CustomDashboard-modules-web` |
| 技术评审 | Confluence | `pages/2752762` 子页面 |
| PRD 文档 | Confluence | `pages/3441902` 子页面 |

## 输出模块

生成的文档按业务模块划分，存放在 `output/` 目录：

- `00-architecture.md` - 全局架构总览
- `01-core-api.md` - Dashboard CRUD / Chart / QueryChart 核心链路
- `02-template.md` - Chart Template 管理
- `03-share-link.md` - ShareLink 功能
- `04-data-source.md` - 数据源路由与物料查询
- `05-chart-types.md` - 各图表类型详解
- `06-platform-amazon.md` - Amazon 平台
- `07-platform-walmart.md` - Walmart 平台
- `08-platform-commerce.md` - Commerce 平台
- `09-platform-others.md` - 其他平台
- `10-survey.md` - 用户调查问卷
- `11-message.md` - 消息通知
- `12-infra.md` - 基础设施
- `13-frontend.md` - 前端架构

## 架构

详见 [ARCHITECTURE.md](ARCHITECTURE.md)
