# QRH 场景：电气、发动机、APU 和防火

## 适用场景

电源、发电机、发动机和 APU 状态、火警、烟雾、异味、过热、灭火及推进系统非正常检查单。

## 高复用术语与搭配

| English | 首选中文 | 备选中文 | 技术对象 | 文档类型 | 阶段／系统 | 典型搭配 | 使用边界 | 状态 | 把握度 |
|---|---|---|---|---|---|---|---|---|---|
| standby power off | 备用电源关 | 备用电源断开 | 电源状态 | QRH | 电气 | STANDBY PWR OFF | 灯名可保留英文 | 等义对照 | 中 |
| generator drive disconnect | 发电机传动装置断开 | 发电机驱动断开 | 机械／电气动作 | QRH | 电气 | generator drive disconnect switch | 与 generator off bus 区分 | 等义对照 | 中 |
| source off | 电源断开 | 电源源断开 | 电源状态 | QRH | 电气 | SOURCE OFF | 固定灯名优先保留英文 | 风格候选 | 中 |
| transfer bus off | 转换汇流条断电 | 转换汇流条关断 | 电源状态 | QRH | 电气 | TRANSFER BUS OFF | 不简化成一般失电 | 等义对照 | 中 |
| APU fire | APU 火警 | 辅助动力装置火警 | 火警事件 | QRH | APU／防火 | APU FIRE | 首次需要时展开 APU | 已对齐 | 高 |
| engine fire | 发动机火警 | 发动机着火 | 火警警告／事件 | QRH | 发动机／防火 | ENGINE FIRE | 标题语境采用“火警”；事实叙述可为“着火” | 已对齐 | 高 |
| engine fire on the ground | 地面发动机火警 | 发动机地面火警 | 火警场景 | QRH | 地面／发动机 | checklist title | 保留地面条件 | 已对齐 | 高 |
| engine overheat | 发动机过热 | 发动机过热警告 | 系统状态 | QRH | 发动机 | ENGINE OVERHEAT | 不等同发动机火警 | 已对齐 | 高 |
| engine high vibration | 发动机振动值高 | 发动机高振动 | 系统状态 | QRH | 发动机 | high vibration indication | 保留“值高”状态含义 | 已对齐 | 高 |
| engine limit or surge or stall | 发动机限制、喘振或失速 | 发动机限制值、喘振或失速 | 推进事件 | QRH | 发动机 | checklist title | 三种情况不得删并列项 | 已对齐 | 高 |
| engine severe damage or separation | 发动机严重损坏或飞脱 | 发动机严重损坏或分离 | 推进事件 | QRH | 发动机 | severe damage or separation | separation 不与关车混同 | 已对齐 | 高 |
| engine tailpipe fire | 发动机尾喷管起火 | 发动机尾管着火 | 火情 | QRH | 发动机／地面 | tailpipe fire | 与发动机火警警告区分 | 已对齐 | 高 |
| loss of thrust on both engines | 双发失去推力 | 两台发动机推力丧失 | 推进状态 | QRH | 发动机 | loss of thrust | 不自动译为双发停车 | 已对齐 | 高 |
| smoke, fire or fumes | 烟雾、着火或异味 | 烟雾、火情或烟气 | 综合事件 | QRH | 防火 | checklist family | 三项范围均保留 | 已对齐 | 高 |
| cargo fire | 货舱火警 | 货舱着火 | 火警警告／事件 | QRH | 防火 | cargo fire warning | 标题和事实语境区分 | 已对齐 | 高 |
| fire bottle discharged | 灭火瓶释放 | 灭火瓶已释放 | 灭火状态 | QRH | 防火 | bottle discharged indication | 与人工释放动作区分 | 等义对照 | 中 |
| fire switch | 火警电门 | 灭火手柄 | 控制件 | QRH | 防火 | engine or APU fire switch | 按机型控制件名称统一 | 已对齐 | 高 |
| override and pull | 超控并提起 | 按压超控后提起 | 控制动作 | QRH | 防火 | fire switch action | 不拆掉动作顺序 | 已对齐 | 高 |
| rotate to the stop and hold | 转到位并保持 | 转至止动位并保持 | 控制动作 | QRH | 防火 | related fire switch | 保留到位和保持 | 已对齐 | 高 |
| engine start lever | 发动机起动手柄 | 发动机启动手柄 | 控制件 | QRH | 发动机 | lever at CUTOFF | 与 start switch 区分 | 已对齐 | 高 |
| CUTOFF | 切断位 | CUTOFF 位 | 目标位置 | QRH | 发动机 | start lever CUTOFF | 需要驾驶舱辨识时保留英文 | 已对齐 | 高 |

## 高复用句式框架

| English pattern | 中文框架 | 控制点 |
|---|---|---|
| one or more of these occur | 出现下列一种或多种情形 | 并列范围不得缩小 |
| fire is observed or indicated | 观察到或显示火警 | 区分目视发现与系统指示 |
| affected engine | 受影响的发动机 | 不自行指定左右 |
| related fire switch | 相关的火警电门 | 指代必须可回溯 |
| if X is needed | 如果需要 X | 不擅自增加判定标准 |

## 易混边界

- engine fire 可指警告标题或真实火情，中文随语境选择“火警／着火”。
- loss of thrust 不必然等于 engine shutdown 或 engine failure。
- fire switch、start switch 和 start lever 是不同控制件。
- discharged 是状态；discharge 作动词时需要明确动作主体。
