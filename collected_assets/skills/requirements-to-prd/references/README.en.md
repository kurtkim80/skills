# requirements-to-prd · references

[中文](README.md)

**7-layer PRD methodology cheat sheet + local copies for Feishu `lark-cli`**

This folder is the **progressive reference layer** for the Agent skill [`requirements-to-prd`](../SKILL.md): the parent `SKILL.md` holds the workflow and PRD template; here we keep a concise methodology, official CLI readmes, and copies of the bundled lark skills needed for “write a doc / create a wiki node”, so the agent does not have to inline long manuals in context.

| Parent skill | Location |
|--------------|----------|
| [../SKILL.md](../SKILL.md) | `requirements-to-prd/` |

---

## Table of contents

- [What this folder fixes](#what-this-folder-fixes)
- [Before / After](#before--after)
- [Layout](#layout)
- [How to use](#how-to-use)
- [What lives where](#what-lives-where)

---

## What this folder fixes

- You want the **full 7-layer PRD flow** without pasting the same theory every time → use [`methodology.md`](methodology.md).  
- The user asked to **push the PRD to Feishu** and you need the order: `config init` vs `auth login`, `docs` vs `wiki` → start from [`lark-cli.md`](lark-cli.md).  
- You are **offline** or only have this repo open → use **`lark-cli-README` and `lark-*-SKILL` snapshots** here.

> [!NOTE]
> Snapshots can lag behind the upstream CLI as versions change. **Validate behavior** against the **`@larksuite/cli` you actually have installed** or the `cli` repo clone on disk. Local clone paths, upstream repo, and snapshot notes live in [`lark-cli.md`](lark-cli.md).

## Before / After

| | No dedicated `references/` (everything in SKILL) | This layout |
|---|:---:|:---:|
| **Methodology** | Bloated main file, harder to maintain | Template stays in `SKILL.md`; theory in [`methodology.md`](methodology.md) |
| **Feishu commands** | Paraphrase from memory each time | Local snapshots + map in [`lark-cli.md`](lark-cli.md) |
| **Relative links in copied lark skills** | Broken in-repo (`references/...`) | Documented in [`lark-cli.md`](lark-cli.md): resolve under **`skills/.../references/`** in your local `larksuite/cli` clone |

---

## Layout

```
references/
├── README.md                 # Chinese README
├── README.en.md              # This file
├── methodology.md            # 7 layers + core toolbox
├── diagram-guide.md          # When to add flow/sequence/architecture diagrams (Chinese)
├── wiki-archive-defaults.md    # Wiki placeholders (space/parent); do not commit real IDs publicly (中文)
├── wiki-archive-defaults.en.md # Same (English)
├── lark-cli.md               # How this skill ties to lark + upstream CLI; no non-official CLIs
├── lark-cli-README.zh.md     # Upstream lark-cli README (zh) snapshot: install, auth, three-tier commands
├── lark-shared-SKILL.md      # config, auth, identity — read before any write
├── lark-doc-SKILL.md         # Feishu Docs; when PRD lands as a doc
└── lark-wiki-SKILL.md        # Wiki nodes; when PRD lands under a knowledge space
```

| File | Role | When to open |
|------|------|--------------|
| [methodology.md](methodology.md) | 7 layers, 10 tools, four levels of a PRD | When aligning on theory or terms |
| [diagram-guide.md](diagram-guide.md) | Requirement signals → diagram types (Mermaid); PRD §3–§8 | When choosing flowcharts, sequence, state, architecture sketches |
| [wiki-archive-defaults.en.md](wiki-archive-defaults.en.md) | Wiki target placeholders; user supplies real space/node or private local config | When publishing PRD under a Feishu wiki tree |
| [lark-cli.md](lark-cli.md) | Read order, relationship to delivery | When user wants Feishu export |
| [lark-cli-README.zh.md](lark-cli-README.zh.md) | Official install and command model | When checking global `npm` / `lark-cli` usage |
| [lark-shared-SKILL.md](lark-shared-SKILL.md) | `lark-cli config` / `auth` | First-time setup, permission errors |
| [lark-doc-SKILL.md](lark-doc-SKILL.md) | `docs` shortcuts, doc tokens | Create/update a Lark doc from Markdown |
| [lark-wiki-SKILL.md](lark-wiki-SKILL.md) | `wiki`, parent node, space | Create nodes under a wiki tree |

---

## How to use

- **Secrets & tokens**: Do not commit App Secret, access tokens, or real wiki `space_id`/node tokens to public Git; see [../README.en.md](../README.en.md) — *Security & privacy*.  
- **Default path**: finish the full PRD in [../SKILL.md](../SKILL.md) first; only then use [lark-cli.md](lark-cli.md) for Feishu.  
- **Do not** replace official `lark-cli` with unofficial “feishu-cli”-style tools for the flows described here.  
- Other skills in this repo (e.g. `scattered-requirements-wiki-delivery`) that share the same **lark-cli** contract can cross-check auth and commands using this folder.

---

## What lives where

| Content | Location |
|---------|----------|
| PRD required sections, EARS, GWT, MoSCoW, checklist | [../SKILL.md](../SKILL.md) |
| 7-layer theory and tool-to-layer map | [methodology.md](methodology.md) |
| Diagram rules for PRD | [diagram-guide.md](diagram-guide.md) |
| Wiki archive placeholders (real IDs local/private only) | [wiki-archive-defaults.en.md](wiki-archive-defaults.en.md) |
| Feishu config and write path | [lark-cli.md](lark-cli.md) + `lark-*` snapshots in this folder |