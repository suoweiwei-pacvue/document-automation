# 图表配置与过滤条件

> Pacvue Custom Dashboard 用户指南
> 更新时间: 2026-04-09 13:19:51

---



# 图表配置与过滤条件

## 功能简介

Custom Dashboard 提供了多种图表类型和灵活的过滤条件，帮助你将广告投放和业务数据以最直观的方式呈现出来。你可以根据分析需求选择趋势图、对比图、饼图、表格等不同图表形式，并通过 Dashboard 级别和图表级别的过滤条件精确控制每张图表展示的数据范围。

本章节将详细介绍每种图表的创建与配置方法，以及过滤条件的设置方式和它们对绩效数据的影响。

## 使用场景

- **追踪广告效果趋势**：使用趋势图查看 Impressions、Clicks、ACOS 等指标在一段时间内的变化走势，快速发现异常波动。
- **对比不同广告活动的表现**：使用对比图将多个 Campaign 或不同时间段的数据放在一起，直观看出差距。
- **监控关键指标达成进度**：使用概览卡片设置目标值，实时查看当前完成进度。
- **分析预算或流量的分布结构**：使用饼图或堆叠柱状图了解各 Campaign、广告类型或投放位置的占比。
- **通过过滤条件聚焦特定数据**：在 Dashboard 级别设置 Profile、Campaign Tag 等过滤条件，让所有图表只展示你关心的数据范围。

---

## 操作指南

### 一、图表类型总览

Custom Dashboard 支持以下八种图表类型，你可以根据分析目的选择最合适的类型：

| 图表类型 | 适用场景 | 简要说明 |
|---|---|---|
| 趋势图（Trend Chart） | 观察指标随时间的变化 | 折线图或面积图，展示日/周/月趋势 |
| 概览卡片（Top Overview） | 快速查看关键指标汇总值 | 数值卡片形式，支持目标进度展示 |
| 对比图（Comparison Chart） | 对比不同物料或时间段 | 柱状图，支持同比/环比对比 |
| 堆叠柱状图（Stacked Bar Chart） | 分析指标的构成拆分 | 按维度拆分的堆叠柱状图 |
| 饼图（Pie Chart） | 查看占比分布 | 展示各物料在某指标上的占比 |
| 表格（Table） | 多指标数据明细查看 | 表格形式展示，支持排序 |
| 交叉表格（Grid Table） | 二维交叉分析 | 行列分别为不同物料维度 |
| 白板（WhiteBoard） | 自由布局 | 自由画布类型 |

[截图: 图表类型选择界面，展示八种图表类型的选择入口]

---

### 二、创建图表的通用流程

无论选择哪种图表类型，创建过程都遵循以下基本步骤：

1. 在 Dashboard 编辑页面，点击添加图表的按钮。
2. **选择图表类型**：从上述八种类型中选择一种。
3. **配置基础设置（Basic Setting）**：填写图表名称，选择模式、时间粒度等基础参数。
4. **选择指标（Select Metric）**：根据图表类型选择一个或多个指标（如 Impressions、Clicks、Spend、ACOS 等），并为每个指标配置颜色等展示样式。
5. **配置数据范围（Scope Setting）**：为指标选择数据来源的物料范围，包括平台、Profile、Campaign Tag 等层级。
6. **可选：高级配置**：根据图表类型，可能还有快捷切换、拆分维度等高级选项。
7. **保存**：确认配置无误后保存图表。

下面分别介绍每种图表类型的详细配置方法。

---

### 三、趋势图（Trend Chart）

#### 功能说明

趋势图以折线或面积图的形式展示一个或多个指标随时间的变化趋势。它是最常用的图表类型之一，适合用来追踪广告效果的日常波动和长期走势。

#### 三种模式

趋势图提供三种模式，适用于不同的分析场景：

