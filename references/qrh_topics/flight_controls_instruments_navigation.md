# QRH 场景：飞控、仪表和导航

## 适用场景

自动驾驶、自动油门、飞行操纵、安定面、飞行仪表、显示、空速、高度、惯导、GPS、CDU 和飞行管理系统检查单。

## 高复用术语与搭配

| English | 首选中文 | 备选中文 | 技术对象 | 文档类型 | 阶段／系统 | 典型搭配 | 使用边界 | 状态 | 把握度 |
|---|---|---|---|---|---|---|---|---|---|
| autopilot | 自动驾驶 | 自动驾驶仪 | 自动飞行系统 | QRH | 自动飞行 | autopilot engaged | 系统或控制状态按句法选择 | 已对齐 | 高 |
| autopilot disengage | 自动驾驶脱开 | 脱开自动驾驶 | 控制动作 | QRH | 自动飞行 | if engaged, disengage | 不译成断电 | 已对齐 | 高 |
| autothrottle | 自动油门 | 自动推力 | 自动飞行系统 | QRH | 自动飞行 | autothrottle engaged | 737 语境优先“自动油门” | 已对齐 | 高 |
| autothrottle disengage | 自动油门脱开 | 脱开自动油门 | 控制动作 | QRH | 自动飞行 | if engaged, disengage | 与断开电源区分 | 已对齐 | 高 |
| runaway stabilizer | 安定面失控 | 安定面非指令运动 | 飞控事件 | QRH | 飞行操纵 | checklist title | 标题采用对照用语；描述时保留具体运动 | 已对齐 | 高 |
| jammed or restricted flight controls | 飞行操纵卡阻或受限 | 飞行操纵卡滞或受限 | 飞控状态 | QRH | 飞行操纵 | overpower jammed system | 卡阻与受限并列不可删除 | 已对齐 | 高 |
| flight control low pressure | 飞行操纵低压 | 飞控低压 | 液压／飞控状态 | QRH | 飞行操纵 | LOW PRESSURE light | 系统灯名可保留英文 | 等义对照 | 中 |
| airspeed unreliable | 空速不可靠 | 空速指示不可靠 | 仪表状态 | QRH | 飞行仪表 | AIRSPEED UNRELIABLE | 不自动补成单一仪表失效 | 已对齐 | 高 |
| stick shaker deactivation | 抑制抖杆器 | 解除抖杆 | 警告装置动作 | QRH | 飞行仪表 | by pulling circuit breaker | 保留实现方式和对象 | 已对齐 | 高 |
| circuit breaker | 跳开关 | 断路器 | 电气保护件 | QRH | 通用 | pull the circuit breaker | 驾驶舱程序语境优先“跳开关” | 已对齐 | 高 |
| GPS data unreliable | GPS 数据不可靠 | GPS 资料不可靠 | 导航数据状态 | QRH | 导航 | GPS DATA UNRELIABLE | GPS 保留缩写 | 已对齐 | 高 |
| CDU display fail | CDU 显示失效 | CDU 显示故障 | 显示状态 | QRH | 飞行管理 | CDU display failure | 不等同整部 CDU 失效 | 等义对照 | 中 |
| CDS fault | CDS FAULT | CDS 故障 | 固定警报／系统状态 | QRH | 显示 | CDS FAULT indication | 固定标签优先保留英文 | 已对齐 | 高 |
| IRS alignment | IRS 校准 | 惯导校准 | 导航状态 | QRH | 导航 | verify alignment complete | IRS 保留缩写 | 已对齐 | 高 |
| flight director mode | 飞行指引仪方式 | 飞行指引方式 | 自动飞行方式 | QRH | 自动飞行 | proper mode selected | 不省略 mode | 已对齐 | 高 |
| verify that the thrust is symmetrical | 核实推力对称 | 核实对称推力 | 状态核实 | QRH | 飞行操纵 | thrust is symmetrical | 这是核实状态，不是调推力指令 | 已对齐 | 高 |

## 高复用句式框架

| English pattern | 中文框架 | 控制点 |
|---|---|---|
| X (if engaged) — disengage | X（如接通）——脱开 | 保留构型／状态条件 |
| verify that X is symmetrical | 核实 X 对称 | 不改成执行调节 |
| X is unreliable | X 不可靠 | 不擅自断言完全失效 |
| X indication is inoperative | X 指示不工作 | 指示失效不等于系统失效 |
| select or verify mode X | 选择或核实 X 方式 | 两个动作必须并列保留 |

## 易混边界

- airspeed unreliable 是信息可靠性问题，不等同 airspeed indication inoperative。
- indication failure、display failure 和 system failure 的失效对象不同。
- disengage 多用于自动飞行系统；disconnect 是否译“断开”取决于连接对象。
- verify symmetrical thrust 是状态核实，不能译成“将推力调至对称”。
