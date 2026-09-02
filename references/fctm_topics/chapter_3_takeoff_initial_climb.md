# 第 3 章场景：起飞和起始爬升

## 适用场景

起飞剖面、襟翼和速度、推力调定、起飞滑跑、抬头和离地、侧风起飞、减推力／减功率、低能见度和不利跑道、中断起飞、全发或单发起始爬升、收襟翼和减噪起飞。

## 高频术语与搭配

| English | 优先中文 | 使用边界 |
|---|---|---|
| takeoff profile | 起飞剖面 | 保留所适用的 FMC／机型条件 |
| takeoff flap setting | 起飞襟翼调定 | 高 |
| takeoff speed | 起飞速度 | 具体 V 速度保持符号 |
| takeoff thrust | 起飞推力 | 高 |
| thrust management | 推力管理 | 高 |
| thrust setting | 推力调定 | 动作或目标值按句法选择 |
| initiating takeoff roll | 开始起飞滑跑 | 高 |
| takeoff roll | 起飞滑跑 | 高 |
| rolling takeoff | 滑跑起飞 | 与静止起飞区分 |
| standing takeoff | 原地起飞 | 与滑跑起飞对比时采用 |
| rotation | 抬头 | 起飞动作；不要笼统译为“旋转” |
| rotation speed | 抬头速度 | 不与 `VR` 数值或符号混写 |
| pitch rate | 俯仰率 | 高 |
| liftoff | 离地 | 高 |
| center-of-gravity effect | 重心（CG）效应 | 首次可保留缩写 |
| crosswind takeoff | 侧风起飞 | 高 |
| crosswind takeoff guideline | 起飞侧风指标 | `guideline` 不得自动写成限制值 |
| directional control | 方向控制 | 高 |
| gusty wind | 阵风 | 高 |
| strong crosswind | 大侧风 | 不自动等同于超限侧风 |
| reduced takeoff thrust | 减推力起飞推力 | 假定温度法语境；与固定减功率区分 |
| assumed temperature method (ATM) | 假定温度法（ATM） | 首次保留缩写 |
| derated takeoff thrust | 减功率起飞推力 | 固定减功率语境 |
| fixed derate | 固定减功率 | 不与 ATM 合并 |
| improved climb performance takeoff | 改进爬升性能起飞 | 高 |
| low visibility takeoff | 低能见度起飞 | 高 |
| adverse runway condition | 不利跑道条件 | 保留来源对道面状态的定义 |
| rejected takeoff (RTO) | 中断起飞（RTO） | 不译为“拒绝起飞” |
| rejected takeoff decision | 中断起飞决策 | 高 |
| rejected takeoff maneuver | 中断起飞机动 | 与决策阶段分开 |
| go / stop decision | 继续／停止决策 | 保留二选一关系和临界语境 |
| operational margin | 操作裕度 | 与性能裕度、限制值区分 |
| initial climb | 起始爬升 | 高 |
| all engines operating | 双发工作 | 只适用于双发飞机相同标题语境 |
| roll mode | 横滚方式 | 自动飞行方式语境 |
| pitch mode | 俯仰方式 | 自动飞行方式语境 |
| autopilot engagement | 接通自动驾驶 | 描述动作，不写成自动驾驶“连接” |
| flap retraction schedule | 襟翼收上计划 | 与单个收襟翼动作分开 |
| flap retraction | 收襟翼／襟翼收上 | 过程和完成状态按句法选择 |
| noise abatement takeoff | 减噪起飞 | 具体程序标识按原文保留 |
| engine failure | 发动机失效 | 事件；与不工作状态区分 |
| engine failure recognition | 识别发动机失效 | 保留识别动作 |
| one engine inoperative | 一台发动机不工作 | 状态 |
| positive rate of climb | 正上升率 | 若原文要求指示确认，必须保留 |
| acceleration height | 增速高度 | 高 |
| thrust reduction height | 减推力高度 | 与增速高度不得合并 |

## 高频句式框架

| English pattern | 中文框架 | 控制点 |
|---|---|---|
| advance the thrust levers to X | 将推力手柄前推至 X | 保留目标位置或推力基准 |
| allow the engines to stabilize before X | 在 X 前使发动机稳定 | 保留动作先后，不补写时间 |
| initiate a smooth, continuous rotation | 柔和、连续地开始抬头 | 保留两个方式修饰语 |
| maintain directional control with X | 使用 X 保持方向控制 | 保留操纵手段 |
| use into-wind control input as needed | 按需使用迎风操纵输入 | 不增加幅度 |
| the decision to reject must be made before X | 必须在 X 前作出中断起飞决策 | 保留临界条件和强制性 |
| if the takeoff is continued, X | 如果继续起飞，X | 不省略条件分支 |
| after liftoff, maintain X | 离地后保持 X | 不提前动作 |
| when a positive rate is indicated, X | 指示正上升率后，X | 保留“指示”和确认条件 |
| retract the flaps on schedule | 按计划收襟翼 | 不补写速度或高度数值 |
| an engine failure may cause X | 发动机失效可能导致 X | 保留可能性和事件性质 |
| one-engine-inoperative performance is based on X | 一台发动机不工作性能以 X 为基础 | 不泛化到双发工作情况 |

## 易混边界

- `reduced thrust / derated thrust / fixed derate` 分别是减推力、减功率推力和固定减功率，不应统一成“减推力”。
- `rotation / liftoff / initial climb` 是抬头、离地和起始爬升三个连续但不同的阶段。
- `RTO decision / RTO maneuver` 分别指决策与动作执行。
- `acceleration height / thrust reduction height` 可能重合，也可能不同；译文必须保持两个技术概念。
- `engine failure / one engine inoperative` 分别偏向失效事件和一台发动机不工作的持续状态。
