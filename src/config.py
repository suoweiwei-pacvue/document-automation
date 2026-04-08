from enum import Enum
from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings


class SourceType(str, Enum):
    BACKEND = "backend"
    FRONTEND = "frontend"
    CONFLUENCE_TECH = "confluence-tech"
    CONFLUENCE_PRD = "confluence-prd"
    CONFLUENCE = "confluence"
    FIGMA = "figma"
    ALL = "all"


INDEXABLE_SOURCES: list[str] = [
    SourceType.BACKEND.value,
    SourceType.FRONTEND.value,
    SourceType.CONFLUENCE_TECH.value,
    SourceType.CONFLUENCE_PRD.value,
    SourceType.FIGMA.value,
]

DOC_TYPE_TO_SOURCE: dict[str, str] = {
    "tech_review": SourceType.CONFLUENCE_TECH.value,
    "prd": SourceType.CONFLUENCE_PRD.value,
}


class Settings(BaseSettings):
    openai_api_key: str = ""
    openai_api_base: str = ""
    anthropic_api_key: str = ""
    llm_model: str = "gpt-4o"
    embedding_model: str = "text-embedding-3-small"

    github_token: str = ""
    github_owner: str = "Pacvue"
    github_repo_frontend: str = "CustomDashboard-modules-web"
    github_repo_backend: str = "custom-dashboard"
    github_frontend_branch: str = "master"
    github_backend_branch: str = "production"

    confluence_url: str = "https://pacvue-enterprise.atlassian.net"
    confluence_username: str = ""
    confluence_api_token: str = ""
    confluence_tech_page_id: str = "2752762,827458163"
    confluence_prd_page_id: str = "3441902"

    figma_access_token: str = ""
    figma_file_ids: str = ""

    chroma_persist_dir: str = "./chroma_db"
    chroma_collection_name: str = "cd_knowledge_base"

    output_dir: str = "./output"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

    def get_llm_kwargs(self) -> dict:
        """Build kwargs dict for ChatOpenAI, including base_url if set."""
        kwargs = {
            "model": self.llm_model,
            "openai_api_key": self.openai_api_key,
        }
        if self.openai_api_base:
            kwargs["base_url"] = self.openai_api_base
        return kwargs

    @property
    def confluence_tech_page_ids(self) -> list[str]:
        return [x.strip() for x in self.confluence_tech_page_id.split(",") if x.strip()]

    @property
    def confluence_prd_page_ids(self) -> list[str]:
        return [x.strip() for x in self.confluence_prd_page_id.split(",") if x.strip()]

    @property
    def figma_file_id_list(self) -> list[str]:
        return [x.strip() for x in self.figma_file_ids.split(",") if x.strip()]

    @property
    def output_path(self) -> Path:
        p = Path(self.output_dir)
        p.mkdir(parents=True, exist_ok=True)
        return p

    @property
    def chroma_path(self) -> Path:
        p = Path(self.chroma_persist_dir)
        p.mkdir(parents=True, exist_ok=True)
        return p


