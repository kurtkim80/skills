# prd-discuss

一个 `SKILL.md` 标准格式的 Agent Skill，[Claude Code](https://claude.com/claude-code)、[Codex CLI](https://developers.openai.com/codex/cli) 以及其它兼容 SKILL.md 的编码 agent 都能直接用：把一个模糊的产品想法，经过结构化的对话，推进到可以落地的需求文档——或者一个想清楚的「不做」。

它不是 PRD 模板填充器。它是一个**对话式**的产品思考搭档，核心立场写在 skill 第一段：帮你做出好的产品判断，而不是让你开心。

> An Agent Skill (standard `SKILL.md` format — works with Claude Code, Codex CLI and other SKILL.md-compatible coding agents) that turns a vague product idea into a structured requirements doc — or a well-reasoned "don't build it" — through adversarial, evidence-first dialogue instead of template filling. Chinese-language skill; pure prompt, no scripts, no platform dependency.

## 为什么需要它

和 AI 讨论产品想法有一个专属陷阱：**AI 会放大确认偏误**。它顺着你的提问方向走——你让它验证一个想法，它就能拼出一套看起来调研充分的支持材料，让你边推一个坏想法边确信自己在做尽调。

这个 skill 的解药是把同一工具反方向用。它内置三个**不重叠**的手段逼想法见现实：

- **需求先于方案** —— 用户现在在用什么方式凑合？找不到「在凑合」的证据，需求大概率是臆想的。需求没坐实之前，不进入「怎么解决更好」。
- **竞品现实** —— 主动搜网找已经在解决同一需求的产品；没人做的时候，认真想清楚是蓝海还是伪需求，别默认是蓝海。
- **结构化反方** —— 去攻击而不是附和：论证需求不存在、找失败的同类产品、为最强竞品辩护、质疑你对数据的解读。目标是逼出**最强**的反对论据；反方一击即溃，先怀疑反方没用力，而不是高兴。

反方可以强烈建议放弃，但做不做的决定权始终在你。

## 它怎么工作

六步对话流程，每一步等你确认再往下走：

1. **理解意图** —— 给谁用、解决什么问题、为什么现在做
2. **需求验证与战略锚定** —— 需求站不住就停在这里；站得住，再对照你项目自己的方向文档，问一句：这个想法是在推动当前最要紧的约束，还是又一个跑在证据前面的 scope？
3. **场景拆解** —— 「谁 → 在什么情况下 → 做什么 → 期望什么结果」，具体到能想象出画面
4. **关键决策** —— 识别分歧点，列选项、代价和倾向，不替你拍板
5. **边界与风险** —— 明确不做什么；然后对看起来成立的方案强制再跑一轮结构化反方——方案越顺，这一轮越不能省
6. **输出** —— 三种结局都算正当收尾：**值得做**（出 PRD）、**不做**（出一份「为什么不做」：核心判断、击穿它的证据、什么条件下值得重新捡起来）、**还不确定**（标出关键未知和验证方式）

不会因为「已经聊了很久」就硬凑一份 PRD——那正是它警告的沉没成本陷阱。

另有三处内置检验：讨论前先对齐目标市场（不默认套用任何市场的习惯）；方案看起来很好时追加「一句话转述 / 推广场景 / 一石多鸟」三问；你 @ 了某个文档时讨论范围就锁定在那份文档上。

## 环境要求

- 一个支持 `SKILL.md` 的编码 agent：Claude Code、Codex CLI，或其它兼容平台
- 纯 prompt skill，没有脚本、没有依赖、不挑操作系统
- skill 正文为中文；讨论语言跟随你的对话

## 安装

Claude Code（全局，所有项目都能用）：

```bash
git clone https://github.com/DragonJames2026/prd-discuss.git ~/.claude/skills/prd-discuss
```

Codex CLI（全局）：

```bash
git clone https://github.com/DragonJames2026/prd-discuss.git ~/.codex/skills/prd-discuss
```

只给某个项目用（Claude Code）：

```bash
git clone https://github.com/DragonJames2026/prd-discuss.git .claude/skills/prd-discuss
```

两边装的是同一份 `SKILL.md`。已经 clone 过一份的话，另一边做个软链就行：

```bash
ln -s ~/.claude/skills/prd-discuss ~/.codex/skills/prd-discuss
```

装好后重开一个会话即可。

## 使用

对 agent 说「需求讨论」「我想做一个…」「这个功能要不要做」「prd」都会触发。几点用法建议：

- **想法越模糊越早聊**。第一步就是帮你把模糊点标出来，不会逼你先想清楚再来
- **想锁定讨论范围**，发起时 @ 一份具体文档，skill 只会基于它讨论
- **项目有方向文档**（顶层方向、架构总览一类）时，第二步会主动去读，把想法放进你项目自己的战略坐标系；没有也能用，它会跟你现场确认当前约束
- 得到「不做」的结论时别失望——一份写清楚「为什么不做、什么条件下重新考虑」的留档，和一份 PRD 同样有价值

## License

MIT
