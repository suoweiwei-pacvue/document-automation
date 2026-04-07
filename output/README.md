# Custom Dashboard 知识库文档索引

> 本知识库由 document-automation 工具自动生成
> 生成时间: 2026-04-07 16:44:19

## 文档列表

- [Custom Dashboard 全局架构总览](00-architecture.md) - 系统整体架构、模块关系、技术栈、部署方式
- [核心 API - Dashboard 与 Chart 管理](01-core-api.md) - Dashboard CRUD、Chart 管理、QueryChart 核心链路
- [Chart Template 管理](02-template.md) - Template 创建/编辑/删除/复制/收藏/分组/批量引用/跨 Client 分享
- [ShareLink 分享功能](03-share-link.md) - ShareLink 创建/访问、CustomHeaderFilter、权限控制、外部访问
- [数据源路由与物料查询](04-data-source.md) - DashboardDatasourceManager、PlatformDatasourceSupport、各平台物料查询接口
- [图表类型详解](05-chart-types.md) - TrendChart/TopOverview/ComparisonChart/StackedBarChart/PieChart/Table/GridTable/WhiteBoard 的 Setting 结构与渲染逻辑
- [Amazon 平台模块](06-platform-amazon.md) - Amazon Advertising / SOV / Product Center 的数据查询与指标映射
- [Walmart 平台模块](07-platform-walmart.md) - Walmart 广告数据查询与指标映射
- [Commerce 平台模块](08-platform-commerce.md) - Commerce/Vendor/Seller 数据查询、HQ 迁移
- [其他平台模块](09-platform-others.md) - Instacart/Criteo/Target/Kroger/DSP/Chewy/Bol/Doordash/Samsclub
- [用户调查问卷](10-survey.md) - 用户提交图表类型调查、Admin 查询/导出
- [消息通知模块](11-message.md) - 消息推送与通知管理
- [基础设施](12-infra.md) - 认证鉴权/Feign 配置/缓存策略/异常处理/MyBatis-Plus/部署/CI-CD
- [前端架构](13-frontend.md) - Vue 组件结构/路由/Store 状态管理/API 层/样式体系

## 数据源

- 后端代码: `Pacvue/custom-dashboard` (Java/Spring Boot)
- 前端代码: `Pacvue/CustomDashboard-modules-web` (Vue)
- 技术评审: Confluence (35+ 篇)
- PRD 文档: Confluence (19 篇)