| 模式 | 说明 | 典型场景 |
|---|---|---|
| 多指标模式（Multi Metrics） | 所有指标共享同一组物料范围，在同一张图上展示多条线 | 同时查看某个 Campaign 的 Impressions 和 Clicks 趋势 |
| 多物料模式（Multi Values） | 选择单一指标，按不同物料分别展示多条线 | 对比多个 Campaign 各自的 Spend 趋势 |
| 自定义模式（Customize） | 每条线可以独立配置指标和物料范围 | 灵活组合，如一条线看 Campaign A 的 Impressions，另一条看 Campaign B 的 Clicks |

#### 操作步骤

1. 选择图表类型为 **Trend Chart**，系统会打开设置弹窗，包含 **Basic Setting**、**Select Metric**、**Scope Setting** 等面板。

2. **配置 Basic Setting**：
   - 输入图表名称。
   - 选择模式：Multi Metrics / Multi Values / Customize。
   - 选择图表子类型：**折线图（Line）** 或 **面积图（Area）**。
   - 选择时间粒度：**Daily（按天）**、**Weekly（按周）** 或 **Monthly（按月）**。
   - 可选：开启 **Quick Switch** 开关。开启后，图表展示时会在右上角显示 D/W/M 快捷切换按钮，方便你在查看时快速切换时间粒度，无需重新编辑图表。

3. **选择指标（Select Metric）**：
   - 点击进入 Select Metric 面板，从指标列表中选择需要展示的指标。
   - 为每个指标设置展示颜色和展示类型。

4. **配置数据范围（Scope Setting）**：
   - 选择平台（如 Amazon、Walmart 等）。
   - 逐级选择物料范围，例如先选 Profile，再选 Campaign 或 Campaign Tag。
   - 在多指标模式下，所有指标共享同一组物料范围。
   - 在自定义模式下，每条线可以独立设置物料范围。

5. 确认配置后点击保存。

[截图: 趋势图设置弹窗，展示 Basic Setting 面板中的模式选择和时间粒度选项]

[截图: 趋势图设置弹窗，展示 Select Metric 面板中的指标选择界面]

#### 注意事项

- **Quick Switch 限制**：当数据源为 Commerce 平台的 SnS（Subscribe & Save）数据时，不支持开启 Quick Switch。
- **Filter-linked Campaign**：仅在多指标模式（Multi Metrics）下支持关联 Dashboard 顶部的 Campaign Filter。选中后，图表的数据范围将跟随 Filter 变化，右侧不再单独展示 Data Scope 选择区域。
- **图表提示文案**：图表上方会自动生成一段描述文案，帮助查看者理解图表展示的数据内容。例如，多物料模式下会显示"The {指标名称} for each {物料层级} individually"。

---

### 四、概览卡片（Top Overview）

#### 功能说明

概览卡片以数值卡片的形式展示关键指标的汇总值，适合放在 Dashboard 顶部，让你一眼看到最重要的数据。它支持三种展示格式。

#### 三种展示格式

| 格式 | 说明 | 适用指标类型 |
|---|---|---|
| Regular（常规） | 默认样式，直接展示指标数值 | 所有指标类型 |
| Target Progress（目标进度） | 进度条样式，展示当前值相对目标值的完成进度 | 仅数字和货币类型指标（如 Spend、Sales），不支持百分比类型 |
| Target Compare（目标对比） | 对比样式，展示当前值与目标值的差异 | 仅百分比类型指标（如 ACOS、CTR） |

#### 操作步骤 — Regular 格式

1. 选择图表类型为 **Top Overview**。
2. 在 Basic Setting 中选择 **Chart Format** 为 **Regular**。
3. 选择需要展示的指标（最多 3 个）。
4. 配置每个指标的数据范围。
5. 保存。

#### 操作步骤 — Target Progress 格式

1. 选择图表类型为 **Top Overview**。
2. 在 Basic Setting 中选择 **Chart Format** 为 **Target Progress**。
3. 选择指标（仅可选择数字和货币类型的指标，最多 3 个）。
4. 为每个选中的指标输入 **Target Value（目标值）**——这是必填项，需要输入大于 0 的数字（最多两位小数）。
5. 配置数据范围。
6. 保存。

