# QRH 场景：检查单结构与动作

## 适用场景

检查单介绍、非正常检查单结构、条件和目的字段、记忆／参考／延迟项目、分支、转阅、完成状态、控制件动作与机组协同。

## 高复用术语与搭配

| English | 首选中文 | 备选中文 | 技术对象 | 文档类型 | 阶段／系统 | 典型搭配 | 使用边界 | 状态 | 把握度 |
|---|---|---|---|---|---|---|---|---|---|
| Quick Action Index | 快速反应索引 | 快速动作索引 | 检查单索引 | QRH | 通用 | QRH 快速反应索引 | 作为正式栏目名称使用 | 已对齐 | 高 |
| annunciated checklist | 显示检查单 | 有显示检查单 | 检查单类别 | QRH | 非正常 | 对应灯光或警报的检查单 | 不等同“正常检查单” | 已对齐 | 高 |
| unannunciated checklist | 非显示检查单 | 无显示检查单 | 检查单类别 | QRH | 非正常 | 非显示检查单索引 | 指没有相应警报指示 | 已对齐 | 高 |
| airplane effectivity statement | 飞机有效性说明 | 飞机适用性说明 | 适用性字段 | QRH | 通用 | 核实飞机有效性 | 与一般审查中的“机型适用性”区分 | 已对齐 | 高 |
| condition statement | 状况说明 | 条件说明 | 检查单字段 | QRH | 非正常 | 读出足够的状况说明 | 仅限字段名称 | 已对齐 | 高 |
| objective statement | 目的说明 | 目标说明 | 检查单字段 | QRH | 非正常 | 理解预期结果 | 不把性能目标统一译为“目的” | 已对齐 | 高 |
| memory item | 记忆项目 | 记忆动作 | 检查单项目 | QRH | 非正常 | 完成所有记忆项目 | 与参考项目区分 | 已对齐 | 高 |
| reference item | 参考项目 | 非记忆项目 | 检查单项目 | QRH | 非正常 | 执行参考项目 | 不误解为文献引用 | 已对齐 | 高 |
| additional information | 附加信息 | 补充信息 | 说明字段 | QRH | 非正常 | 阅读附加信息 | 不提升为动作项目 | 已对齐 | 高 |
| deferred item | 延迟项目 | 推迟项目 | 检查单项目 | QRH | 非正常 | 除延迟项目外完成 | 保留延迟范围 | 已对齐 | 高 |
| start a checklist | 检查单开始 | 开始执行检查单 | 检查单阶段 | QRH | 非正常 | 检查单开始条件 | 作栏目名与动作句时调整语序 | 等义对照 | 高 |
| do memory items | 执行记忆项目 | 完成记忆项目 | 机组动作 | QRH | 非正常 | 迅速完成记忆项目 | do 不机械译为“做” | 已对齐 | 高 |
| call for checklist | 叫出检查单 | 要求执行检查单 | 机组口令 | QRH | 非正常 | PF 叫出检查单 | 与朗读检查单区分 | 已对齐 | 高 |
| do initial actions | 执行起始动作 | 完成初始动作 | 机组动作 | QRH | 非正常 | 叫出检查单、执行起始动作 | 不改成记忆项目 | 已对齐 | 高 |
| do reference items | 执行参考项目 | 完成参考项目 | 机组动作 | QRH | 非正常 | 逐项执行参考项目 | 与记忆项目区分 | 已对齐 | 高 |
| Confirm step | “核实”步骤 | 确认步骤 | 双人确认 | QRH | 非正常 | 动作前口头达成一致 | QRH 特定概念；不是普通 verify | 已对齐 | 高 |
| areas of responsibility | 责任区 | 职责范围 | 机组分工 | QRH | 通用 | 各自责任区 | 与岗位名称分开 | 已对齐 | 高 |
| inoperative item | 不工作项目 | 失效项目 | 项目状态 | QRH | 非正常 | 项目不工作 | 事件用“失效”时另行处理 | 已对齐 | 高 |
| loss of indications | 失去指示 | 指示丧失 | 显示状态 | QRH | 非正常 | 部分或全部失去指示 | 不等同系统功能丧失 | 已对齐 | 高 |
| configuration check | 形态检查 | 构型检查 | 检查动作 | QRH | 非正常 | 完成形态检查 | 飞行形态优先用“形态” | 已对齐 | 高 |
| captain's discretion | 机长决断 | 机长酌情决定 | 决策权限 | QRH | 非正常 | 使用机长决断 | 不译成任意处置 | 已对齐 | 高 |
| response or action | 回答或动作 | 响应或动作 | 参考项目组成 | QRH | 非正常 | 读出回答或动作 | response 是否为口头回答需看栏目 | 等义对照 | 中 |
| amplifying information | 扩展信息 | 补充说明 | 解释信息 | QRH | 非正常 | 读出扩展信息 | 不提升为新动作 | 已对齐 | 高 |
| choose one | 选其一 | 选择一项 | 决策分支 | QRH | 通用 | 读出所有选项 | 必须保留完整分支 | 已对齐 | 高 |
| go to step X | 转阅第 X 步 | 转到第 X 步 | 内部跳转 | QRH | 通用 | 转阅指定步骤 | 不改变目标编号 | 已对齐 | 高 |
| go to the X checklist | 转阅 X 检查单 | 转到 X 检查单 | 跨检查单跳转 | QRH | 通用 | 转阅相关检查单 | 与“执行检查单”区分 | 已对齐 | 高 |
| checklist complete | 检查单完成 | 检查单已完成 | 完成状态 | QRH | 通用 | 完成符 | 与动作“完成检查单”区分 | 已对齐 | 高 |
| checklist complete except deferred items | 除延迟项目外，检查单完成 | 检查单完成，延迟项目除外 | 完成状态 | QRH | 非正常 | 延迟项目段之前 | 例外范围不可删除 | 已对齐 | 高 |
| redirection symbol | 转阅符 | 重定向符 | 检查单图标 | QRH | 通用 | 指向其他步骤或检查单 | 采用检查单栏目用语 | 已对齐 | 高 |
| separator symbol | 分隔符 | 分隔标志 | 检查单图标 | QRH | 通用 | 分开项目类别 | 不当作普通版面线 | 已对齐 | 高 |
| task divider symbol | 任务分隔符 | 任务分界符 | 检查单图标 | QRH | 通用 | 标识任务边界 | 保留任务范围 | 已对齐 | 高 |
| decision symbol | 决断符 | 选择符 | 检查单图标 | QRH | 通用 | 标识可选分支 | 与注意符区分 | 已对齐 | 高 |
| precaution symbol | 注意符 | 注意标志 | 检查单图标 | QRH | 通用 | 动作前必须考虑的信息 | 不等同 CAUTION 标题 | 已对齐 | 高 |
| checklist complete symbol | 检查单完成符 | 完成标志 | 检查单图标 | QRH | 通用 | 表示检查单结束 | 不遗漏结束范围 | 已对齐 | 高 |
| continued on next page | 下页续 | 续下页 | 续页标识 | QRH | 通用 | X 续 | 必须指出续页对象 | 已对齐 | 高 |
| plan to land at the nearest suitable airport | 计划在最近合适机场着陆 | 计划飞往最近合适机场着陆 | 运行计划 | QRH | 非正常 | plan to land | 不删 plan to | 已对齐 | 高 |
| land at nearest suitable airport | 在最近合适机场着陆 | 飞往最近合适机场着陆 | 运行指令 | QRH | 非正常 | land at nearest suitable | 不擅加“计划” | 已对齐 | 高 |
| immediate landing | 立即着陆 | 立即实施着陆 | 紧急指令 | QRH | 非正常 | immediate landing | 不弱化为“尽快” | 已对齐 | 高 |

