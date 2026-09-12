---
name: requirements-to-prd
description: >-
  Transforms user requirements (fragmented or complete) into a full product PRD using a seven-layer
  methodology: opportunity, problem, insight, solution design, requirement expression, prioritization
  and versioning, and validation/closed-loop. Combines problem definition (JTBD, 5 Whys, problem statement),
  insight (persona, journey, constraints), design (use cases, flows, state, MVP), and expression (EARS,
  user stories, Given-When-Then, NFRs) with MoSCoW/RICE-style prioritization. Use when the user asks
  for a PRD, product requirements document, 需求转PRD, 产品需求文档, 从需求写PRD, or to apply this product methodology map.
---

# 需求 → 完整 PRD（七层方法论）

## 何时使用

用户在对话中**提供一段或多段需求**（零散、口头、草稿或较完整），需要输出**一份可供设计/研发/测试/业务对齐的完整产品 PRD** 时，按本 Skill 的**工作流与模板**执行。

**主交付物**为 **Markdown 结构正文**（可写入用户指定本地路径或直接在对话中输出）。  
**可选**：用户明确要求将 PRD **同步到飞书**（云文档/知识库）且本机已安装并配置官方 **`lark-cli`** 时，按 [references/lark-cli.md](references/lark-cli.md) 与各 **lark-\*** Skill 执行；未满足条件时**仅交付 Markdown**。

**谁提供知识库落点？**

- **给外部用户用时**：若要把 PRD 写入**飞书知识库树**，须由**该用户**提供（或给出可解析的 wiki 链接）**知识空间**与**父节点**（`space_id` + `parent_node_token`，或仅父节点 token 由 CLI 反查空间，见 `lark-wiki`）。  
- **维护者自用提示词**：可在系统提示词或**未提交**的本地文件里写死**自己的** `space_id` / 父节点；公开仓库内仅保留占位符示例，见 [references/wiki-archive-defaults.md](references/wiki-archive-defaults.md)。**不能**用你的默认替代其他用户的显式提供——对外分发时应要求对方自备落点。

**写入飞书时建议安装的 lark-cli Skills（能力组合）**见 [references/lark-cli.md](references/lark-cli.md) 首节「写入飞书时的 Skill 组合」表格；至少包含 **`lark-wiki`（知识库）**、**`lark-shared`（授权）**、**`lark-whiteboard`（可选：流程图/Mermaid 落白板）**、**`lark-openapi-explorer`（兜底原生 OpenAPI）**；将 Markdown 灌入 wiki 关联云文档时通常还需要 **`lark-doc`**（或全程改用 OpenAPI 自拼）。

## 执行原则

1. **从模糊到可执行**：先七层**推理与补全**（在文档中区分「用户原文」「推断」「待补充」），再统合成一篇 PRD。  
2. **禁止编造事实**：若缺业务数据、系统名、政策约束，在对应章节写 **`待补充`** 或列「假设/待确认问题清单」。  
3. **EARS 与 GWT 组合**：系统行为用 EARS 句式；关键路径用 **Given-When-Then** 收束验收。  
4. **控制范围**：PRD 内必须出现 **In Scope / Out of Scope** 与 **V1 必做**；避免「一次写完所有未来版本」导致无法落地。  
5. 理论与术语的完整展开见 [references/methodology.md](references/methodology.md)（**撰写时按需查阅**，避免在正文堆砌教科书）。飞书 CLI 与可选归档见 [references/lark-cli.md](references/lark-cli.md)。  
6. **配图（可选但强建议按规则）**：流程图、时序图、架构/状态/数据流等 **Mermaid** 图，在命中「强流程 / 强协作 / 强状态 / 强集成 / 强数据」等条件时补充，规则与需求信号对照表见 [references/diagram-guide.md](references/diagram-guide.md)；无信号则不必堆图。

## 工作流（建议顺序）

对用户的输入，在内心按七层**逐项覆盖**；若某层用户已写得很全，可合并小节，但**不跳过**「优先级」与「验证/指标」两块的实质性内容（即使简短）。