系统会自动计算完成百分比：
- 对于**正向指标**（如 Sales、Impressions，数值越高越好）：完成百分比 = 当前值 ÷ 目标值。
- 对于**反向指标**（如 ACOS，数值越低越好）：完成百分比 = 目标值 ÷ 当前值。

[截图: Target Progress 格式的概览卡片，展示进度条和完成百分比]

#### 操作步骤 — Target Compare 格式

1. 选择图表类型为 **Top Overview**。
2. 在 Basic Setting 中选择 **Chart Format** 为 **Target Compare**。
3. 选择指标（仅可选择百分比类型的指标）。
4. 为每个指标输入 **Target Value（目标值）**，单位与当前值一致。
5. 配置数据范围。
6. 保存。

系统会用颜色标识达成情况：
- **正向指标**（数值越高越好）：≥100% 显示绿色，80%~100% 显示橙色，≤80% 显示红色。
- **反向指标**（数值越低越好）：≤100% 显示绿色，100%~120% 显示橙色，≥120% 显示红色。
- **中性指标**（如 Impressions、Spend、ASP、COGS）：统一显示灰色，不做好坏判断。

#### 注意事项

- Target Progress 格式支持选择未来时间范围（用于设定未来目标），而 Regular 和 Target Compare 格式不支持。
- 系统会为前三个指标卡片自动设置默认名称：Performance、Efficiency、Awareness，你可以自行修改。

---

### 五、对比图（Comparison Chart）

#### 功能说明

对比图以柱状图的形式对比不同物料或不同时间段的指标数据，帮助你快速发现差异和变化。

#### 三种对比方式

| 对比方式 | 说明 | 典型场景 |
|---|---|---|
| By Sum（按汇总值） | 直接对比各物料的指标汇总值，支持多指标 | 对比 5 个 Campaign 的 Spend 和 Sales |
| YOY（同比） | 与去年同期对比 | 查看今年 Q1 与去年 Q1 的 Impressions 对比 |
| POP（环比） | 与上一个周期对比 | 查看本月与上月的 Sales 对比 |

#### 操作步骤

1. 选择图表类型为 **Comparison Chart**。
2. 在 Basic Setting 中选择对比方式：**By Sum**、**YOY** 或 **POP**。
3. 选择指标：
   - By Sum 模式下可选择多个指标。
   - YOY / POP 模式下通常选择单一指标进行对比。
4. 配置数据范围（Scope Setting）。
5. 保存。

对于 YOY 和 POP 模式，图表会自动生成两组柱子：一组代表当前周期的数据，另一组代表对比周期的数据。你可以在设置中自定义两组柱子的颜色。

[截图: 对比图设置弹窗，展示 YOY 模式下的颜色配置选项]

---

### 六、堆叠柱状图（Stacked Bar Chart）

#### 功能说明

堆叠柱状图将单一指标按某个维度拆分，以堆叠的方式展示各部分的构成。例如，你可以将 Spend 按投放位置（Placement）拆分，查看每个位置贡献了多少花费。

#### 两种展示模式

| 模式 | 说明 |
|---|---|
| By Trend（按趋势） | 按时间展示堆叠柱状图，查看各部分随时间的变化 |
| By Sum（按汇总） | 按物料展示堆叠柱状图，查看各物料中各部分的构成 |

#### 操作步骤

1. 选择图表类型为 **Stacked Bar Chart**。
2. 选择一个指标。
3. 选择 **Break Down 维度**（拆分维度），如 Placement（投放位置）、Campaign Type（广告活动类型）等。系统会根据你选择的指标和平台，自动列出可用的拆分维度。
4. 选择展示模式：By Trend 或 By Sum。
5. 配置数据范围。
6. 保存。

[截图: 堆叠柱状图设置弹窗，展示 Break Down 维度的选择下拉框]

#### 注意事项

