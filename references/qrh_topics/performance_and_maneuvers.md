# QRH 场景：性能和机动

## 适用场景

飞行中性能、非正常形态性能、紧急下降、空速不可靠、颠簸穿越、交通／地形避让和其他非正常机动。具体数值和动作顺序必须回到当前来源，不进入本模块。

## 高复用术语与搭配

| English | 首选中文 | 备选中文 | 技术对象 | 文档类型 | 阶段／系统 | 典型搭配 | 使用边界 | 状态 | 把握度 |
|---|---|---|---|---|---|---|---|---|---|
| Performance Inflight | 空中性能 | 飞行中性能 | 性能章节 | QRH | 性能 | performance section | 栏目名称按当前资料统一 | 等义对照 | 中 |
| performance data | 性能数据 | 性能资料 | 数据 | QRH／FCOM | 性能 | approved performance data | 不从参考库带入数值 | 已对齐 | 高 |
| non-normal configuration landing distance | 非正常形态着陆距离 | 非正常构型着陆距离 | 性能数据 | QRH | 着陆性能 | landing distance table | 形态与构型按文体统一 | 已对齐 | 高 |
| landing distance table | 着陆距离表 | 着陆距离数据表 | 性能表 | QRH | 着陆性能 | check the table | 不改写为停机距离表 | 已对齐 | 高 |
| unreliable airspeed | 空速不可靠 | 不可靠空速 | 数据状态 | QRH | 飞行中性能 | flight with unreliable airspeed | 标题词序服从中文结构 | 已对齐 | 高 |
| turbulent air penetration | 穿越颠簸气流 | 颠簸气流穿越 | 飞行场景 | QRH／FCTM | 巡航 | penetration speed | 不简化为普通颠簸 | 已对齐 | 高 |
| emergency descent | 紧急下降 | 应急下降 | 非正常机动 | QRH | 机动 | emergency descent checklist | 与普通快速下降区分 | 已对齐 | 高 |
| traffic avoidance | 冲突避让 | 活动避让 | 非正常机动 | QRH／FCTM | 机动 | traffic avoidance maneuver | TCAS 语境需保持冲突含义 | 已对齐 | 高 |
| terrain avoidance | 地形避让 | 避让地形 | 非正常机动 | QRH／FCTM | 机动 | terrain avoidance maneuver | 与交通避让区分 | 等义对照 | 高 |
| loss of thrust | 失去推力 | 推力丧失 | 推进状态 | QRH | 性能 | single or multiple engines | 不自动等同发动机停车 | 已对齐 | 高 |
| engine inoperative | 发动机不工作 | 发动机失效 | 持续状态 | QRH | 性能 | one engine inoperative | 与 failure 事件分开 | 等义对照 | 中 |
| gear down | 起落架放下 | 放轮 | 构型 | QRH | 性能 | performance with gear down | 不省略构型条件 | 已对齐 | 高 |
| flaps extended | 襟翼放出 | 襟翼已放出 | 构型 | QRH | 性能 | performance with flaps extended | 与放出动作区分 | 已对齐 | 高 |
| maneuver margin | 机动裕度 | 操纵裕度 | 性能裕度 | QRH／FCTM | 进近／机动 | sufficient maneuver margin | 不扩写成具体速度规则 | 已对齐 | 高 |
| available airport | 可用机场 | 可供使用的机场 | 运行选择 | QRH | 非正常 | weather, fuel and available airports | 不擅自改成“合适机场” | 已对齐 | 高 |
| long range cruise | 远程巡航 | 远程巡航方式 | 性能方式 | QRH | 巡航 | use may be needed | 保留 may 的可能性 | 已对齐 | 高 |

## 高复用句式框架

| English pattern | 中文框架 | 控制点 |
|---|---|---|
| check the approved performance data | 查阅经批准的性能数据 | 不用术语库补写数值 |
| X may be needed | 可能需要 X | 不升级为必须 |
| if performance allows | 如果性能允许 | 保留性能条件 |
| maintain sufficient maneuver margin | 保持足够的机动裕度 | 不自行给出裕度数值 |
| the course of action is based on X | 后续措施根据 X 决定 | 保留全部并列因素 |

## 易混边界

- emergency descent 与一般快速下降不是同一程序概念。
- traffic avoidance、terrain avoidance 和 weather avoidance 的对象不同。
- engine failure 是事件，engine inoperative 是状态，loss of thrust 是性能／推力结果。
- landing distance、stopping distance 和 available runway distance 不得互换。
