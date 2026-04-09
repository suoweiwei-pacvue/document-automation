# 各广告平台使用指南

> Pacvue Custom Dashboard 用户指南
> 更新时间: 2026-04-09 13:20:01

---



# 各广告平台使用指南

## 功能简介

Pacvue Custom Dashboard 支持接入多个广告平台的数据，让您在同一个看板中查看和分析不同平台的广告表现。目前支持的平台包括 **Amazon Advertising（广告）**、**Amazon SOV（搜索份额）**、**Amazon Commerce（零售数据）**、**Walmart** 以及 **DSP（程序化广告）**。

每个平台提供不同的数据维度和指标，您可以根据业务需要选择合适的平台数据源，创建图表进行分析。本指南将帮助您了解各平台的数据查看方式、配置方法以及它们之间的关键差异。

## 使用场景

- **查看 Amazon 广告投放效果**：了解各广告活动、关键词、ASIN 的花费、销售额、ACOS 等核心指标表现。
- **分析 Amazon 搜索份额（SOV）**：查看品牌或 ASIN 在搜索结果中的曝光占比，评估品牌竞争力。
- **监控 Amazon 零售数据**：查看 Vendor（1P）或 Seller（3P）渠道的销售、流量等商业数据。
- **追踪 Walmart 广告表现**：查看 Walmart 平台各层级广告数据，包括关键词搜索份额。
- **分析 DSP 程序化广告效果**：查看 Amazon DSP 广告的展示、点击、转化等全链路数据。

---

## 操作指南

### 一、Amazon Advertising（广告数据）

#### 功能说明

Amazon Advertising 模块用于查看 Amazon 广告投放的绩效数据。您可以从多个维度查看数据，包括广告账户（Profile）、广告活动（Campaign）、关键词（Keyword）、商品（ASIN）、广告类型（Ad Type）、搜索词（Search Term）等，并选择 ACOS、ROAS、CPC、Sales、Spend 等指标进行分析。

#### 操作步骤

1. 进入 Dashboard 编辑页面，点击添加图表或编辑已有图表。
2. 选择图表类型（如折线图、表格、饼图、堆叠柱状图、网格表等）。
3. 在数据源区域选择 **Amazon** 平台。
4. **选择物料层级**（Material Level）——即您希望从哪个维度查看数据：
   - **Profile**：按广告账户汇总查看
   - **Campaign**：按广告活动查看
   - **Keyword**：按关键词查看
   - **ASIN**：按商品查看
   - **Ad Type**：按广告类型查看
   - **Search Term**：按搜索词查看（用户实际搜索的词）
   - **PAT（Product Attribute Targeting）**：按商品定向查看
   - **Campaign Tag**：按活动标签分组查看
   - **Amazon Channel**：按渠道查看（包含 Search 和 DSP 两大类）

[截图: Amazon 平台物料层级选择下拉框]

5. **选择物料范围模式**：
   - **Customize（自定义）**：手动搜索并选择具体的物料项（如选择特定的几个 Campaign）
   - **Top Rank（排名前列）**：系统自动按指标排名选取表现最好的物料
   - **Top Mover（变化最大）**：系统自动选取指标变化幅度最大的物料
   - **Bottom Ranked（排名末尾）**：系统自动选取表现最差的物料

6. **配置筛选条件**：
   - 选择 **Profile**（必选，即广告账户）
   - 可选择 **Campaign Tags** 进行标签筛选，支持 **And**（同时满足所有标签）和 **Or**（满足任一标签）两种条件模式
   - 设置时间范围
   - 选择时间粒度（Time Segment）：按天（Daily）、按周（Weekly）或按月（Monthly）

7. **选择指标**：从指标列表中勾选需要展示的指标，常用指标包括：
   - **ACOS**（广告花费占销售额比例，越低越好）
   - **ROAS**（广告投资回报率，越高越好）
   - **CPC**（每次点击成本）
   - **Sales**（广告带来的销售额）
   - **Spend**（广告花费）
   - **CTR**（点击率）
   - **CVR**（转化率）
   - **NTB 系列**（New-to-Brand，品牌新客相关指标）