- 堆叠柱状图**不支持** Filter-linked Campaign 功能。
- 堆叠柱状图**不支持** Share Tag 作为物料。

---

### 七、饼图（Pie Chart）

#### 功能说明

饼图展示单一指标在不同物料之间的占比分布，帮助你了解各部分的相对大小。

#### 两种数据选择方式

| 方式 | 说明 |
|---|---|
| Customize（自定义） | 手动选择要展示的物料范围 |
| Top N | 系统自动按指标值排序，取前 N 个物料展示 |

#### 操作步骤

1. 选择图表类型为 **Pie Chart**。
2. 选择一个指标。
3. 选择数据方式：
   - **Customize**：手动选择要对比的物料。
   - **Top N**：设置 N 的值，系统自动选取指标值最高的前 N 个物料。
4. 选择物料层级（如 Campaign、Profile 等）。
5. 配置数据范围。
6. 保存。

---

### 八、表格（Table）

#### 功能说明

表格以行列形式展示多指标数据，适合需要查看详细数据明细的场景。同样支持 Customize 和 Top N 两种数据选择方式。

#### 操作步骤

1. 选择图表类型为 **Table**。
2. 选择物料层级（Material Level），如 Campaign、Profile、Account 等。
3. 选择数据方式：Customize 或 Top N。
4. 选择需要展示的指标（可多选，每个指标对应表格中的一列）。
5. 配置数据范围。
6. 保存。

#### Commerce 平台的 Data Segment 功能

当你在 Commerce 平台的表格中选择 Account、Category 或 Brand 作为物料层级时，会出现一个额外的 **Data Segment** 选项。这个选项允许你在主物料的基础上，增加一个子维度进行组合展示。

可选的组合如下：

| 主物料层级（Material Level） | 可选的 Data Segment |
|---|---|
| Account | Category、Brand |
| Category | Account、Market、Brand |
| Brand | Category、Market、Account |
| Amazon Category | Account |
| Amazon Brand | Account |

例如，选择 Material Level 为 "Category"，Data Segment 为 "Account"，表格会按 Category 分组，每个 Category 下再按 Account 细分展示数据。

Data Segment 默认为空（不启用），且只允许单选。

---

### 九、交叉表格（Grid Table）

#### 功能说明

交叉表格是一种二维表格，行和列分别代表不同的物料维度，单元格展示两个维度交叉处的指标值。适合用来分析两个维度之间的关系。

#### 操作步骤

1. 选择图表类型为 **Grid Table**。
2. **选择指标**：仅支持单选一个指标。
3. **选择横向物料层级**（表格的列）：可选 Profile、Campaign Tag、Campaign Parent Tag、Campaign Type、Retailer、Share Tag。
4. **选择纵向物料层级**（表格的行）：可选范围取决于横向物料的选择（见下方兼容表）。
5. **高级配置**（可选）：
   - **Add Total Row**：在表格底部添加合计行。
   - **Add % of Total**：在每个单元格中额外显示占总计的百分比（仅纯数值指标支持此选项）。
6. 保存。

#### 横向与纵向物料的兼容关系

并非所有横向和纵向物料的组合都可以使用。下表展示了哪些组合是支持的（✓ 表示支持，✗ 表示不支持）：

| 纵向 ↓ \ 横向 → | Profile | Campaign (Parent) Tag | Campaign Type | Retailer | Share Tag |
|---|---|---|---|---|---|
| **Profile** | ✗ | ✓ | ✓ | ✗ | ✓ |
| **Campaign (Parent) Tag** | ✓ | ✓ | ✓ | ✗ | ✓ |
| **Campaign Type** | ✓ | ✓ | ✗ | ✗ | ✓ |
| **Retailer** | ✗ | ✗ | ✗ | ✗ | ✓ |
| **Share Tag** | ✓ | ✓ | ✓ | ✓ | ✗ |

例如：横向选择 "Campaign Tag"，纵向可以选择 Profile、Campaign (Parent) Tag、Campaign Type 或 Share Tag，但不能选择 Retailer。