MODULE_DEFINITIONS = {
    "architecture": {
        "id": "00-architecture",
        "title": "Custom Dashboard 全局架构总览",
        "description": "系统整体架构、模块关系、技术栈、部署方式",
        "backend_modules": ["*"],
        "frontend_dirs": ["*"],
        "keywords": ["architecture", "overview", "system design"],
    },
    "core-api": {
        "id": "01-core-api",
        "title": "核心 API - Dashboard 与 Chart 管理",
        "description": "Dashboard CRUD、Chart 管理、QueryChart 核心链路",
        "backend_modules": ["custom-dashboard-api"],
        "backend_packages": [
            "com.pacvue.api.controller.DashboardController",
            "com.pacvue.api.controller.DashboardDatasourceController",
            "com.pacvue.api.service",
            "com.pacvue.api.handler",
            "com.pacvue.api.core",
            "com.pacvue.api.strategy",
        ],
        "frontend_dirs": ["Dashboard", "dashboardSub", "components"],
        "keywords": [
            "queryChart", "ChartHandler", "SettingHandler",
            "CollectorHandler", "IndicatorProcessor", "FrameHandler",
            "dashboard", "chart", "CRUD",
        ],
    },
    "template": {
        "id": "02-template",
        "title": "Chart Template 管理",
        "description": "Template 创建/编辑/删除/复制/收藏/分组/批量引用/跨 Client 分享",
        "backend_modules": ["custom-dashboard-api"],
        "backend_packages": [
            "com.pacvue.api.controller.TemplateController",
            "com.pacvue.api.controller.TemplateShareController",
        ],
        "frontend_dirs": ["TemplateManagements", "steps"],
        "keywords": [
            "template", "Template", "group", "favorite",
            "batch", "share pass", "import",
        ],
    },
    "share-link": {
        "id": "03-share-link",
        "title": "ShareLink 分享功能",
        "description": "ShareLink 创建/访问、CustomHeaderFilter、权限控制、外部访问",
        "backend_modules": ["custom-dashboard-api"],
        "backend_packages": [
            "com.pacvue.api.controller.ShareController",
            "com.pacvue.api.Filter",
        ],
        "frontend_dirs": ["Share"],
        "keywords": [
            "share", "ShareLink", "CustomHeaderFilter",
            "briefTips", "walmartUserGuidance",
        ],
    },
    "data-source": {
        "id": "04-data-source",
        "title": "数据源路由与物料查询",
        "description": "DashboardDatasourceManager、PlatformDatasourceSupport、各平台物料查询接口",
        "backend_modules": ["custom-dashboard-api"],
        "backend_packages": [
            "com.pacvue.api.manager",
            "com.pacvue.api.controller.DashboardDatasourceController",
        ],
        "frontend_dirs": ["api", "metricsList"],
        "keywords": [
            "datasource", "DatasourceManager", "PlatformDatasourceSupport",
            "material", "profile", "getAsinList",
        ],
    },
    "chart-types": {
        "id": "05-chart-types",
        "title": "图表类型详解",
        "description": "TrendChart/TopOverview/ComparisonChart/StackedBarChart/PieChart/Table/GridTable/WhiteBoard 的 Setting 结构与渲染逻辑",
        "backend_modules": ["custom-dashboard-base", "custom-dashboard-api"],
        "backend_packages": ["com.pacvue.base.dto"],
        "frontend_dirs": ["dashboardSub", "components"],
        "keywords": [
            "ChartSetting", "LineChart", "TrendChart", "TopOverview",
            "BarChart", "ComparisonChart", "StackedBarChart", "PieChart",
            "Table", "GridTable", "WhiteBoard", "extractParam",
        ],
    },
    "dashboard-setting-filter": {
        "id": "06-dashboard-setting-filter",
        "title": "Dashboard Setting 过滤条件与绩效影响（Retail/Commerce）",
        "description": "Retail(HQ) 与 Commerce 两个平台各自的 Dashboard Setting 物料过滤条件（Campaign/AdGroup/Keyword/ASIN/SKU 等）如何影响最终绩效数据结果。文档内分两大章节分别描述各平台的过滤逻辑、指标计算和数据口径差异",
        "backend_modules": ["custom-dashboard-commerce", "custom-dashboard-api"],
        "backend_packages": [
            "com.pacvue.api.handler.SettingHandler",
            "com.pacvue.api.handler.CollectorHandler",
            "com.pacvue.api.strategy",
            "com.pacvue.api.manager.support.CommerceDatasourceSupport",
        ],
        "frontend_dirs": ["dashboardSub", "steps", "components"],
        "keywords": [
            "ChartSetting", "SettingHandler", "CollectorHandler",
            "commerce", "HQ", "vendor", "seller",
            "retail", "Retail", "CrossRetailer",
            "filter", "campaign", "adGroup", "keyword",
            "ASIN", "SKU", "profile", "material",
            "extractParam", "indicator", "metric",
            "CommerceReport", "CommerceDatasourceSupport",
        ],
    },
    "platform-amazon": {
        "id": "07-platform-amazon",
        "title": "Amazon 平台模块",
        "description": "Amazon Advertising / SOV / Product Center 的数据查询与指标映射",
        "backend_modules": ["custom-dashboard-amazon", "custom-dashboard-amazon-rest"],
        "frontend_dirs": [],
        "keywords": [
            "amazon", "AmazonReport", "AmazonRest", "SOV",
            "ProductCenter", "ASIN", "campaignTag",
        ],
    },
    "platform-walmart": {
        "id": "08-platform-walmart",
        "title": "Walmart 平台模块",
        "description": "Walmart 广告数据查询与指标映射",
        "backend_modules": ["custom-dashboard-walmart"],
        "frontend_dirs": [],
        "keywords": ["walmart", "WalmartReport"],
    },
    "platform-commerce": {
        "id": "09-platform-commerce",
        "title": "Commerce 平台模块",
        "description": "Commerce/Vendor/Seller 数据查询、HQ 迁移",
        "backend_modules": ["custom-dashboard-commerce"],
        "frontend_dirs": [],
        "keywords": ["commerce", "CommerceReport", "vendor", "seller", "HQ"],
    },
    "platform-instacart": {
        "id": "10-platform-instacart",
        "title": "Instacart 平台模块",
        "description": "Instacart 广告数据查询与指标映射",
        "backend_modules": ["custom-dashboard-instacart"],
        "frontend_dirs": [],
        "keywords": ["instacart", "InstacartReport"],
    },
    "platform-criteo": {
        "id": "11-platform-criteo",
        "title": "Criteo 平台模块",
        "description": "Criteo 广告数据查询与指标映射",
        "backend_modules": ["custom-dashboard-criteo"],
        "frontend_dirs": [],
        "keywords": ["criteo", "CriteoReport"],
    },
    "platform-target": {
        "id": "12-platform-target",
        "title": "Target 平台模块",
        "description": "Target 广告数据查询与指标映射",
        "backend_modules": ["custom-dashboard-target"],
        "frontend_dirs": [],
        "keywords": ["target", "TargetReport"],
    },
    "platform-kroger": {
        "id": "13-platform-kroger",
        "title": "Kroger 平台模块",
        "description": "Kroger 广告数据查询与指标映射",
        "backend_modules": ["custom-dashboard-kroger"],
        "frontend_dirs": [],
        "keywords": ["kroger", "KrogerReport"],
    },
    "platform-dsp": {
        "id": "14-platform-dsp",
        "title": "DSP 平台模块",
        "description": "Amazon DSP 广告数据查询与指标映射",
        "backend_modules": ["custom-dashboard-dsp"],
        "frontend_dirs": [],
        "keywords": ["dsp", "DspReport", "DSP"],
    },
    "platform-chewy": {
        "id": "15-platform-chewy",
        "title": "Chewy 平台模块",
        "description": "Chewy 广告数据查询与指标映射",
        "backend_modules": ["custom-dashboard-chewy"],
        "frontend_dirs": [],
        "keywords": ["chewy", "ChewyReport"],
    },
    "platform-citrus": {
        "id": "16-platform-citrus",
        "title": "Citrus 平台模块",
        "description": "Citrus 广告数据查询与指标映射",
        "backend_modules": ["custom-dashboard-citrus"],
        "frontend_dirs": [],
        "keywords": ["citrus", "CitrusReport"],
    },
    "platform-bol": {
        "id": "17-platform-bol",
        "title": "Bol 平台模块",
        "description": "Bol 广告数据查询与指标映射",
        "backend_modules": ["custom-dashboard-bol"],
        "frontend_dirs": [],
        "keywords": ["bol", "BolReport"],
    },
    "platform-doordash": {
        "id": "18-platform-doordash",
        "title": "Doordash 平台模块",
        "description": "Doordash 广告数据查询与指标映射",
        "backend_modules": ["custom-dashboard-doordash"],
        "frontend_dirs": [],
        "keywords": ["doordash", "DoordashReport"],
    },
    "platform-samsclub": {
        "id": "19-platform-samsclub",
        "title": "Samsclub 平台模块",
        "description": "Sam's Club 广告数据查询与指标映射",
        "backend_modules": ["custom-dashboard-samsclub"],
        "frontend_dirs": [],
        "keywords": ["samsclub", "SamsclubReport"],
    },
    "survey": {
        "id": "20-survey",
        "title": "用户调查问卷",
        "description": "用户提交图表类型调查、Admin 查询/导出",
        "backend_modules": ["custom-dashboard-api"],
        "backend_packages": ["com.pacvue.api.controller.SurveyController"],
        "frontend_dirs": [],
        "keywords": ["survey", "questionnaire"],
    },
    "message": {
        "id": "21-message",
        "title": "消息通知模块",
        "description": "消息推送与通知管理",
        "backend_modules": ["custom-dashboard-message"],
        "frontend_dirs": [],
        "keywords": ["message", "notification", "kafka"],
    },
    "infra": {
        "id": "22-infra",
        "title": "基础设施",
        "description": "认证鉴权/Feign 配置/缓存策略/异常处理/MyBatis-Plus/部署/CI-CD",
        "backend_modules": ["custom-dashboard-web-base", "custom-dashboard-feign"],
        "frontend_dirs": [],
        "keywords": [
            "OAuth2", "SecurityContext", "Feign", "cache",
            "ExceptionAdvice", "MyBatisPlus", "Apollo", "Eureka",
        ],
    },
    "frontend": {
        "id": "23-frontend",
        "title": "前端架构",
        "description": "Vue 组件结构/路由/Store 状态管理/API 层/样式体系",
        "backend_modules": [],
        "frontend_dirs": ["*"],
        "keywords": [
            "store", "router", "vue", "component",
            "api", "dialog", "steps",
        ],
    },
}