## 动作与状态框架

| English pattern | 中文框架 | 控制点 |
|---|---|---|
| verify X is Y | 核实 X 在 Y 位／处于 Y 状态 | 不把核实改成执行移位 |
| move X to Y | 将 X 移至 Y 位 | 保留控制件和目标位置 |
| hold X in Y until Z | 将 X 保持在 Y 位，直至 Z | 终止条件必须紧跟 |
| pull X | 提起／拔出 X | 火警电门与跳开关动作不同 |
| rotate X to the stop and hold | 将 X 转到位并保持 | 保留到位和保持 |
| X (if engaged) — disengage | X（如接通）——脱开 | 条件不能删除 |
| X — as needed | X——按需 | 不补充使用标准 |
| do not accomplish X | 不要完成 X | 保留否定对象 |
| if time allows, verify X before Y | 如果时间允许，在 Y 前核实 X | 保留条件和先后关系 |

## 易混边界

- Confirm step 是 QRH 中的特定双人确认概念，不能仅凭普通词义处理。
- checklist complete 是状态；complete the checklist 是动作。
- go to 是逻辑跳转；continue 是在当前流程中继续。
- annunciated / unannunciated 与 normal / non-normal 是不同分类轴。
- plan to land、land at nearest suitable airport、land immediately 的紧迫程度不可合并。
