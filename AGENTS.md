# AGENTS.md — flight-doc-translate

任何 AI 助手接手本仓库时**首先读本文件**，再按 `SKILL.md` 执行。本文件只讲能力边界与仓库红线，翻译规则一律以 `SKILL.md` 及 `references/` 为准。

## 一、先实测能力，不要假设

对应 `preflight_review.md` 能力自检的四项：

```bash
ls references/ scripts/ && python3 scripts/validate_package.py   # 能读能跑？
NODE_PATH=<装有 docx 的 node_modules> node -e "require('docx')"   # ① DOCX 生成库
python3 -c "import fitz"; which pdftoppm pdfimages               # ② 源 PDF 渲染
which soffice                                                     # ③ DOCX → 逐页图像
```

**注意 ①**：可使用本仓库 package.json 安装 docx，或用 NODE_PATH 指向环境中已安装的兼容依赖。先实测，不根据目录位置断言可用性。

**第 ④ 项（CJK 字体）没有一行命令能测。** 必须按 `docx_production.md` 实际生成一页含中文、全角标点、负号、温度符号的烟雾测试，渲染成图像后**目视**确认无方框、缺字、错误回退。不得只看字体名或系统安装列表就下结论。

四项全过 → **完整路线**。缺任一项 → **受限路线**，按 `preflight_review.md` 的规定先向用户说明缺失能力和交付影响。

**永远不要编造执行结果。** 未做渲染目检就明说未做，并列出因此未覆盖的检查项。

## 二、两条路线各能交付什么

| | 完整路线 | 受限路线 |
|---|---|---|
| 读原文、提交《初始翻译方案》 | 是 | 是 |
| 全文翻译与双遍复核 | 是 | 是 |
| 生成 DOCX | 是 | 否 |
| 逐页视觉 QA | 是 | 否 |
| 称「终稿」 | 是 | **否，只能是明确标记的结构性草稿** |

**不得用纯文本或 Markdown 冒充约定的 DOCX 成品。** 未经用户接受不得降级交付。

## 三、规则真源与加载顺序

每次任务完整读取：`references/fidelity.md`（内容最高优先级）→ `references/standing_decisions.md`（长期决策，已有结论不得重复提问）→ `references/source_authority.md`（事实来源与措辞优先级）。

正式资料另读 `references/preflight_review.md`；需要生成或校订 DOCX 时再读 `references/docx_production.md`。其余按 `SKILL.md`「按任务加载参考资料」一节定向加载，**不得因孤立词命中就加载全部参考文件**。

优先级：`fidelity.md` 中未被 `standing_decisions.md` 明确写明「覆盖」的条款始终是硬约束。**SD 编号只表示关联，可能是收紧也可能是澄清，不自动代表放宽。**

## 四、通用工作约定（本仓库适用部分）

- 回答前先检查前提：未经证实的前提、逻辑跳跃、关键信息缺失、概念混淆、把推测当事实。有问题先指出。
- 明确区分：已确认事实／合理推测／建议／无法核实。文档现行性、机型适用性属于典型的「无法独立核实」项，如实说明，不替用户假设。
- **本 skill 有两个硬性停止关口**（初始方案、终稿前确认），不得跳过，除非用户明确要求。除此之外正常做完，不自己发明审批关口。
- 已在 `standing_decisions.md` 有结论的问题不重复询问。
- 不处理密码、token 或登录流程。
- 不使用子代理、委派或并行代理，除非用户明确要求。

> 以上采用 `AGENTS-common.md` 的第 1、2、3、4、5、7、8、9 条。规范版本见公开仓库 `flight-notes-toolkit/prompt/AGENTS-common.md`（raw：`https://raw.githubusercontent.com/yzyboeing/flight-notes-toolkit/main/prompt/AGENTS-common.md`）。本节是按本仓库裁剪的副本——**条目编号固定**，从上面这行就能看出哪几条被省略了。修改总约定后需回头核对五份。

## 五、本仓库红线

1. **本仓库是公开的。** 只保存工作流、短术语和抽象句式；**不得包含**源 PDF、抽取文本、页面图像、连续手册正文、具体运行限制值、组织身份、内部编号、机号、本地路径或文件哈希。
2. **推送前跑 `python3 scripts/validate_package.py`。** CI 的 `--structural-only` 仅覆盖包结构等公开检查，不替代本机完整发布检查。 它包含组织身份检查，关键词表读取仓库外的 `~/.leakscan-keywords` 或 `FLIGHT_DOC_LEAKSCAN_KEYWORDS` 指定路径。**关键词表缺失时校验器会报错并非零退出——那是设计如此，不要绕过。**
3. **忠实性六条**以 `references/fidelity.md` 为准，此处不复述。违反任一条即为不合格译本。
4. **原文疑点照译 + 报告**：疑似笔误、内部矛盾、错号一律照原文译，不加译注（SD-3），进终稿前确认与交付说明的「原文疑点清单」。**不得静默改正，也不得静默略过。**
5. **译本不得作为运行依据。** 交付说明必须原样包含「本译文未经技术复核，仅供学习参考，不得作为运行依据。」按 SD-4 该声明不写入纸面，但交付说明中是硬约束。
6. **改动能否持久，取决于环境，先确认再承诺**：
   - **Codex（本机 `~/.codex/skills/flight-doc-translate/`）**：加载目录可能是安装副本、符号链接或 Git 检出，先实测；永久规则在正式仓库修改并验证发布，再从确定提交同步安装。修改副本不等于已发布。
   - **Claude 网页端（`/mnt/skills/…`）**：该目录的改动**只在当次会话有效**，不跨会话。规则变更须产出增补包由用户替换一次，**不得暗示会自动生效**。
   - 两个环境的副本会各自漂移。改完一侧后按 `reference_ingestion.md` 第三阶段第 4 条核对另一侧，不要假定已同步。
7. **推送前先 `git fetch` 比对远端。**