8. 预览图表效果，确认无误后保存。

[截图: Amazon 广告图表配置完成后的预览效果]

#### 注意事项

- **Amazon Channel 物料层级**仅在 Cross Retailer（跨平台）模式下可用。选择 Amazon Channel 后，Search 类型包含 4 种广告类型，DSP 类型包含 1 种广告类型，两者的筛选条件不同——Amazon Search 需要选择 Profile 和 Campaign Tags，DSP 需要选择 Advertiser 和 Order Tag。
- 当时间粒度选择 **Weekly** 时，日期显示格式为"日期 + 第 xx 周"（如"01/06 第 2 周"），方便您快速定位周次。
- Campaign Tag 的 And/Or 筛选条件会影响数据范围：选择 **And** 表示物料必须同时包含所有选中的标签，选择 **Or** 表示包含任一标签即可。

---

### 二、Amazon SOV（搜索份额数据）

#### 功能说明

SOV（Share of Voice，搜索份额）用于衡量您的品牌或商品在 Amazon 搜索结果中的曝光占比。通过 SOV 数据，您可以了解品牌在特定关键词或品类中的竞争地位。SOV 支持两种查看维度：**Brand（品牌）** 和 **ASIN（商品）**。

#### 操作步骤

1. 在 Dashboard 中添加或编辑图表，选择 **SOV** 作为数据源。
2. **选择 SOV Market**：从可用的市场列表中选择您要查看的市场（如 US、UK、DE 等）。
3. **选择 SOV Group**：选择要分析的品牌分组。系统会展示品牌和父品牌的分组信息，已自动去重处理。
4. **选择查看维度**：
   - **Brand Metric**：从品牌维度查看搜索份额
   - **ASIN Metric**：从具体商品维度查看搜索份额
5. **设置时间范围**：开始日期和结束日期为必填项。
6. 如需在 Keyword 物料层级下查看 SOV 数据，可以在筛选条件中添加 **Keyword** 作为筛选项，进一步缩小分析范围。

[截图: SOV 数据源配置界面，展示 Market 和 Group 选择]

#### 注意事项

- SOV 数据查询必须设置时间范围，否则系统将提示参数错误。
- SOV 数据的更新频率可能与广告数据不同，请以实际数据时间为准。

---

### 三、Amazon Commerce（零售/商业数据）

#### 功能说明

Amazon Commerce 模块用于查看 Amazon 零售端的商业数据，包括销售额、流量、订单量等。该模块支持三种渠道模式，对应不同的 Amazon 卖家类型：

| 渠道模式 | 说明 | 适用对象 |
|---|---|---|
| **Vendor（1P）** | 一方卖家模式，通过 Amazon Vendor Central 供货 | 品牌商/供应商 |
| **Seller（3P）** | 三方卖家模式，通过 Amazon Seller Central 自营 | 第三方卖家 |
| **Hybrid（混合）** | 同时拥有 1P 和 3P 账户 | 同时使用两种模式的卖家 |

#### 操作步骤

1. 在图表配置中选择 **Amazon Commerce** 作为数据分类。
2. **选择渠道模式**（Vendor / Seller / Hybrid）。
3. **选择物料层级**——不同渠道模式支持的物料层级不同：

| 物料层级 | Hybrid | Vendor (1P) | Seller (3P) |
|---|---|---|---|
| Account Summary | ✅ | — | — |
| Account | ✅ | ✅ | ✅ |
| Market | ✅ | ✅ | ✅ |
| Category（自定义品类） | ✅ | ✅ | ✅ |
| Brand（自定义品牌） | ✅ | ✅ | ✅ |
| Amazon Category（Amazon 官方品类） | — | ✅ | ✅ |
| Amazon Brand（Amazon 官方品牌） | — | ✅ | ✅ |
| Product Tag（商品标签） | — | ✅ | ✅ |
| ASIN | — | ✅ | ✅ |

