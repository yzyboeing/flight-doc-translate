# QRH 场景：机体、气源、防冰和通讯

## 适用场景

舱门、风挡、增压、座舱高度、气源、空调组件、发动机／机翼防冰、排雨和通讯系统检查单。

## 高复用术语与搭配

| English | 首选中文 | 备选中文 | 技术对象 | 文档类型 | 阶段／系统 | 典型搭配 | 使用边界 | 状态 | 把握度 |
|---|---|---|---|---|---|---|---|---|---|
| cargo door | 货舱门 | 货舱舱门 | 舱门 | QRH | 机体 | cargo door not secure | 不与登机门／勤务门合并 | 已对齐 | 高 |
| entry door | 登机门 | 入口门 | 舱门 | QRH | 机体 | entry door not closed | 采用客舱登机门语境 | 已对齐 | 高 |
| equipment door | 设备舱门 | 设备门 | 舱门 | QRH | 机体 | equipment door indication | 不泛化为所有维护口盖 | 已对齐 | 高 |
| service door | 勤务门 | 服务门 | 舱门 | QRH | 机体 | service door not closed | 与登机门分开 | 已对齐 | 高 |
| door handle | 舱门手柄 | 门手柄 | 控制件 | QRH | 机体 | handle in the closed position | 保留位置条件 | 已对齐 | 高 |
| closed and secure | 关闭锁好 | 关闭并锁定 | 状态 | QRH | 机体 | door is closed and secure | 不只译“关闭” | 已对齐 | 高 |
| cabin altitude warning | 座舱高度警告 | 客舱高度警告 | 警告状态 | QRH | 增压 | cabin altitude warning or rapid depressurization | 采用驾驶舱警告语境 | 已对齐 | 高 |
| rapid depressurization | 快速释压 | 快速失压 | 增压事件 | QRH | 增压 | warning or rapid depressurization | 与缓慢增压变化区分 | 已对齐 | 高 |
| cabin altitude | 座舱高度 | 客舱高度 | 参数 | QRH | 增压 | maintain cabin altitude | 驾驶舱技术用语优先“座舱” | 已对齐 | 高 |
| cabin differential pressure | 座舱压差 | 客舱压差 | 参数 | QRH | 增压 | maintain differential pressure | 不丢失 pressure | 已对齐 | 高 |
| outflow valve | 外流活门 | 排气活门 | 活门 | QRH | 增压 | outflow valve position | 与放气活门区分 | 已对齐 | 高 |
| bleed trip off | 引气跳开 | 引气跳开关断 | 系统状态 | QRH | 气源 | BLEED TRIP OFF | 灯名可保留英文标签 | 已对齐 | 高 |
| pack | 组件 | 空调组件 | 系统组件 | QRH | 气源／空调 | PACK switch | 固定标签可保留 PACK | 已对齐 | 高 |
| duct overheat | 管道过热 | 引气管道过热 | 系统状态 | QRH | 气源 | duct overheat indication | 是否补“引气”取决于章节对象 | 等义对照 | 中 |
| engine cowl anti-ice | 发动机整流罩防冰 | 发动机短舱防冰 | 防冰系统 | QRH | 防冰 | engine cowl anti-ice duct | 与机翼防冰区分 | 已对齐 | 高 |
| wing anti-ice valve open | 机翼防冰活门开 | 机翼防冰活门打开 | 活门状态 | QRH | 防冰 | L or R valve open | 灯名和左右标识按原文保留 | 已对齐 | 高 |
| window overheat | 风挡过热 | 风挡加温过热 | 系统状态 | QRH | 风挡加温 | WINDOW OVERHEAT | 不扩大为驾驶舱全部窗户 | 已对齐 | 高 |
| ACARS electrical power loss | ACARS 电源失效 | ACARS 失去电源 | 系统状态 | QRH | 通讯 | ACARS electrical power | ACARS 保留缩写 | 已对齐 | 高 |
| establish crew communications | 建立机组通讯 | 建立机组通信 | 机组协同 | QRH | 非正常 | establish communications | 不补写设备或顺序 | 已对齐 | 高 |
| passenger signs | 旅客信号牌 | 旅客信号 | 控制／指示 | QRH | 客舱协调 | passenger signs ON | 保留目标状态 | 已对齐 | 高 |

## 高复用句式框架

| English pattern | 中文框架 | 控制点 |
|---|---|---|
| X door is not closed and secure | X 门未关闭锁好 | 两个状态都保留 |
| continue manual operation to maintain X | 继续人工操作以保持 X | 保留方式和目的 |
| X valve is not in the commanded position | X 活门不在指令位置 | 不改成完全失效 |
| avoid conditions requiring X | 避开需要使用 X 的条件 | 不把建议范围扩大 |
| X switch — as needed | X 电门——按需 | 固定标签和目标状态分开 |

## 易混边界

- cabin altitude 是参数；cabin altitude warning 是警告状态。
- closed、latched、locked、secure 的状态范围不同，不得只用“关闭”覆盖。
- PACK 作为驾驶舱标签时可保留英文，作为系统组件叙述时可译“组件”。
- anti-ice system、anti-ice valve 和 anti-ice indication 分别是系统、活门和指示。
