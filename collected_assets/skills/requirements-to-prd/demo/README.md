# requirements-to-prd · Demo 与回归

本目录与 [../SKILL.md](../SKILL.md) 末尾 **Demo（回归用）** 一致：固定**输入**与**金样 PRD**，用于人工或 Agent 自检「是否仍按七层模板成稿」。

## 文件

| 文件 | 说明 |
|------|------|
| [input-requirement.md](input-requirement.md) | 用户侧原始需求（测试时勿改**字面表述**） |
| [expected-prd.md](expected-prd.md) | 按本技能 PRD 模板撰写的参考输出 |
| [TEST-RUN.md](TEST-RUN.md) | 每次回归的简要记录（可追加） |

若要将金样（如 `expected-prd.md`）同步到飞书，按 [../references/lark-cli.md](../references/lark-cli.md) 与 [../references/wiki-archive-defaults.md](../references/wiki-archive-defaults.md) 自行配置 `lark-cli` 与知识库落点即可。

## 如何通过自检

对照 [../SKILL.md](../SKILL.md) **成稿后自检（Checklist）**：

- [ ] §2 是否从功能愿望回写到可验证问题  
- [ ] §5 EARS 可测试、少模糊词（「友好」等是否在 §9/§10 量化）  
- [ ] §8、§9 是否含权限、数据、NFR  
- [ ] §10 GWT 是否覆盖主成功与关键失败  
- [ ] §10–§11 是否含 MVP、Out of Scope、上线后指标  
- [ ] 若需求命中 [../references/diagram-guide.md](../references/diagram-guide.md) 的「应配图」条件，是否已配图或说明为何不画  

**与金样比较**：`expected-prd.md` 不必逐字相同，但**一级标题顺序**、**§5 FR 编号习惯**、**§10/§11 必含项**应一致；业务内容允许随评审迭代。

## 与仓库根目录关系

- 本技能根目录为 `requirements-to-prd/`。  
- 未配置飞书时，交付物仅为 Markdown；见 [../references/lark-cli.md](../references/lark-cli.md)。  
- 密钥、token、真实 wiki 标识勿入公开库：见 [../README.md](../README.md)。