#### 注意事项

- 交叉表格**不支持**批量创建 Dashboard。
- 交叉表格**不支持** Filter-linked 功能。

---

### 十、Dashboard 级别的过滤条件（Filter Setting）

#### 功能说明

Dashboard 级别的过滤条件是一个全局设置，它控制整个 Dashboard 中所有图表的数据范围上限。设置后，Dashboard 中的每张图表都不会超出这个过滤范围，包括通过分享链接查看的场景。

#### 进入 Filter Setting

1. 进入 Dashboard 编辑页面。
2. 点击顶部的 **Dashboard Setting** 按钮。
3. 在弹窗中切换到 **Filter Setting** 标签页。

[截图: Dashboard Setting 弹窗，展示 Filter Setting 标签页]

#### Retail（HQ）平台的过滤项

| 过滤项 | 默认状态 | 说明 |
|---|---|---|
| **Retailer** | 默认全选 | 控制显示哪些 Retailer 的数据，会与 Profile 联动 |
| **Profile** | 默认选中，不可关闭 | 选择广告账户，这是必选项 |
| **Campaign Tag** | 默认关闭 | 按 Campaign Tag 过滤数据，可为每个 Retailer 单独配置；未选择任何 Tag 视为全选 |
| **Ad Type Filter** | 默认关闭 | 按广告类型过滤（如 SP、SB、SD 等）；不同 Retailer 支持的广告类型不同，只有一种广告类型的 Retailer 不会显示此选项 |
| **Advertiser** | 默认关闭 | 仅 DSP 平台使用，按广告主过滤 |

#### Commerce 平台的过滤项

| 过滤项 | 默认状态 | 联动关系 |
|---|---|---|
| **Market** | 默认关闭，开启后默认为空（不选 = 全选） | 无 |
| **Account** | 默认关闭 | 受 Market 影响：选择了 Market 后，Account 下拉框只显示该 Market 下的 Account |
| **Category** | 默认关闭 | 受 Market 和 Account 影响 |
| **Amazon Category** | 默认关闭 | 受 Market 和 Account 影响 |
| **Brand** | 默认关闭 | 受 Market 和 Account 影响 |
| **Amazon Brand** | 默认关闭 | 受 Market 和 Account 影响 |
| **Tag（Product Tag）** | 默认关闭 | 独立过滤，不受其他过滤项影响 |

每个过滤项都有一个开关，你可以根据需要开启或关闭。开启后，在下拉框中选择具体的数据范围。

[截图: Commerce 平台的 Filter Setting 面板，展示各过滤项的开关和下拉框]

#### 操作步骤

1. 打开 **Dashboard Setting** > **Filter Setting**。
2. 根据需要开启对应的过滤项开关。
3. 在下拉框中选择数据范围。注意 Commerce 平台的联动关系——例如先选 Market，再选 Account，Account 的候选项会根据 Market 的选择自动更新。
4. 点击保存。

#### 注意事项

- **Profile 是必选项**：在 Retail 平台中，Profile 过滤默认选中且不可关闭，你至少需要选择一个 Profile。
- **过滤范围是上限**：Dashboard Filter 设定的是数据范围的"天花板"。图表中配置的物料范围不能超出这个范围，系统会自动取交集。
- **影响分享链接**：通过分享链接查看 Dashboard 的用户，也会受到 Filter Setting 的限制。

---

### 十一、查看 Dashboard 时使用过滤条件

#### 功能说明

在 Dashboard 查看页面，页面顶部会展示已配置的过滤条件下拉框。你可以在查看时动态调整过滤条件，所有图表会实时响应变化。

#### 操作步骤

1. 进入 Dashboard 查看页面。
2. 在页面顶部找到过滤条件下拉框（如 Profile、Campaign Tag、Market 等）。
3. 在下拉框中选择或取消选择某些值。
4. 下方所有图表的数据会自动更新。

#### 过滤条件与图表数据的交互规则