| 顺序 | 层 | 本 Skill 在 PRD 中的落点（最少要写到） |
|------|----|----------------------------------------|
| 1 | 机会识别 | §1 背景、业务目标、与战略/OKR 的对齐；无则写**合理推断**+**待补充** |
| 2 | 问题定义 | §2 问题陈述、JTBD/5 Whys 精要、**不在此层写界面细节** |
| 3 | 需求洞察 | §3 用户与角色、核心场景、现状流程摘要、**约束**（政策/系统/时间） |
| 4 | 方案设计 | §4 目标方案、范围、**业务流程/状态**、MVP 边界、异常与边界 |
| 5 | 需求表达 | §5～§9 **功能（EARS）**、**业务规则**、**数据**、**非功能**、**验收（GWT）** |
| 6 | 优先级 | §10 MoSCoW 或 RICE 摘要表；**V1** 与**后续** |
| 7 | 验证交付 | §11 成功指标/埋点、**上线后看哪些数**、风险、**待评审问题** |

## PRD 输出模板（必须沿用一级标题与顺序）

用下面骨架生成**一篇** Markdown 文档。二级标题可增删，但 **§1、§2、§5、§8、§10、§11** 信息不得为空（无信息则写 `待补充` 或显式「不适用」+ 原因）。

```markdown
# {产品/项目名称} 产品需求文档（PRD）

> **文档状态**：草案 | 评审中 | 已基线（选一）  
> **版本**：v0.1  **日期**：YYYY-MM-DD  **作者**：Agent+用户

---

## 1. 背景与目标（机会层）

### 1.1 背景与机会
（为何现在做；可含战略/OKR/北极星/漏斗等**摘要**，避免长篇理论。）

### 1.2 业务目标与可衡量指标
| 目标 | 指标 | 基线/目标值 | 备注 |
|------|------|-------------|------|
| … | … | … | 待补充可 |

### 1.3 不做的后果 / 做错的代价（可选但推荐）
（简短：若不做，业务或用户会承受什么。）

---

## 2. 问题定义

### 2.1 问题陈述（Problem Statement）
**谁** 在 **什么场景** 下遇到 **什么问题**，导致 **什么影响**。

### 2.2 根因与 JTBD
- **5 Whys 摘要**（可列表，不必凑满 5 条，以止于可行动根因为准）
- **Jobs To Be Done**：用户要完成的「任务」一句话

### 2.3 How Might We（可选）
（1～3 条 HMW，用于对齐探索方向。）

---

## 3. 用户、场景与现状（洞察层）

### 3.1 用户与角色
| 角色 | 描述 | 主要诉求 | 使用频率/权重 |
|------|------|----------|----------------|
| … | … | … | 高/中/低（或待补充） |

### 3.2 用户故事（User Story，覆盖主路径）
- 作为「角色」，我希望「能力」，以便「价值」。

### 3.3 核心场景与用户旅程（摘要）
（可用子小节或简表；复杂流程在 §4.2 用 Mermaid/步骤展开。**何时用何种图**见 [references/diagram-guide.md](references/diagram-guide.md)。）

### 3.4 现状与约束
- **现状流程/系统**  
- **业务规则、合规、** **系统/接口/数据** 约束

---

## 4. 方案与范围（设计层）

### 4.1 产品形态与信息架构（若适用）
（端：Web/小程序/App/纯后端；主导航或模块关系。）

### 4.2 业务流程与状态
- **主流程**（文字步骤或 Mermaid `flowchart` / `stateDiagram`；多系统协作时加 `sequenceDiagram`）  
- **关键对象与状态**（如订单/工单/审批；状态机表）  
- **配图选型**：按 [references/diagram-guide.md](references/diagram-guide.md) 中「需求信号 → 图类型」表执行。

### 4.3 MVP 范围
**本版必须达到**：…  
**明确推迟**：…

### 4.4 方案取舍（可选）
（若存在 A/B 方案，写选型理由与**验证计划**摘要。）

---

## 5. 功能需求（EARS，需求表达层）

> 对每条**分配编号**：FR-001, FR-002, … 使用 **EARS** 易混分类（Ubiquitous / Event-driven / State-driven / Unwanted / Optional）在括号或标签中标明。

### 5.1 功能需求列表
1. **FR-001** …（EARS 规范句；主语为系统/产品）  
2. **FR-002** …  
…

### 5.2 用例（Use Case）摘要表（多角色/强流程时推荐）
| 用例ID | 名称 | 主参与者 | 前置条件 | 成功结果 |
|--------|------|----------|----------|----------|
| UC-01 | … | … | … | … |

---

## 6. 业务规则
（可编号 BR-001…；与 FR 区别：**规则/策略/计算口径** 放此处。）

---

## 7. 异常、边界与错误处理
| 场景 | 系统行为 | 用户提示/日志 | 备注 |
|------|----------|----------------|------|
| … | … | … | … |

---

## 8. 权限与数据

### 8.1 角色与权限（RBAC 或具体规则）
| 能力 | 角色/条件 | 说明 |
|------|-----------|------|
| … | … | … |

### 8.2 数据定义（关键实体/字段级摘要）
| 实体 | 关键字段/枚举 | 来源 | 约束 |
|------|----------------|------|------|
| … | … | … | … |

### 8.3 与外部系统/接口（若有）
| 系统 | 接口/同步方式 | 说明 |
|------|----------------|------|
| … | … | … |

---

## 9. 非功能需求（NFR）
| 类型 | 要求 | 验收方式 |
|------|------|----------|
| 性能 | … | … |
| 安全/权限 | … | … |
| 可用性/兼容 | … | … |
| 审计/日志 | … | … |
| 其他 | … | … |

---

## 10. 验收标准

### 10.1 Given-When-Then（主路径与关键异常）
| ID | 场景 | GWT | 关联FR |
|----|------|-----|--------|
| AC-01 | … | **Given** … **When** … **Then** … | FR-… |

### 10.2 验收清单（可勾选的客观项）
- [ ] …
- [ ] …

---

## 11. 优先级、版本与成功度量（优先级 + 验证层）

### 11.1 MoSCoW 或 RICE 摘要
| 需求/主题 | 分类或分数 | 说明 |
|------------|------------|------|
| … | Must/Should/… 或 R-I-C-E | … |

### 11.2 本 PRD 范围与路线图
- **V1（本单）**  
- **V1.1+**  
- **明确不做（Out of Scope）**

### 11.3 指标与埋点
| 指标 | 埋点/事件 | 作用 |
|------|-----------|------|
| … | … | … |

### 11.4 风险与未决问题
| 风险/问题 | 影响 | 缓解/依赖 |
|------------|------|-----------|
| … | 高/中/低 | … |

### 11.5 需求追溯（轻量，可选但推荐）
| 业务目标 | PRD 章节/FR | 验收项 |
|----------|-------------|--------|
| … | FR-… | AC-… |
```

