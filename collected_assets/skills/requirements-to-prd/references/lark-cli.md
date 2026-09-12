# 飞书 lark-cli 与本 Skill 的衔接

本文件说明：把 PRD（Markdown）**可选**同步到飞书时，应使用**官方 lark-cli**，以及本目录内哪些文件是「命令与权限」的查阅入口。

## 本机 CLI 以何为准

- **发布包**：**包名**（npm）`@larksuite/cli`，可执行名 `lark-cli`；安装与版本以你本机为准（快照见 [lark-cli-README.zh.md](lark-cli-README.zh.md)）。
- **源码克隆**：若本地克隆了 [larksuite/cli](https://github.com/larksuite/cli)，路径因机器而异；从本技能目录到 CLI 仓库的相对路径仅作**结构示例**（例如与 `requirements-to-prd` 并列的 `../cli`），**勿**假设固定盘符或用户名。

- **上游开源仓库**：[larksuite/cli](https://github.com/larksuite/cli)（`@larksuite/cli`，MIT License）

## 写入飞书时的 Skill 组合（推荐）

以下 Skill 随 **`@larksuite/cli`** 通过 `npx skills add …` 安装（以官方 README 为准）；**本仓库 `references/` 仅镜像部分 `SKILL.md`，未镜像的请读你本机 `cli` 仓库或上游技能包**。

| Skill | 用途（与本 PRD 技能配合） |
|-------|-------------------------|
| **`lark-shared`** | **必选**：`config init`、`auth login`、`--as user/bot`、scope 与 Permission denied。任何写入飞书前先看。 |
| **`lark-wiki`** | **知识库必选**：在指定空间/父节点下 `+node-create` 等，把 PRD 挂到 wiki 树。 |
| **`lark-doc`** | **强烈建议**：把 `PRD_REPORT.md` 等 Markdown **写入 wiki 节点关联的云文档**（docx）；与 `lark-wiki` 建节点顺序配合。 |
| **`lark-whiteboard`** | **可选**：将 PRD 中的 **Mermaid/流程图** 同步为飞书**画板**（白板），便于评审；无此需求可省略。 |
| **`lark-openapi-explorer`** | **兜底**：当 shortcut 未封装、需查官方 OpenAPI 文档并直接 `lark-cli api …` 时使用。 |

**外部用户**使用本技能并写入知识库时，仍须自行提供 **`space_id` 与父节点 token**（或等价 wiki URL）；维护者在提示词里预填的默认值仅对维护者本人适用，见 [wiki-archive-defaults.md](wiki-archive-defaults.md)。

## 本 `references` 目录内放了什么

| 文件 | 说明 |
|------|------|
| [lark-cli-README.zh.md](lark-cli-README.zh.md) | 飞书官方 CLI 中文版 README 快照（安装、快速开始、认证、三层命令） |
| [lark-shared-SKILL.md](lark-shared-SKILL.md) | **必看**：`config init`、`auth login`、身份 `--as user`/`bot`、权限与 Permission denied 处理 |
| [lark-doc-SKILL.md](lark-doc-SKILL.md) | 云文档：`docs +create` / `docs +update` 等，适合把 PRD 写入云文档 |
| [lark-wiki-SKILL.md](lark-wiki-SKILL.md) | 知识库：`wiki +node-create` 等，适合在知识空间挂节点再关联文档 |
| [methodology.md](methodology.md) | 七层需求方法论（与 CLI 无依赖） |

**快照说明**：`lark-*-SKILL.md` 从上游 `larksuite/cli` 仓库的 `skills/.../SKILL.md` 复制。文内若出现指向 `references/子路径` 的链接，在**本目录可能无解**，请到**你本机克隆的 CLI 仓库**内 `skills/<对应 lark-*>/references/` 查看同名文件，或查阅官方技能包。

## 与 `requirements-to-prd` 主流程的关系

- **主 Skill**仍以生成「完整 PRD 正文」为第一交付物。  
- **仅当用户明确要求**将 PRD 发布到飞书、且本机已安装并配置 `lark-cli` 时，Agent 应：

  1. 先读 [lark-shared-SKILL.md](lark-shared-SKILL.md) 确认登录与 scope；  
  2. 再按用户目标选读 [lark-doc-SKILL.md](lark-doc-SKILL.md) 和/或 [lark-wiki-SKILL.md](lark-wiki-SKILL.md) 中的 Shortcuts 与注意事项；  
  3. **不要**用非官方的 `feishu-cli` 等替代；飞书端统一通过 **`lark-cli`** 调用（与 [lark-cli-README.zh.md](lark-cli-README.zh.md) 一致）。

### 知识库归档（空间、父节点与占位符）

若用户要求把 PRD 落到**知识库树**而非仅云文档：按 **`lark-wiki`** 创建节点，并按 **`lark-doc`** 写入 Markdown 正文。  
**落点约定与占位符**（`space_id`、父节点 `wiki token`、主文件 `PRD_REPORT.md`、`PRD_prompts/` 子节点约定）见 **[wiki-archive-defaults.md](wiki-archive-defaults.md)**（公开库内为 `<YOUR_*>`，真实值由用户或维护者私有配置提供）。  
**须向用户确认**：对方提供的 **space_id** 与 **parent_node_token**（或可解析的 wiki URL）；勿假设与占位符或他人租户一致。

## 最低限度命令（人类或 Agent 复核用）

```bash
lark-cli config init
lark-cli auth login --recommend
lark-cli auth status
# 云文档/知识库写操作示例见各 lark-*-SKILL 内 Shortcuts
```

## 与项目内其他 Skill 的一致性

若需「PRD 落知识库 + 画板/文档」的完整编排，可与仓库内 `scattered-requirements-wiki-delivery` 等技能对齐**同一套 lark-cli 约定**；本目录文件便于 **requirements-to-prd** 在**无网络/仅本地仓库**时仍可调阅 CLI 行为。