当你在顶部 Filter 中进行筛选时，系统会将 Filter 的选择与每张图表自身配置的物料范围取**交集**：

- **物料类型相同时**：如果图表的物料类型与 Filter 类型相同（例如图表按 Campaign Tag 展示，Filter 也选择了 Campaign Tag），则图表只展示两者的交集数据。
- **物料类型不同时**：如果图表的物料类型与 Filter 类型不同，Filter 仍然会限制数据的底层范围。

---

### 十二、Campaign Tag Filter 与图表的联动

#### 功能说明

当图表的物料选择了 Campaign Tag 或 Campaign Parent Tag 时，你可以控制该图表是否与 Dashboard 顶部的 Campaign Tag Filter 联动。

#### 操作步骤

1. 在图表设置的 **Scope Setting** 中，选择 Campaign Tag 或 Campaign Parent Tag 作为物料。
2. 你会看到一个复选框 **"Link Campaign Tag Filter"**（默认勾选）。
3. **勾选**：图表数据会与顶部 Campaign Tag Filter 取交集。Filter 中多选的 Tag 之间是"或"的关系（满足任一即可），然后再与图表中每一行的 Campaign Tag 取交集。
4. **不勾选**：顶部的 Campaign Tag Filter 不会影响该图表的数据范围。

#### 数据处理逻辑示例

假设你的图表展示了 Tag A、Tag B、Tag C 三行数据，顶部 Filter 选择了 Tag A 和 Tag B：
- 勾选 Link 后：Tag A 和 Tag B 的数据正常展示，Tag C 的数据显示为 0（因为交集为空），但 Tag C 这一行仍然会显示，不会被隐藏。
- 不勾选 Link：三行数据都正常展示，不受 Filter 影响。

提示文案：*"If you do not check this option, the Campaign Tag in the top Filter will not affect the data scope. If you check it, the selected Campaign Tag here will intersect with the Campaign Tag in the Filter."*

#### 不支持的场景

以下场景不支持 Campaign Tag Filter 联动：
- Cross Retailer - Retailer 场景。
- 饼图和表格的 Top N 排序范围。
- 饼图和表格中选择 Campaign Tag 后的 Top N 模式。

---

### 十三、图表级别的物料 Filter（View/Share 页面）

#### 功能说明

除了 Dashboard 级别的过滤条件，部分图表还支持在查看或分享页面展示独立的物料 Filter，让查看者可以在图表级别进一步筛选数据。

#### 支持情况

| 图表类型 | Filter 粒度 | 说明 |
|---|---|---|
| 概览卡片（Top Overview） | 按分组（Section） | 同一分组内的多个指标共享一个 Filter |
| 趋势图（Trend Chart） | 按指标（Metric） | 每个指标可以有独立的 Filter |
| 对比图（Comparison Chart） | 按指标（Metric） | 每个指标可以有独立的 Filter |
| 饼图（Pie Chart） | 按指标（Metric） | 每个指标可以有独立的 Filter |
| 表格（Table） | 按指标（Metric） | 通常只有一个指标 |
| 堆叠柱状图 | 不支持 | — |
| 交叉表格（Grid Table） | 不支持 | — |

#### 操作步骤

1. 在图表设置中，找到 **Show Filter** 开关并开启。
2. 可选：开启 **Specify Filter Scope**，指定查看者可以筛选的物料范围（如果不指定，则使用图表配置的全部物料范围）。
3. 保存后，在查看或分享页面，该图表上方会出现物料筛选下拉框。

---

### 十四、Commerce 图表中的 Market 筛选项

#### 功能说明

当 Commerce 平台的图表选择 Account、Category 或 Brand 作为物料层级时，会在图表设置中新增一个 **Market 筛选项**，用于进一步限定数据范围。

#### 各图表中 Market 筛选项的位置

| 图表类型 | Market 筛选项位置 |
|---|---|
| 概览卡片（Overview） | Basic Setting 模块下 |
| 趋势图（Trend） | 指标卡片内 |
| 对比图（Comparison） | Scope Setting 下 |
| 饼图（Pie Chart） | Customize 模式下展示 |
| 表格（Table） | Customize 模式下展示 |

