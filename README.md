# flight-doc-translate

用于将英文航空技术资料翻译为来源忠实、术语一致、版式经过逐页检查的中文 DOCX，也可依据英文原文校订已有中文译稿。

## 核心特点

- 默认双确认：先提交《初始翻译方案》，确认后执行；完成草稿和首轮视觉检查后，再进行终稿前确认。
- 英文原文决定技术事实、条件、情态、数字和适用范围，不用术语库补写原文没有的内容。
- 将 FCTM 第 1—8 章重构为八个场景模块，覆盖综合信息、地面操作、起飞和起始爬升、爬升／巡航／下降／等待、进近和复飞、着陆、机动飞行及非正常操作。
- 翻译时根据材料内容和涉及范围按需加载相关模块，使用其中的高频术语、动作搭配、句式框架和易混边界；不会把无关章节或运行数值带入译文。
- 每份文档定稿并完成最终 QA 后，复盘术语、句式、歧义、版式和检查经验；只把经过验证、可复用且已脱敏的经验回写到 Skill，没有合格经验时不制造条目。
- 保留原图、表格、警告层级、版权和出口管制标识，并对生成的 DOCX 做逐页渲染检查。
- 区分航空技术文档翻译与中文个人学习笔记整理。

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

每个模块包含适用场景、高频术语与搭配、短句式框架及易混边界。章号用于组织和检索，不表示其他待译材料必须采用相同章节结构。

## 安装

将整个 `flight-doc-translate` 文件夹复制到 Codex skills 目录，例如 `~/.codex/skills/flight-doc-translate`，然后以 `$flight-doc-translate` 调用。默认允许根据翻译请求自动选择该 skill。

## 内容边界

仓库不包含任何源手册 PDF、连续手册正文、具体运行限制或组织身份信息。术语和短语仅用于提高翻译一致性，不构成现行程序、运行批准或机型资格依据。

最终译文必须保留声明：**本译文未经技术复核，仅供学习参考，不得作为运行依据。**