## 成稿后自检（Checklist）

- [ ] 是否从「功能愿望」回写到了**可验证的问题**（§2）？  
- [ ] §5 的 EARS 是否**可测试、无「尽快」「友好」等模糊词**（除非在 §9/§10 量化）？  
- [ ] §8、§9 是否覆盖权限、**数据**、**NFR**？  
- [ ] §10 GWT 是否覆盖**主成功 + 关键失败**？  
- [ ] §10–§11 是否含 **MVP/Out of Scope** 与**上线后指标**？  
- [ ] 若需求命中 [diagram-guide](references/diagram-guide.md) 中的「应配图」条件，§3/§4/§8 是否已用**对应类型的图或显式说明为何不画**？

## 与「零散需求结构化」类 Skill 的边界

若用户**只要** EARS/追溯表/测试用例/飞书知识库交付，不强调「完整 PRD 七层叙事」，可转向项目内其他 `scattered-*` 或专项 Skill；**本 Skill 优先产出「完整 PRD 单文档」**。

## Demo（回归用）

固定输入与示例金样见 [`demo/`](demo/)：[demo/input-requirement.md](demo/input-requirement.md)（用户原文）、[demo/expected-prd.md](demo/expected-prd.md)（按本模板撰写的参考 PRD）、[demo/README.md](demo/README.md)（如何通过自检）、[demo/TEST-RUN.md](demo/TEST-RUN.md)（回归记录样例）。  
仓库级说明、英文 README 与**勿提交的密钥/token 约定**见 [README.md](README.md)、[README.en.md](README.en.md)。

## 附：术语速查

- **EARS** / **GWT** / **MoSCoW** / **RICE** / **MVP** 的展开与七层对照见 [references/methodology.md](references/methodology.md)。