#### 操作步骤

1. 在 Commerce 图表设置中，选择 Account、Category 或 Brand 作为物料层级。
2. 系统会自动显示 Market 筛选项。
3. 默认不筛选（不选 = 全选）。如果选择了具体的 Market，数据范围会取原有范围与所选 Market 的交集。

---

## 各平台差异说明

### 物料名称差异

不同广告平台对商品标识的叫法不同，在搜索和选择物料时请注意：

| 平台 | 商品标识名称 |
|---|---|
| Amazon、DSP | ASIN |
| Walmart、Samsclub | Item |
| Instacart、Criteo、Target、Citrus、Kroger、Chewy、Bol、Doordash | Product |
| Commerce | Commerce ASIN |

### DSP 平台的特殊层级

DSP 平台的 Profile 展示方式与其他平台不同，采用 **Entity → Advertiser** 的二级菜单结构。选择时需要先展开 Entity，再选择其下的 Advertiser。

### Commerce 平台的数据源选择

Commerce 平台需要选择数据通道：
- **1P（Vendor）**：供应商模式数据
- **3P（Seller）**：卖家模式数据
- **Hybrid**：混合模式数据

在图表设置中选择指标时，需要先确认数据源类型。

### Cross Retailer 场景

在 HQ 模块下创建 Cross Retailer Dashboard 时：
- 支持的图表类型：趋势图、对比图、概览卡片、表格、饼图。
- 物料选择仅支持 Customize（自定义）模式。
- Share Tag 物料目前仅支持与 Profile 联动，暂不支持与 Campaign Tag 或 Campaign Type 联动。

---

## 批量创建 Dashboard 的限制

当你选择多个图表批量创建 Dashboard 时，以下情况**不支持**批量操作：

1. 包含 Cross Retailer 的图表。
2. 包含趋势图 Customize（自定义）模式的图表。
3. 概览卡片中选择了不同物料的图表。
4. 包含交叉表格（Grid Table）的图表。

如果你的选择中包含以上情况，点击 "Go to Create" 后系统会弹窗提示具体原因。

---

## 常见问题

**Q: 为什么我在趋势图中看不到 Quick Switch（D/W/M 快捷切换）按钮？**
A: Quick Switch 需要在图表设置的 Basic Setting 中手动开启。另外，如果你的数据源是 Commerce 平台的 SnS（Subscribe & Save）数据，则不支持此功能。

**Q: 为什么概览卡片的 Target Progress 格式中，我找不到某些指标？**
A: Target Progress 格式仅支持数字和货币类型的指标（如 Spend、Sales、Impressions 等），不支持百分比类型的指标（如 ACOS、CTR）。如果你需要为百分比指标设置目标，请使用 Target Compare 格式。

**Q: Dashboard Filter 和图表自身的物料范围是什么关系？**
A: Dashboard Filter 设定的是数据范围的上限。图表自身配置的物料范围会与 Dashboard Filter 取交集。也就是说，图表最终展示的数据，既要在图表自身配置的范围内，也要在 Dashboard Filter 的范围内。

**Q: 为什么交叉表格（Grid Table）中某些横向和纵向物料的组合不可选？**
A: 交叉表格对横向和纵向物料的组合有兼容性限制。例如，横向和纵向不能选择相同的物料层级（如都选 Profile），某些组合在业务逻辑上没有意义也不被支持。请参考本文中的兼容关系表选择合适的组合。

**Q: Commerce 平台的过滤项之间有联动关系，我应该按什么顺序设置？**
A: 建议按照从上到下的顺序设置：先选 Market，再选 Account，最后选 Category / Brand 等。因为下级过滤项的候选值会根据上级的选择自动更新。如果你先选了下级再改上级，下级的选择可能会被重置。

---

*本文档基于产品功能自动生成，如有疑问请联系产品团队。*