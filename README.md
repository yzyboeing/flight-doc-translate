# flight-doc-translate

跨 AI 统一入口：[AI_INDEX.md](https://github.com/yzyboeing/flight-notes-toolkit/blob/main/AI_INDEX.md)。版本化 Skill 包使用本仓库 Releases 中的 `skill-vX.Y.Z` 标签；不要与配置版本混用。安装、环境检查与更新方式见 [分发说明](https://github.com/yzyboeing/flight-notes-toolkit/blob/main/DISTRIBUTION.md)。私有包及资料仍受本仓库的保密和授权边界约束。

用于将英文航空技术资料翻译为来源忠实、术语一致、版式经过逐页检查的中文 DOCX，也可依据英文原文校订已有中文译稿。

## 核心特点

- 默认双确认：先提交《初始翻译方案》，确认后执行；完成草稿和首轮视觉检查后，再进行终稿前确认。
- 非术语类长期选择统一写入 [长期决策记录](references/standing_decisions.md)，确认关口不重复询问已有结论。
- 英文原文决定技术事实、条件、情态、数字和适用范围，不用术语库补写原文没有的内容。
- 先识别 FCTM、QRH、FCOM、SOP、法规或事故调查等文档类型，再使用对应中文表达；不同文体不能相互强化或稀释。
- 将 FCTM 第 1—8 章重构为八个场景模块，覆盖综合信息、地面操作、起飞和起始爬升、爬升／巡航／下降／等待、进近和复飞、着陆、机动飞行及非正常操作。
- 将 QRH 表达按检查单结构及系统重构为六个模块，覆盖检查单字段、控制件状态、条件分支、机组协同和主要系统术语。
- 翻译时根据材料内容和涉及范围按需加载相关模块，使用其中的高复用术语、动作搭配、句式框架和易混边界；不会把无关章节或运行数值带入译文。
- 每份文档定稿并完成最终 QA 后，复盘术语、句式、歧义、版式和检查经验；只把经过验证、可复用且已脱敏的经验回写到 Skill，没有合格经验时不制造条目。
- 保留原图、表格、警告层级、版权和出口管制标识，并对生成的 DOCX 做逐页渲染检查。

## 工作系统设计

本 Skill 按“微型 Harness”组织，入口只保留每次任务都必须知道的主干，细节按需加载：

| 层 | 仓库中的实现 | 解决的问题 |
|---|---|---|
| 信息边界 | `SKILL.md` 的 `description` + `evals/trigger_cases.yaml` | 哪些真实说法应触发，哪些相邻任务不应误触发 |
| 执行编排 | `SKILL.md` 五步流程 + `preflight_review.md` | 高风险翻译如何串联两次确认和内部 QA |
| 参考状态 | `references/` 的文体、场景和系统路由 | 大量资料放在哪里、什么时候加载，避免整库进入上下文 |
| 工具系统 | `scripts/` | 将裁图、配色、页面样式和包检查等重复动作固化 |
| 失败恢复 | `SKILL.md` 的“异常与失败” | 缺资料、越界或执行失败时默认停在哪里，禁止假装成功 |
| 评估观测 | `evals/` + `scripts/validate_package.py` | 如何检查触发、忠实性、文体路由、版式与失败行为 |

## 验证

```bash
python3 scripts/validate_package.py
python3 <skill-creator>/scripts/quick_validate.py .
```

`evals/trigger_cases.yaml` 保存真实口吻的应触发与不应触发用例；`evals/translation_cases.yaml` 保存语义、版式和失败恢复用例。评测按行为与失败条件判断，不要求输出固定措辞。实质改动应覆盖相应案例，并至少真实运行一次成功路径和一次故意破坏后的失败路径。

## FCTM 场景表达模块

总入口是 [FCTM 中文用法路由](references/fctm_zh_usage.md)。八个模块分别覆盖：

1. [综合信息](references/fctm_topics/chapter_1_general_information.md)
2. [地面操作](references/fctm_topics/chapter_2_ground_operations.md)
3. [起飞和起始爬升](references/fctm_topics/chapter_3_takeoff_initial_climb.md)
4. [爬升、巡航、下降和等待](references/fctm_topics/chapter_4_climb_cruise_descent_holding.md)
5. [进近和复飞](references/fctm_topics/chapter_5_approach_missed_approach.md)
6. [着陆](references/fctm_topics/chapter_6_landing.md)
7. [机动飞行](references/fctm_topics/chapter_7_maneuvers.md)
8. [非正常操作](references/fctm_topics/chapter_8_non_normal_operations.md)

每个模块包含适用场景、高复用术语与搭配、短句式框架及易混边界。章号用于组织和检索，不表示其他待译材料必须采用相同章节结构。

## QRH 检查单表达模块

总入口是 [QRH 中文用法路由](references/qrh_zh_usage.md)。六个模块分别覆盖：

1. [检查单结构与动作](references/qrh_topics/checklist_structure.md)
2. [机体、气源、防冰和通讯](references/qrh_topics/airframe_air_anti_ice_communications.md)
3. [电气、发动机、APU 和防火](references/qrh_topics/electrical_engines_apu_fire.md)
4. [飞控、仪表和导航](references/qrh_topics/flight_controls_instruments_navigation.md)
5. [燃油、液压、起落架和警告](references/qrh_topics/fuel_hydraulics_landing_gear_warnings.md)
6. [性能和机动](references/qrh_topics/performance_and_maneuvers.md)

来源分层见 [来源权威与文体路由](references/source_authority.md)，双语手册维护见 [手册导入流程](references/reference_ingestion.md)，稳定分歧见 [术语冲突与决策边界](references/terminology_conflicts.md)，DOCX 生成与字体／图层检查见 [DOCX 制作与视觉 QA](references/docx_production.md)。

## 安装

将整个 `flight-doc-translate` 文件夹复制到 Codex skills 目录，例如 `~/.codex/skills/flight-doc-translate`，然后以 `$flight-doc-translate` 调用。默认允许根据翻译请求自动选择该 skill。

## 内容边界

仓库不包含任何源手册 PDF、抽取文本、页面图像、连续手册正文、具体运行限制、内部编号、机号或组织身份信息。术语和短语仅用于提高翻译一致性，不构成现行程序、运行批准或机型资格依据。

对话交付说明末尾必须保留：**本译文未经技术复核，仅供学习参考，不得作为运行依据。** 按现行长期决策，该声明不写入译本文件。

## 可移植性与自动检查

Node.js 环境可在本仓库运行 `npm install` 安装 docx。Python 图像处理需要 Pillow，PDF 提取需要 PyMuPDF；页面渲染需要 Poppler，DOCX 转换需要 LibreOffice 或经过实测的等效工具。字体和逐页视觉检查按 references/docx_production.md 执行。

支持 Skill 的环境安装完整仓库；其他代理完整读取 SKILL.md 及当前任务引用的文件。仅聊天环境可协助讨论、翻译草稿与审核，不因此获得本机文件、执行或渲染能力。

CI 运行 `python3 scripts/validate_package.py --structural-only` 和脚本检查，不携带个人组织关键词。发布前仍必须在本机使用仓库外的关键词文件运行默认完整检查；未执行的隐私检查不能标为通过。安装记录来源提交，备份放在 Skill 发现目录之外。

自有原创的工具与工作流采用 MIT 许可证。第三方术语、资料及其他权利仍受原许可约束；此许可证不授权传播源手册或公司材料。
