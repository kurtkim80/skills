# requirements-to-prd · references

[English](README.en.md)

**七层方法论附件 + 飞书 lark-cli 本地查阅副本**

本目录是 Agent Skill [`requirements-to-prd`](../SKILL.md) 的**渐进式资料层**：主文件 `SKILL.md` 负责工作流与 PRD 模板；此处放方法论速查、官方 CLI 说明快照，以及「写云文档 / 建知识库节点」时必读的 lark 捆绑 Skill 副本，避免上下文塞满大段说明。

| 主 Skill | 父目录 |
|----------|--------|
| [../SKILL.md](../SKILL.md) | `requirements-to-prd/` |

---

## 目录

- [本目录解决什么问题](#本目录解决什么问题)
- [Before / After](#before--after)
- [文件结构](#文件结构)
- [使用提示](#使用提示)
- [与主 Skill 的分工](#与主-skill-的分工)

---

## 本目录解决什么问题

- **想按七层法写全 PRD**，但不想在对话里反复贴同一套理论 → 用 [`methodology.md`](methodology.md) 速查。  
- **用户要把 PRD 同步到飞书**，需要立即知道先 `config init` 还是先 `auth login`、用 `docs` 还是 `wiki` → 用 [`lark-cli.md`](lark-cli.md) 定查阅顺序。  
- **机器离线或只打开了本仓库**，仍要核对命令行行为 → 用本目录里的 **lark-cli-README** 与 **lark-*-SKILL 快照**。

> [!NOTE]
> 快照可能与上游 CLI 随版本更新而落后；**命令与权限以**本机/仓库内的 **`@larksuite/cli` 实际行为**为准。本机副本路径、上游仓库与快照说明见 [lark-cli.md](lark-cli.md)。

## Before / After

| | 无 `references/`，全塞进 SKILL.md | 有本目录（当前） |
|---|:---:|:---:|
| **方法论** | 主文件冗长、难维护 | 主文件保留模板，理论独立成 [`methodology.md`](methodology.md) |
| **飞书操作** | 每次从外网/记忆复述命令 | 本地快照 + 衔接说明 [`lark-cli.md`](lark-cli.md) |
| **lark 子 Skill 链接** | 复制的 SKILL 内 `references/子路径` 在快照中断裂 | 在 [`lark-cli.md`](lark-cli.md) 中说明如何到**上游** `larksuite/cli` 仓库的 `skills/.../references/` 补全 |

---

## 文件结构

```
references/
├── README.md                 # 本说明（中文）
├── README.en.md              # 本说明（英文）
├── methodology.md            # 七层：机会→…→验证；与核心工具箱速查
├── diagram-guide.md          # 何时配流程/时序/架构等图；需求信号与 Mermaid 类型
├── wiki-archive-defaults.md    # 知识库归档占位符（space_id/父节点）；真实值勿提交公开库
├── wiki-archive-defaults.en.md # 同上（英文）
├── lark-cli.md               # 与主 Skill 的衔接：何时读、上游 CLI、勿用 feishu-cli
├── lark-cli-README.zh.md     # 官方 lark-cli 中文 README 快照（安装/认证/三层命令）
├── lark-shared-SKILL.md      # 配置、登录、身份与权限（任何写操作前读）
├── lark-doc-SKILL.md         # 云文档；PRD 落「文档」场景
└── lark-wiki-SKILL.md        # 知识库节点；PRD 落「知识空间」场景
```

| 文件 | 用途 | 何时打开 |
|------|------|----------|
| [methodology.md](methodology.md) | 七层方法论、10 个核心工具、PRD 四层次补全 | 需要对照理论或术语时 |
| [diagram-guide.md](diagram-guide.md) | 需求特征与流程/时序/架构等配图规则 | 写 §3～§8 时需决定是否画 Mermaid 图 |
| [wiki-archive-defaults.md](wiki-archive-defaults.md) | 知识库落点占位符；须用户自备或本地私有配置真实 space/节点 | PRD 写入飞书知识库树时 |
| [wiki-archive-defaults.en.md](wiki-archive-defaults.en.md) | 同上（英文） | 英文读者或双语仓库 |
| [lark-cli.md](lark-cli.md) | 飞书 CLI 与 PRD 交付关系、读副本顺序 | 用户要求归档到飞书时 |
| [lark-cli-README.zh.md](lark-cli-README.zh.md) | 官方安装与命令体系 | 核对 `npm` / `lark-cli` 全局行为 |
| [lark-shared-SKILL.md](lark-shared-SKILL.md) | `lark-cli config` / `auth` | 首次配置、Permission denied |
| [lark-doc-SKILL.md](lark-doc-SKILL.md) | `docs` Shortcuts、Markdown 与文档 token | 创建/更新云文档 |
| [lark-wiki-SKILL.md](lark-wiki-SKILL.md) | `wiki`、父节点、空间 | 在知识库下建子节点并挂文档 |

---

## 使用提示

- **密钥与 token**：勿将 App Secret、各类 access token、真实 wiki `space_id`/节点 token 写入公开 Git；见仓库根 [../README.md](../README.md)「安全与隐私」一节。  
- **主流程**：先完成 [../SKILL.md](../SKILL.md) 中的 PRD 全文；**再**在需要时按 [lark-cli.md](lark-cli.md) 操作飞书。  
- **不要**用非官方的 `feishu-cli` 等替代与官方 `lark-cli` 的约定。  
- 与仓库内 `scattered-requirements-wiki-delivery` 等技能共用同一套 **lark-cli** 时，本目录便于只打开 **references** 就能对齐权限与命令。

---

## 与主 Skill 的分工

| 内容 | 放在哪里 |
|------|----------|
| PRD 必含章节、EARS、GWT、MoSCoW、自检清单 | [../SKILL.md](../SKILL.md) |
| 七层法展开、工具到层的映射 | [methodology.md](methodology.md) |
| PRD 配图类型与触发条件 | [diagram-guide.md](diagram-guide.md) |
| 知识库归档占位符与用户确认项 | [wiki-archive-defaults.md](wiki-archive-defaults.md) / [wiki-archive-defaults.en.md](wiki-archive-defaults.en.md) |
| 飞书侧配置与写入入口 | [lark-cli.md](lark-cli.md) + 本目录各 `lark-*` 快照 |
