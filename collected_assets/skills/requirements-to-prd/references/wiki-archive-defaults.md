# 飞书知识库归档约定（requirements-to-prd）

[English](wiki-archive-defaults.en.md)

> **性质**：公开仓库内**仅含占位符** `<YOUR_*>`。维护者若要在系统提示词里写死**自己的**真实 `space_id`/父节点，请用**未跟踪的本地文件**或私有仓库副本，**勿**将真实租户标识推送到公开 Git。  
> **对外分发本技能时**：对方要把 PRD 写入**自己的**知识库，须由**对方**提供 `space_id`、父节点 token（或 wiki URL 供解析）；**不得**假设对方与你的私有落点一致。  
> **换团队/换知识库**时须由**当前用户**提供新的 `space_id`、父节点 `wiki token`，或从知识库 URL 用 `lark-cli wiki spaces get_node` 解析（见 [lark-wiki-SKILL.md](lark-wiki-SKILL.md)）。

## 与用户确认清单（执行写入前）

| 项 | 说明 |
|----|------|
| 知识空间 | 飞书「知识库」维度的 **space_id**（数字串）；占位示例见下表。 |
| 父节点 | 挂载在**哪一个 wiki 节点下面**的 **parent_node_token**（常为 URL 中 `/wiki/` 后一段）；占位示例见下表。 |
| 产品名称 | 新建 PRD 节点在目录中的**标题**（与需求中的产品/项目名一致）。 |
| 本地文件 | 主 PRD 正文文件 **`PRD_REPORT.md`**；附录/提示词等多文件放在 **`PRD_prompts/`** 目录下（文件名即子文档标题来源，可约定去掉扩展名）。 |
| 身份与权限 | 已 `lark-cli auth login`，且当前用户对目标空间有建节点、编辑文档权限（见 [lark-shared-SKILL.md](lark-shared-SKILL.md)）。 |

若不用下面占位符（即你有真实值），由**当前使用者**（或从链接解析）提供**知识空间 ID** 与**父节点 token**；也可只传 `--parent-node-token`，由 CLI 反查 `space_id`（与显式 `--space-id` 一致时再写入）。

## 写入飞书时建议安装的 Skills（与维护者清单对齐）

| Skill | 作用 |
|-------|------|
| `lark-wiki` | 知识库节点创建与树结构 |
| `lark-doc` | 将 Markdown 写入节点关联云文档（与本节流程配套时**建议与 wiki 同为必选**） |
| `lark-whiteboard` | 将 PRD 内 Mermaid/流程图转为飞书画板（可选） |
| `lark-shared` | 授权与身份 |
| `lark-openapi-explorer` | shortcut 未覆盖能力时的 OpenAPI 兜底 |

全文说明见 [lark-cli.md](lark-cli.md) 中的「写入飞书时的 Skill 组合」一节。

## 占位符示例（公开仓库；真实值仅本地或私有配置）

| 变量 | 占位示例 | 备注 |
|------|----------|------|
| `space_id` | `<YOUR_SPACE_ID>` | 替换为你的目标知识空间 ID（数字串） |
| `parent_node_token` | `<YOUR_PARENT_NODE_TOKEN>` | 替换为父 wiki 节点 token（常为 URL 中 `/wiki/` 后一段） |

> 勿将真实 `space_id`、wiki token 提交到**公开** Git；维护者可复制本表到私有提示词或本地 `*.local.md`（并加入 `.gitignore`）再填真实值。飞书侧目录变更时只改你的本地表或 CLI 参数即可。

## 归档流程（逻辑顺序）

操作细节与参数以 **`lark-wiki`** / **`lark-doc`** 的 Skill 与 CLI 为准（本仓库副本：[lark-wiki-SKILL.md](lark-wiki-SKILL.md)、[lark-doc-SKILL.md](lark-doc-SKILL.md)）。

1. **创建主 PRD 文档节点**  
   - 在默认父节点下执行 `wiki +node-create`（示例参数：`--space-id`、`--parent-node-token`、`--title` 为「产品名称」或用户指定标题）。  
   - 得到新节点的 `node_token`、`obj_token`（关联的 docx）。

2. **写入主文档正文**  
   - 将本地 **`PRD_REPORT.md`** 的内容写入上一步关联的云文档（Markdown → 文档的 Shortcuts 见 `lark-doc`，如 `docs +create` / 更新类命令；**以当前 CLI 版本文档为准**）。

3. **挂载 `PRD_prompts/` 子文档**  
   - 以**步骤 1 新建节点的 `node_token` 作为父节点**，对每个子文件再执行 `wiki +node-create --parent-node-token <主PRD的node_token> --title "<子文档标题>"`。  
   - 再分别将各文件正文写入对应云文档。

4. **校验**  
   - 在飞书知识库中展开父节点，确认主文档与子节点层级正确、正文可读。

## 与 Demo 回归的关系

- **`demo/TEST-RUN.md` / `demo/README.md` 中的「回归」**：只验证 **Markdown PRD 金样与章节自检**，**不包含**调用 `lark-cli`、**不包含**写入飞书。  
- 若要对「归档飞书」做技术验证，需在已登录、有权限的环境中**单独执行**上述步骤，并自行记录结果（可参考项目内其他技能的 `TECH-TEST` 写法）。