[截图: Commerce 渠道模式和物料层级选择界面]

4. **配置筛选条件（Filter 联动）**：Commerce 的筛选条件之间存在层级联动关系，选择上级筛选项后，下级选项会自动过滤：
   - 先选择 **Market**（国家/地区）
   - 再选择 **Account**（账户），系统会根据已选 Market 过滤可选账户
   - 再选择 **Brand / Category** 等，系统会根据已选 Market 和 Account 进一步过滤
   - 当物料为 ASIN 时，可以通过 Market 筛选项缩小 ASIN 范围

5. **选择指标**：根据所选渠道和物料，系统会展示可用的 Commerce 指标，按 Sales（销售）、Traffic（流量）等分组显示。

   > **重要提示**：选择某个渠道的指标后，其他渠道的指标将置灰不可选。例如，选择了 Vendor 的指标后，Seller 的指标将不可勾选。

6. **选择数据源层级**（Data Source）：
   - **Vendor (1P)** 下可选择：Manufacturing 或 Sourcing，以及更细分的 Retail / RetailSNS / Core / Business / Fresh 等
   - **Seller (3P)** 下可选择：All 或 SnS

7. 保存图表配置。

#### Vendor (1P) Profile 的特殊指标

对于 3P Profile 层级，系统额外提供以下零售指标：

| 指标名称 | 说明 |
|---|---|
| **Total Orders (3P)** | 总订单数 |
| **Total CVR (3P)** | 总转化率 = 总订单数 / 页面浏览量 |
| **Total AOV (3P)** | 平均订单价值 = 总收入 / 总订单数 |

> 注意：这三个指标仅在 3P Profile 下有数据。

#### Dashboard Setting 中的 Commerce 筛选

在 Dashboard Setting 的全局筛选器中，Commerce 和广告（Ads）的筛选条件是独立分开的：

- **Vendor 筛选器**：Account / Market / Category / Amazon Category / Brand / Amazon Brand / Product Tag
- **Seller 筛选器**：Account / Market / Category / Amazon Category / Brand / Amazon Brand / Product Tag
- **Hybrid 筛选器**：Account / Market / Category / Brand

全局筛选器设置的条件会与图表中的数据取交集，确保看板中所有图表的数据范围一致。

#### 注意事项

- **Hybrid 模式**下支持的物料层级较少（仅 Account Summary / Account / Market / Category / Brand），如需查看 Amazon Category、Amazon Brand、Product Tag 或 ASIN 层级的数据，请选择 Vendor 或 Seller 模式。
- 在编辑页面修改 Overview 物料时，仅展示 Data Source 信息，不支持直接修改。
- ASIN 物料支持批量粘贴 ASIN 进行快速选择。
- 分享链接（Share Link）场景下，系统会根据分享配置自动过滤数据范围，确保数据安全。

---

### 四、Walmart（沃尔玛广告数据）

#### 功能说明

Walmart 模块用于查看 Walmart 平台的广告投放数据。目前支持 **Search Ads（搜索广告）** 类型，提供多个物料层级的数据查看，并支持 Keyword 层级的品牌搜索份额（SOV）指标。

#### 操作步骤

1. 在图表配置中选择 **Walmart** 平台。
2. 选择广告类型为 **Search Ads**。

   > 注意：Walmart 的 Search Ads 在系统中归类为 **Display** 类别，与渠道/展示类定义对齐。

3. **选择物料层级**（Material Level）：
   - **Profile**：广告账户级别
   - **Campaign**：广告活动级别
   - **Ad Group**：广告组级别
   - **Keyword**：关键词级别
   - **Item**：广告商品级别
   - **Search Term**：搜索词级别
   - **Campaign Tag / Campaign Parent Tag**：活动标签级别
   - **Keyword Tag / Keyword Parent Tag**：关键词标签级别
   - **Item Tag / Item Parent Tag**：商品标签级别

[截图: Walmart 物料层级选择下拉框]

