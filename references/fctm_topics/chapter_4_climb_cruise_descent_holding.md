# 第 4 章场景：爬升、巡航、下降和等待

## 适用场景

爬升推力与限制、改平、爬升速度、发动机结冰、经济／最大率／最大角爬升、单发爬升、巡航高度与速度、梯度爬升、低燃油温度、飘降、下降航径与计划、减速板、襟翼／起落架阻力、速度限制和等待。

## 高复用术语与搭配

| English | 优先中文 | 使用边界 |
|---|---|---|
| reduced climb thrust | 减推力爬升 | 与减推力起飞区分 |
| climb constraint | 爬升限制 | 保留限制来源和高度／速度对象 |
| low-altitude level-off | 低高度改平 | 高 |
| transition to climb | 过渡到爬升 | 高 |
| climb speed determination | 确定爬升速度 | 高 |
| engine icing during climb | 爬升过程中发动机结冰 | 高 |
| economy climb | 经济爬升 | 高 |
| economy climb schedule | 经济爬升计划 | 与速度计划按原文区分 |
| maximum-rate climb | 最大爬升率爬升 | 与最大角爬升区分 |
| maximum-angle climb | 最大爬升角爬升 | 与最大率爬升区分 |
| engine-inoperative climb | 一台发动机不工作爬升 | 状态语境 |
| maximum altitude | 最大高度 | 必须保留决定因素或限制语境 |
| optimum altitude | 最佳高度 | 与最大高度区分 |
| cruise speed determination | 确定巡航速度 | 高 |
| step climb | 梯度爬升 | 采用对照手册用语；其他体系若用“阶梯爬升”则进入确认 |
| low fuel temperature | 燃油温度低 | 状态标题语境 |
| cruise performance economy | 经济巡航性能 | 高 |
| engine-inoperative cruise | 发动机不工作巡航 | 与失效事件区分 |
| driftdown | 飘降 | 发动机不工作性能语境 |
| high-altitude high-speed flight | 高高度大速度飞行 | 采用对照手册标题用语 |
| ETOPS | ETOPS | 缩写按原文保留，首次展开服从来源 |
| polar operations | 极地飞行 | 高 |
| descent speed determination | 确定下降速度 | 高 |
| descent path | 下降航径 | 与下降率区分 |
| descent constraint | 下降限制 | 高 |
| speed intervention | 速度干预 | 仅适用于已安装该功能的构型 |
| descent preparation | 下降准备 | 高 |
| descent planning | 下降计划 | 高 |
| descent rate | 下降率 | 与下降角、航径区分 |
| top of descent (T/D) | 下降顶点（T/D） | 首次保留缩写；若来源用其他标识则照录 |
| idle descent | 慢车下降 | 推力状态语境 |
| speedbrake | 减速板 | 与扰流板、地面扰流板区分 |
| speedbrake extension | 减速板放出 | 过程或结果；动作可写“放出减速板” |
| flap extension | 放襟翼 | 下降／进近构型语境 |
| landing gear extension | 放起落架 | 下降／进近构型语境 |
| speed restriction | 速度限制 | 保留约束来源 |
| engine icing during descent | 下降过程中发动机结冰 | 高 |
| holding | 等待 | 程序语境 |
| holding airspeed | 等待速度 | 高 |
| procedure holding | 程序等待 | 与一般空中等待按来源区分 |
| FMC data unavailable | FMC 数据不可用 | 不扩写故障原因 |

## 高复用句式框架

| English pattern | 中文框架 | 控制点 |
|---|---|---|
| select a speed appropriate for X | 选择适合 X 的速度 | 不自行加入数值 |
| level off at X | 在 X 改平 | X 是高度、限制或事件时准确落词 |
| X is limited by Y | X 受 Y 限制 | 不倒置因果 |
| the optimum altitude is based on X | 最佳高度以 X 为基础 | 不误写为最大批准高度 |
| initiate the descent at X | 在 X 开始下降 | 保留时点或条件 |
| remain on the descent path | 保持在下降航径上 | 不译为保持下降率 |
| use speedbrakes if required | 如需要，使用减速板 | 不补写放出量 |
| additional drag may be required | 可能需要额外阻力 | 保留可能性，不擅自指定构型 |
| reduce the selected speed before X | 在 X 前减小选择的速度 | 保留先后关系 |
| holding speed is available from the FMC | FMC 提供等待速度 | 不暗示所有构型均可用 |
| if FMC data is unavailable, X | 如果 FMC 数据不可用，X | 保留替代条件 |
| engine icing may affect X | 发动机结冰可能影响 X | 保留不确定性和影响对象 |

## 易混边界

- `maximum altitude / optimum altitude` 分别是最大高度和最佳高度，不能用“最适高度”覆盖两者。
- `maximum-rate climb / maximum-angle climb` 分别追求爬升率和爬升角。
- `descent path / descent rate / descent angle` 分别是下降航径、下降率和下降角。
- `driftdown` 是发动机不工作性能语境中的“飘降”，不是一般下降。
- `step climb` 在本对照资料中采用“梯度爬升”；若当前材料或用户体系明确用“阶梯爬升”，进入术语确认而非静默替换。
