# document-automation

基于 RAG + LangChain 的知识库文档自动生成工具，专为 Pacvue Custom Dashboard 项目设计。

融合五个数据源（后端代码、前端代码、技术评审文档、PRD 文档、Figma 设计稿），按业务模块自动生成结构化 Markdown 知识库文档。

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

> LLM Gateway 的 API Key 请联系 zack.shang@pacvue.com 申请。

### 验证数据源连通性

配置完成后，运行检查脚本确认所有数据源（GitHub、Confluence、LLM Gateway）均可正常连接：

```bash
python check_config.py
```

全部通过后再进行后续操作。如有失败项，请根据提示修正 `.env` 中的对应配置。

### 使用

```bash
# 1. 索引所有数据源（首次使用）
python -m src.main index

# 2. 生成全部模块文档
python -m src.main generate

# 3. 生成指定模块文档
python -m src.main generate --module core-api

# 4. 全量重建索引（清除后重建）
python -m src.main index --clear
```

## 数据源

系统从 5 个独立数据源采集信息，每个数据源可单独索引和更新：

| `--source` 值 | 数据来源 | 说明 |
|---|---|---|
| `backend` | GitHub `Pacvue/custom-dashboard` production 分支 | Java/Spring Boot 后端代码 |
| `frontend` | GitHub `Pacvue/CustomDashboard-modules-web` master 分支 | Vue 前端代码 |
| `confluence-tech` | Confluence page `2752762` 子页面 | 技术评审文档 |
| `confluence-prd` | Confluence page `3441902` 子页面 | PRD 产品需求文档 |
| `figma` | Figma file `2sKAoYhrKF3G8ZLiumT1rc` | UI 设计稿（页面结构、组件、文本、评论） |

此外还有两个快捷别名：

| 别名 | 等价于 |
|---|---|
| `confluence` | `confluence-tech` + `confluence-prd` |
| `all`（默认） | 全部 5 个数据源 |

## 增量更新

指定 `--source` 时，系统会自动清除该数据源的旧索引再重建，不影响其他数据源的数据。

```bash
# 后端代码变了 —— 只重建后端索引，再生成相关模块
python -m src.main index --source backend
python -m src.main generate --module core-api

# PRD 文档更新了 —— 只重建 PRD 索引
python -m src.main index --source confluence-prd

# 技术评审文档更新了 —— 只重建技术评审索引
python -m src.main index --source confluence-tech

# Confluence 两类文档都更新了 —— 同时重建
python -m src.main index --source confluence

# 前端代码变了 —— 只重建前端索引，再生成前端架构文档
python -m src.main index --source frontend
python -m src.main generate --module frontend

# Figma 设计稿更新了 —— 只重建 Figma 索引
python -m src.main index --source figma
```

### 典型工作流

1. **首次使用**：`index`（全量）-> `generate`（全量）-> `generate-user-guide`（用户指南）
2. **后端代码变更**：`index --source backend` -> `generate --module <模块名>` -> `generate-user-guide --module <章节名>`
3. **PRD 文档更新**：`index --source confluence-prd` -> `generate` -> `generate-user-guide`
4. **全量重建**：`index --clear` -> `generate` -> `generate-user-guide`

## 用户指南生成

除技术文档外，还可以基于已生成的技术文档，自动转写为面向终端用户（广告主/运营人员）的操作指南：

```bash
# 生成全部用户指南（需先运行 generate 生成技术文档）
python -m src.main generate-user-guide

# 生成指定章节
python -m src.main generate-user-guide --module chart-settings

# 查看所有用户指南章节
python -m src.main list-user-chapters
```

用户指南输出到 `output/user-guide/` 目录，包含以下章节：

- `00-overview.md` - Custom Dashboard 产品概览
- `01-dashboard-management.md` - Dashboard 管理
- `02-chart-settings.md` - 图表配置与过滤条件
- `03-platform-guide.md` - 各广告平台使用指南
- `04-sharing.md` - 分享与协作
- `05-faq.md` - 常见问题

## 输出说明

向量数据库（ChromaDB）仅在本地运行，用于中间检索，不包含在最终产物中。**最终产物为 `output/` 目录下的 Markdown 文档**，可直接提交到 Git 或导入到任何知识库平台。

### 技术文档

生成的技术文档按业务模块划分：

- `00-architecture.md` - 全局架构总览
- `01-core-api.md` - Dashboard CRUD / Chart / QueryChart 核心链路
- `02-template.md` - Chart Template 管理
- `03-share-link.md` - ShareLink 功能
- `04-data-source.md` - 数据源路由与物料查询
- `05-chart-types.md` - 各图表类型详解
- `06-dashboard-setting-filter.md` - Dashboard Setting 过滤条件与绩效影响（Retail/Commerce）
- `07-platform-amazon.md` - Amazon 平台
- `08-platform-walmart.md` - Walmart 平台
- `09-platform-commerce.md` - Commerce 平台
- `10-platform-instacart.md` - Instacart 平台
- `11-platform-criteo.md` - Criteo 平台
- `12-platform-target.md` - Target 平台
- `13-platform-kroger.md` - Kroger 平台
- `14-platform-dsp.md` - DSP 平台
- `15-platform-chewy.md` - Chewy 平台
- `16-platform-citrus.md` - Citrus 平台
- `17-platform-bol.md` - Bol 平台
- `18-platform-doordash.md` - Doordash 平台
- `19-platform-samsclub.md` - Sam's Club 平台
- `20-survey.md` - 用户调查问卷
- `21-message.md` - 消息通知
- `22-infra.md` - 基础设施
- `23-frontend.md` - 前端架构

### 用户指南

面向终端用户的操作指南，输出到 `output/user-guide/`：

- `00-overview.md` - 产品概览
- `01-dashboard-management.md` - Dashboard 管理
- `02-chart-settings.md` - 图表配置与过滤条件
- `03-platform-guide.md` - 各广告平台使用指南
- `04-sharing.md` - 分享与协作
- `05-faq.md` - 常见问题

## 架构

详见 [ARCHITECTURE.md](ARCHITECTURE.md)

## 后续优化方向
不够智能化，通用性不够（skill->agent方向）
- `文档目录应全基于LLM生成，非半人工制定`
- `调研采取更好的embeding分词模型和实现更好的检索器`
- `解析confluence 富文本格式，需要使用LLM理解图片等`
- `缺少投喂CS的客户单，FAQ精准实用度不足`
- `LLM不可用时的容灾`