4. **选择物料范围**：支持 Customize（自定义选择）、Top Rank（排名前列）和 Top Mover（变化最大）三种模式。

5. **配置筛选条件**：
   - 对于 **Item** 和 **Keyword** 物料层级，可以额外使用 **Campaign Tag** 进行筛选
   - Ad Group 物料支持 Filter 搜索（由于数量可能较多，系统最多返回 300 条供选择）

6. **选择指标**：可选指标包括 Impressions（展示量）、Clicks（点击量）、Spend（花费）、Sales（销售额）、ROAS（广告投资回报率）等基础指标，以及 Online Same SKU Sales（同 SKU 线上销售额）、Online Same SKU Sale Units（同 SKU 线上销售件数）等在线指标。

7. 设置时间范围和对比模式（POP 环比 / YOY 同比），保存图表。

#### Walmart Keyword 层级的 SOV 指标

当物料层级选择 **Keyword** 时，指标面板中会出现 **SOV 分组**，包含以下品牌搜索份额指标：

| 指标名称 | 说明 |
|---|---|
| Brand Total SOV | 品牌总搜索份额 |
| Brand Paid SOV | 品牌付费搜索份额 |
| Brand SP SOV | 品牌 SP 广告搜索份额 |
| Brand SB SOV | 品牌 SB 广告搜索份额 |
| Brand SV SOV | 品牌 SV 广告搜索份额 |
| Brand Organic SOV | 品牌自然搜索份额 |

使用 SOV 指标时，需要额外选择 **Market**（市场）和 **Brand**（品牌）。

> **注意**：SOV 指标仅在 **Customize** 模式下支持按指标排序（Sort By），Top Rank 和 Top Mover 模式不支持排序。

#### Ad Group 物料层级的特殊说明

- 选择 Ad Group 后，在表格和趋势图中会额外显示 **Campaign Name** 列，方便您了解该广告组所属的活动。
- Ad Group 的筛选联动规则与 Campaign 相同，支持按 Profile 和 Campaign Tag 进行关联筛选。

---

### 五、DSP（程序化广告数据）

#### 功能说明

DSP（Demand-Side Platform，需求方平台）模块用于查看 Amazon DSP 程序化广告的投放数据。DSP 广告覆盖展示广告、视频广告等多种形式，数据维度丰富，支持从 Entity（实体）、Advertiser（广告主）、Order（订单）、Line Item（投放项）、Creative（创意素材）、ASIN（商品）等多个层级查看数据。

> **前提条件**：您的账号下需要有处于启用（Enable）状态的 DSP Profile，DSP 数据源选项才会出现。

#### 操作步骤

1. 在图表配置中选择 **DSP** 作为数据源。

   > 注意：DSP 数据源支持除白板（WhiteBoard）和堆叠柱状图（Stacked Bar Chart）以外的所有图表类型。

2. **选择物料层级**（Material Level）：
   - **Entity**：DSP 实体级别（最高层级）
   - **Advertiser**：广告主级别
   - **Order / Order Tag / Order Parent Tag**：订单及其标签级别
   - **Line Item / Line Item Tag / Line Item Parent Tag**：投放项及其标签级别
   - **Creative / Creative Tag / Creative Parent Tag**：创意素材及其标签级别
   - **ASIN**：商品级别
   - **Campaign Type / Ad Type**：活动类型 / 广告类型
   - **Filter-Linked Order**：关联订单（支持按 Advertiser 和 Order Tag 联动筛选）
   - **Amazon Channel**：Amazon 渠道级别

[截图: DSP 物料层级选择界面]

3. **配置 Profile 筛选**：DSP 的 Profile 筛选器显示为 **Entity → Advertisers** 的二级菜单结构。先选择 Entity，再选择该 Entity 下的 Advertiser。系统会将 Profile 筛选和 Advertiser 筛选分开存储。

[截图: DSP Entity → Advertiser 二级筛选菜单]

