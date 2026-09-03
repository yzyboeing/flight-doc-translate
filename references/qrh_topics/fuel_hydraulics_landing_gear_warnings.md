# QRH 场景：燃油、液压、起落架和警告

## 适用场景

燃油量和供油、液压泵及压力、起落架位置和人工放轮、起飞／着陆形态及警告系统检查单。

## 高复用术语与搭配

| English | 首选中文 | 备选中文 | 技术对象 | 文档类型 | 阶段／系统 | 典型搭配 | 使用边界 | 状态 | 把握度 |
|---|---|---|---|---|---|---|---|---|---|
| fuel leak engine | 发动机燃油泄漏 | 发动机燃油漏油 | 燃油事件 | QRH | 燃油／发动机 | checklist title | 与一般机翼／油箱泄漏区分 | 已对齐 | 高 |
| fuel quantity indication inoperative | 燃油油量指示不工作 | 燃油量指示失效 | 指示状态 | QRH | 燃油 | quantity indication | 不等同燃油量本身异常 | 已对齐 | 高 |
| fuel temperature low | 燃油温度低 | 低燃油温度 | 参数状态 | QRH | 燃油 | FUEL TEMP LOW | 与低温限制值分开 | 已对齐 | 高 |
| fuel imbalance | 燃油不平衡 | 燃油量不平衡 | 分布状态 | QRH | 燃油 | maintain fuel balance | 不自动等同燃油泄漏 | 已对齐 | 高 |
| fuel crossfeed valve | 燃油交输活门 | 燃油交叉供油活门 | 活门 | QRH | 燃油 | valve position | 与选择器区分 | 已对齐 | 高 |
| crossfeed selector inoperative | 交输活门选择器不工作 | 燃油交输选择器不工作 | 控制件状态 | QRH | 燃油 | CROSSFEED SELECTOR INOPERATIVE | 不与活门本体合并 | 已对齐 | 高 |
| fuel pump low pressure | 燃油泵低压 | 燃油泵压力低 | 泵状态 | QRH | 燃油 | LOW PRESSURE light | 固定灯名可保留英文 | 等义对照 | 高 |
| hydraulic pump overheat | 液压泵过热 | 液压泵超温 | 泵状态 | QRH | 液压 | OVERHEAT light | 与低压状态区分 | 已对齐 | 高 |
| hydraulic pump low pressure | 液压泵低压 | 液压泵压力低 | 泵状态 | QRH | 液压 | system or standby pump | 必须保留系统／备用泵限定 | 已对齐 | 高 |
| standby hydraulic system | 备用液压系统 | 备用液压 | 系统 | QRH | 液压 | standby pump | standby 不译成“待机” | 已对齐 | 高 |
| gear disagree | 起落架不一致 | 起落架位置不一致 | 构型状态 | QRH | 起落架 | GEAR DISAGREE | 不擅自断言某一支柱位置 | 等义对照 | 中 |
| landing gear lever | 起落架手柄 | 起落架操纵手柄 | 控制件 | QRH | 起落架 | lever at UP or DN | 与实际起落架位置区分 | 已对齐 | 高 |
| landing gear lever jammed in the UP position | 起落架手柄卡在 UP 位 | 起落架手柄卡阻在收上位 | 控制件状态 | QRH | 起落架 | checklist title | 固定位置标签可保留英文 | 已对齐 | 高 |
| landing gear lever will not move up after takeoff | 起飞后起落架手柄不能移到 UP 位 | 起落架手柄不能移至收上位 | 控制件状态 | QRH | 起飞／起落架 | after takeoff | 保留起飞后条件 | 已对齐 | 高 |
| manual gear extension | 人工放起落架 | 起落架人工放出 | 非正常动作 | QRH | 起落架 | manual extension | 不等同正常放轮 | 已对齐 | 高 |
| partial or all gear up landing | 部分或全部起落架收上着陆 | 部分／全部起落架未放下着陆 | 着陆构型 | QRH | 着陆／起落架 | landing configuration | partial 和 all 都保留 | 已对齐 | 高 |
| landing configuration | 着陆形态 | 着陆构型 | 形态／警告标题 | QRH | 警告系统 | LANDING CONFIGURATION | 与具体形态错误事实分开 | 已对齐 | 高 |
| takeoff configuration warning | 起飞形态警告 | 起飞构型警告 | 警告状态 | QRH | 警告系统 | TAKEOFF CONFIGURATION | 与起飞形态本身区分 | 已对齐 | 高 |
| warning horn (intermittent) | 警告喇叭（间断的） | 间歇性警告喇叭 | 音响警告 | QRH | 警告系统 | intermittent horn | 保留间断特征 | 已对齐 | 高 |
| landing gear indicator light | 起落架指示灯 | 起落架位置指示灯 | 指示 | QRH | 起落架 | check indicator lights | 指示灯状态不等同机械位置 | 已对齐 | 高 |

## 高复用句式框架

| English pattern | 中文框架 | 控制点 |
|---|---|---|
| it is not possible to determine X | 无法确定 X | 不擅自选择一种状态 |
| verify sufficient fuel is available | 核实有足够燃油可用 | 保留 sufficient 和 available |
| maintain fuel balance | 保持燃油平衡 | 不自动规定泵构型 |
| check landing gear indicator lights | 检查起落架指示灯 | 只描述检查动作 |
| all / any / one or more | 全部／任一／一个或多个 | 范围量词逐项保留 |

## 易混边界

- fuel quantity indication inoperative 是指示问题，不等同 fuel quantity low。
- selector、valve 和 indication 是控制件、执行部件和指示，不得合并。
- landing gear lever position、indicator light 和实际起落架位置是三个证据层级。
- configuration warning 是警告，不自动证明构型实际处于某一状态。