4. **配置其他筛选条件**：根据所选物料层级，系统会动态展示对应的筛选选项。例如：
   - 选择 **ASIN** 物料时，可以按 **Product Tag** 或 **Advertiser** 进行筛选
   - 选择 **Order** 相关物料时，可以按 **Order Tag** 进行筛选

5. **选择指标**：DSP 提供非常丰富的指标体系，主要分组包括：

| 指标分组 | 常用指标示例 |
|---|---|
| **成本与效率** | Total Cost（总花费）、eCPM（千次展示成本）、eCPC（每次点击成本） |
| **流量** | Impressions（展示量）、Click Throughs（点击量）、CTR（点击率）、Viewability Rate（可见率） |
| **销售与转化** | DSP Sales（DSP 销售额）、ROAS（投资回报率）、ACOS（广告花费占比）、Purchase（购买次数）、Units Sold（销售件数） |
| **购物行为** | DPV（商品详情页浏览）、DPVR（详情页浏览率）、ATC（加入购物车）、ATCR（加购率） |
| **品牌新客（NTB）** | NTB Sales（新客销售额）、NTB Purchase（新客购买次数）、NTB ROAS（新客投资回报率） |
| **Subscribe & Save** | SnSS（订阅并省钱次数）、SnSSR（订阅率） |
| **Brand Halo** | BH Sales、BH DPV、BH ATC 等（品牌光环效应指标） |
| **Off-Amazon** | Off-Amazon Purchases、Off-Amazon Sales 等（站外转化指标） |
| **视频** | Video Complete（视频完播次数）、Video Complete Rate（完播率） |

6. 设置时间范围，可选设置对比时间范围（用于环比/同比分析）。
7. 选择时间粒度（Daily / Weekly / Monthly）。
8. 保存图表配置。

#### 注意事项

- DSP 不支持白板（WhiteBoard）和堆叠柱状图（Stacked Bar Chart）图表类型。
- 如果您的账号下没有启用状态的 DSP Profile，将看不到 DSP 数据源选项。
- DSP 的 Tag 筛选支持 **And** 和 **Or** 两种操作符：And 表示必须同时匹配所有标签，Or 表示匹配任一标签即可。

---

## 各平台差异说明

### 支持的物料层级对比

| 物料层级 | Amazon Advertising | Amazon SOV | Amazon Commerce | Walmart | DSP |
|---|---|---|---|---|---|
| Profile / Entity | ✅ | — | — | ✅ | ✅（Entity） |
| Advertiser | — | — | — | — | ✅ |
| Campaign | ✅ | — | — | ✅ | — |
| Ad Group | — | — | — | ✅ | — |
| Order | — | — | — | — | ✅ |
| Line Item | — | — | — | — | ✅ |
| Creative | — | — | — | — | ✅ |
| Keyword | ✅ | — | — | ✅ | — |
| ASIN / Item | ✅ | ✅ | ✅ | ✅（Item） | ✅ |
| Search Term | ✅ | — | — | ✅ | — |
| Ad Type | ✅ | — | — | — | ✅ |
| Account / Market | — | — | ✅ | — | — |
| Brand / Category | — | ✅（Brand） | ✅ | — | — |
| 各级 Tag | ✅（Campaign Tag） | — | ✅（Product Tag） | ✅（Campaign/Keyword/Item Tag） | ✅（Order/LineItem/Creative Tag） |
| Amazon Channel | ✅ | — | — | — | ✅ |

### 支持的图表类型对比

| 图表类型 | Amazon Advertising | Amazon SOV | Amazon Commerce | Walmart | DSP |
|---|---|---|---|---|---|
| 折线图（Trend） | ✅ | ✅ | ✅ | ✅ | ✅ |
| 对比图（Comparison） | ✅ | — | ✅ | ✅ | ✅ |
| 饼图（Pie） | ✅ | — | ✅ | ✅ | ✅ |
| 表格（Table） | ✅ | ✅ | ✅ | ✅ | ✅ |
| 概览（Top Overview） | ✅ | — | ✅ | ✅ | ✅ |
| 堆叠柱状图（Stacked Bar） | ✅ | — | — | — | ❌ |
| 网格表（Grid Table） | ✅ | — | — | — | — |
| 白板（WhiteBoard） | ✅ | — | — | — | ❌ |

### SOV（搜索份额）功能对比

| 功能 | Amazon SOV | Walmart SOV |
|---|---|---|
| 查看入口 | 独立的 SOV 数据源 | Keyword 物料层级下的 SOV 指标分组 |
| 支持维度 | Brand、ASIN | Keyword（Brand SOV） |
| 需要额外选择 | SOV Market、SOV Group | Market、Brand |
| 指标类型 | Brand/ASIN 维度的搜索份额 | Brand Total/Paid/SP/SB/SV/Organic SOV |

### Commerce 渠道模式差异

| 特性 | Vendor (1P) | Seller (3P) | Hybrid |
|---|---|---|---|
| 适用卖家 | 品牌商/供应商 | 第三方卖家 | 同时使用两种模式 |
| 支持物料层级数量 | 8 种 | 8 种 | 5 种（较少） |
| Amazon Category/Brand | ✅ | ✅ | ❌ |
| Product Tag | ✅ | ✅ | ❌ |
| ASIN | ✅ | ✅ | ❌ |
| Data Source 细分 | Manufacturing / Sourcing | All / SnS | — |
| 特殊指标 | — | Total Orders/CVR/AOV (3P) | — |

---

## 常见问题

**Q: 为什么我在数据源选项中看不到 DSP？**
A: DSP 数据源仅在您的账号下有处于启用（Enable）状态的 DSP Profile 时才会显示。请确认您的 DSP 账户已正确配置并启用。如仍无法看到，请联系您的账户管理员确认权限。

**Q: Amazon Commerce 的 Hybrid 模式为什么支持的物料层级比 Vendor/Seller 少？**
A: Hybrid 模式需要同时合并 1P 和 3P 两套数据，由于 Amazon Category、Amazon Brand、Product Tag 和 ASIN 等层级在两种渠道下的数据结构存在差异，目前 Hybrid 模式仅支持 Account Summary、Account、Market、Category 和 Brand 五个层级。如需查看更细粒度的数据，建议分别选择 Vendor 或 Seller 模式。

**Q: Walmart Keyword 层级的 SOV 指标为什么不能在 Top Rank 模式下排序？**
A: SOV 指标仅在 Customize（自定义选择）模式下支持按指标排序（Sort By）。在 Top Rank 和 Top Mover 模式下，系统按照广告绩效指标进行排名，SOV 指标不参与排序逻辑。如需按 SOV 指标排序，请切换到 Customize 模式。

**Q: Campaign Tag 筛选中的 And 和 Or 有什么区别？**
A: **And** 表示"同时满足"——只有同时包含所有选中标签的物料才会被纳入数据范围。**Or** 表示"满足任一"——包含任何一个选中标签的物料都会被纳入。例如，您选择了标签 A 和标签 B：使用 And 时，只有同时带有 A 和 B 标签的 Campaign 会被统计；使用 Or 时，带有 A 或 B 标签的 Campaign 都会被统计。

**Q: 在 Commerce 模块中，Dashboard Setting 的全局筛选器和图表内的筛选条件是什么关系？**
A: 全局筛选器（Dashboard Setting Filter）设置的条件会与图表查询结果取**交集**。也就是说，图表最终展示的数据必须同时满足全局筛选器和图表自身筛选条件。例如，全局筛选器选择了 Market = US，图表中选择了 Brand = X，那么最终只会展示美国市场下品牌 X 的数据。

**Q: 为什么 Walmart Ad Group 的下拉列表中只显示了部分数据？**
A: 由于 Ad Group 数量可能非常多，系统最多返回 300 条记录。您可以使用下拉框中的搜索功能（Filter）输入关键词来快速定位目标 Ad Group。如果您需要查看的 Ad Group 未出现在列表中，请尝试输入更精确的搜索词。

---

*本文档基于产品功能自动生成，如有疑问请联系产品团队。*